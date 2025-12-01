# packing_list/admin.py

from django.contrib import admin

from packing_list.models import Activity, Item, Task


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "description")
    search_fields = ("name", "description")
    list_filter = ("user",)
    ordering = ("-name",)


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
    search_fields = ("name", "description")
    list_filter = ("activity", "is_packed", "is_essential")
    ordering = ("activity", "name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("activity", "user", "activity__user")

    def activity_user(self, obj):
        return (
            obj.activity.user.username if obj.activity and obj.activity.user else "N/A"
        )

    activity_user.short_description = "Activity User"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "activity",
        "activity_user",
        "is_completed",
    )
    search_fields = ("name", "description")
    list_filter = ("activity", "is_completed")
    ordering = ("activity", "name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("activity", "user", "activity__user")

    def activity_user(self, obj):
        return (
            obj.activity.user.username if obj.activity and obj.activity.user else "N/A"
        )

    activity_user.short_description = "Activity User"
