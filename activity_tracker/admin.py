from django.contrib import admin

from .models import Activity, ActivityCompleted, ActivityType


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    """
    Admin for the `ActivityType` model.
    """

    list_display = ("name", "user")
    # search_fields = (
    #     "name",
    #     # "user"
    # )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """
    Admin for the `Activity` model.
    """

    list_display = ("name", "user", "activity_type")
    list_filter = ("activity_type",)
    # search_fields = (
    #     "name",
    #     # "user",
    #     "activity_type",
    #     "notes",
    # )


@admin.register(ActivityCompleted)
class ActivityCompletedAdmin(admin.ModelAdmin):
    """
    Admin for the `ActivityCompleted` model.
    """

    list_display = ("activity", "user", "date")
    # search_fields = (
    #     "activity",
    #     # "user"
    # )
    fields = ("activity", "user", "date")
