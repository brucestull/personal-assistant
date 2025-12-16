# plan_it/admin.py

from django.contrib import admin

from plan_it.models import (
    Activity,
    ActivityInstance,
    ActivityLocation,
    ActivityType,
    Item,
    StorageLocation,
)


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    fields = ["name", "description"]


class SubLocationInline(admin.TabularInline):
    model = StorageLocation
    extra = 0
    fk_name = "parent_location"
    fields = ["name"]
    verbose_name = "Sub-location"
    verbose_name_plural = "Sub-locations"


@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "parent_location", "item_count"]
    search_fields = ["name", "user__username"]
    list_filter = ["user"]
    readonly_fields = ["item_count"]
    inlines = [ItemInline, SubLocationInline]

    def item_count(self, obj):
        return obj.item_set.count()

    item_count.short_description = "Items"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "storage_location", "description_preview"]
    search_fields = ["name", "description", "user__username"]
    list_filter = ["storage_location", "user"]
    autocomplete_fields = ["storage_location"]

    def description_preview(self, obj):
        if obj.description:
            preview = obj.description[:50]
            return preview + "..." if len(obj.description) > 50 else preview
        return "-"

    description_preview.short_description = "Description"


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "activity_count"]
    search_fields = ["name", "user__username"]
    list_filter = ["user"]
    readonly_fields = ["activity_count"]

    def activity_count(self, obj):
        return obj.activity_set.count()

    activity_count.short_description = "Activities"


class SubActivityLocationInline(admin.TabularInline):
    model = ActivityLocation
    extra = 0
    fk_name = "parent_location"
    fields = ["name"]
    verbose_name = "Sub-location"
    verbose_name_plural = "Sub-locations"


@admin.register(ActivityLocation)
class ActivityLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "parent_location", "activity_count"]
    search_fields = ["name", "user__username"]
    list_filter = ["user"]
    readonly_fields = ["activity_count"]
    inlines = [SubActivityLocationInline]

    def activity_count(self, obj):
        return obj.activity_set.count()

    activity_count.short_description = "Activities"


class ActivityInstanceInline(admin.TabularInline):
    model = ActivityInstance
    extra = 0
    fields = ["completed_at", "name_snapshot"]
    readonly_fields = ["completed_at", "name_snapshot"]
    can_delete = False
    max_num = 5
    verbose_name = "Recent Completion"
    verbose_name_plural = "Recent Completions (Latest 5)"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("-completed_at")[:5]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user",
        "type",
        "activity_location",
        "target_item",
        "due_date",
        "due_status_display",
        "is_recurring",
        "last_completed",
    ]
    list_filter = ["type", "is_recurring", "due_date", "user", "last_completed"]
    search_fields = ["name", "description", "user__username"]
    autocomplete_fields = ["type", "target_item", "activity_location"]
    readonly_fields = ["last_completed", "due_status_display"]
    inlines = [ActivityInstanceInline]
    fieldsets = (
        ("Basic Information", {
            "fields": ("user", "name", "type", "description")
        }),
        ("Location & Target", {
            "fields": ("activity_location", "target_item")
        }),
        ("Schedule", {
            "fields": (
                "due_date",
                "is_recurring",
                "last_completed",
                "due_status_display",
            )
        }),
    )

    def due_status_display(self, obj):
        status = obj.due_status()
        if status == "overdue":
            return "🔴 Overdue"
        elif status == "today":
            return "🟡 Due Today"
        elif status == "upcoming":
            return "🟢 Upcoming"
        return "No due date"

    due_status_display.short_description = "Due Status"


@admin.register(ActivityInstance)
class ActivityInstanceAdmin(admin.ModelAdmin):
    list_display = (
        "name_snapshot",
        "user",
        "type_name_snapshot",
        "activity_location_name_snapshot",
        "completed_at",
    )
    list_filter = (
        "user",
        "completed_at",
        "type_name_snapshot",
    )
    search_fields = ("name_snapshot", "type_name_snapshot", "user__username")
    readonly_fields = ["completed_at"]
    date_hierarchy = "completed_at"
