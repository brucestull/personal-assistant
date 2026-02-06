# packing_list/admin.py

from __future__ import annotations

from django.contrib import admin
from django.db.models import Count, Q

from packing_list.models import Activity, Item, Task


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    fields = ("name", "quantity", "is_packed", "is_essential", "description", "user")
    readonly_fields = ("user",)
    show_change_link = True


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("name", "is_completed", "description", "user")
    readonly_fields = ("user",)
    show_change_link = True


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "description",
        "item_count",
        "packed_item_count",
        "packed_percent",
        "task_count",
        "completed_task_count",
    )
    search_fields = ("name", "description", "user__username", "user__email")
    list_filter = ("user",)
    ordering = ("name",)
    inlines = (ItemInline, TaskInline)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Avoid N+1 queries in list_display summary columns.
        return qs.annotate(
            _item_count=Count("items", distinct=True),
            _packed_item_count=Count(
                "items", filter=Q(items__is_packed=True), distinct=True
            ),
            _task_count=Count("tasks", distinct=True),
            _completed_task_count=Count(
                "tasks", filter=Q(tasks__is_completed=True), distinct=True
            ),
        )

    @admin.display(description="Items", ordering="_item_count")
    def item_count(self, obj: Activity) -> int:
        return int(getattr(obj, "_item_count", 0) or 0)

    @admin.display(description="Packed Items", ordering="_packed_item_count")
    def packed_item_count(self, obj: Activity) -> int:
        return int(getattr(obj, "_packed_item_count", 0) or 0)

    @admin.display(description="% Packed")
    def packed_percent(self, obj: Activity) -> str:
        total = self.item_count(obj)
        packed = self.packed_item_count(obj)
        if total <= 0:
            return "—"
        pct = int(round((packed / total) * 100))
        return f"{pct}%"

    @admin.display(description="Tasks", ordering="_task_count")
    def task_count(self, obj: Activity) -> int:
        return int(getattr(obj, "_task_count", 0) or 0)

    @admin.display(description="Done Tasks", ordering="_completed_task_count")
    def completed_task_count(self, obj: Activity) -> int:
        return int(getattr(obj, "_completed_task_count", 0) or 0)

    def save_formset(self, request, form, formset, change):
        """
        When editing Activity with inlines:
        - ensure inline entries have user set to the Activity.user
        """
        instances = formset.save(commit=False)
        for inst in instances:
            if isinstance(inst, (Item, Task)):
                inst.user = form.instance.user
            inst.save()
        formset.save_m2m()


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "activity",
        "activity_user",
        "quantity",
        "is_packed",
        "is_essential",
    )
    search_fields = (
        "name",
        "description",
        "activity__name",
        "user__username",
        "user__email",
    )
    list_filter = ("activity", "is_packed", "is_essential")
    ordering = ("activity", "name")
    list_editable = ("is_packed", "is_essential", "quantity")
    list_select_related = ("activity", "user", "activity__user")
    autocomplete_fields = ("activity",)
    raw_id_fields = ("user",)

    def save_model(self, request, obj, form, change):
        # Keep user consistent with Activity.user unless explicitly set.
        if obj.activity and (obj.user_id is None):
            obj.user = obj.activity.user
        super().save_model(request, obj, form, change)

    @admin.display(description="Activity User")
    def activity_user(self, obj: Item) -> str:
        if obj.activity and obj.activity.user:
            return obj.activity.user.username
        return "N/A"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "activity",
        "activity_user",
        "is_completed",
    )
    search_fields = (
        "name",
        "description",
        "activity__name",
        "user__username",
        "user__email",
    )
    list_filter = ("activity", "is_completed")
    ordering = ("activity", "name")
    list_editable = ("is_completed",)
    list_select_related = ("activity", "user", "activity__user")
    autocomplete_fields = ("activity",)
    raw_id_fields = ("user",)

    def save_model(self, request, obj, form, change):
        if obj.activity and (obj.user_id is None):
            obj.user = obj.activity.user
        super().save_model(request, obj, form, change)

    @admin.display(description="Activity User")
    def activity_user(self, obj: Task) -> str:
        if obj.activity and obj.activity.user:
            return obj.activity.user.username
        return "N/A"
