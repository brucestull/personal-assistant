from django.contrib import admin
from .models import StorageLocation, Item, ActivityType, Activity


@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ["name", "parent_location", "user"]
    search_fields = ["name"]
    list_filter = ["user"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "storage_location", "user"]
    search_fields = ["name"]
    list_filter = ["user", "storage_location"]


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
    search_fields = ["name"]
    list_filter = ["user"]


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "type",
        "due_date",
        "target_item",
        "target_location",
        "user",
    ]
    list_filter = ["type", "is_recurring", "user"]
    search_fields = ["name", "description"]
