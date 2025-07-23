# packing_list/admin.py

from django.contrib import admin

from packing_list.models import Activity, Item


class ItemInline(admin.TabularInline):
    model = Item.activities.through
    extra = 1


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "description")
    search_fields = ("name", "description")
    list_filter = ("user",)
    ordering = ("-name",)
    inlines = [ItemInline]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_activities",
        "get_activity_users",
        "quantity",
        "is_packed",
        "is_essential",
    )
    search_fields = ("name", "description")
    list_filter = (
        "is_packed",
        "is_essential",
        "activities",
    )  # M2M fields are supported in filter
    filter_horizontal = ("activities",)
    ordering = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("activities__user", "user")

    def get_activities(self, obj):
        return ", ".join(a.name for a in obj.activities.all())

    get_activities.short_description = "Activities"

    def get_activity_users(self, obj):
        return (
            ", ".join(a.user.username for a in obj.activities.all() if a.user) or "N/A"
        )

    get_activity_users.short_description = "Activity Users"
