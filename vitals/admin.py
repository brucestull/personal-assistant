from django.contrib import admin

from vitals.models import BloodPressure


@admin.register(BloodPressure)
class VitalsAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for the `BloodPressure` model.
    """

    list_display = (
        "user",
        "systolic",
        "diastolic",
        "created",
    )
    ordering = ("-created",)
    list_filter = (
        "user",
        "created",
    )
    search_fields = (
        "user__username",
        "systolic",
        "diastolic",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "systolic",
                    "diastolic",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )
