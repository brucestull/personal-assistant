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


@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "parent_location"]
    search_fields = ["name"]
    list_filter = ["user"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "storage_location"]
    search_fields = ["name"]
    list_filter = ["storage_location", "user"]


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
    search_fields = ["name"]
    list_filter = ["user"]


@admin.register(ActivityLocation)
class ActivityLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "parent_location"]
    search_fields = ["name"]
    list_filter = ["user"]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user",
        "type",
        "activity_location",
        "target_item",
        "due_date",
        "is_recurring",
        "last_completed",
    ]
    list_filter = ["type", "is_recurring", "due_date", "user", "last_completed"]
    search_fields = ["name", "description"]
    autocomplete_fields = ["type", "target_item", "activity_location"]


@admin.register(ActivityInstance)
class ActivityInstanceAdmin(admin.ModelAdmin):
    list_display = (
        "name_snapshot",
        "type_name_snapshot",
        "target_item_name_snapshot",
        "activity_location_name_snapshot",
        "completed_at",
    )
    list_filter = (
        "name_snapshot",
        "type_name_snapshot",
        "target_item_name_snapshot",
        "activity_location_name_snapshot",
        "completed_at",
    )
    search_fields = ("name_snapshot", "type_name_snapshot")
