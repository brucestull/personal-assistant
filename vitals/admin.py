from django.contrib import admin

from vitals.models import BloodPressure, Pulse


@admin.register(BloodPressure)
class VitalsAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for the `BloodPressure` model.
    """

    list_display = (
        "user",
        "systolic",
        "diastolic",
        "pulse",
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
        "pulse",
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
                    "pulse",
                )
            },
        ),
        (
            "Dates/Metadata",
            {
                "fields": (
                    "created",
                    "updated",
                )
            },
        ),
    )


@admin.register(Pulse)
class PulseAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for the `Pulse` model.
    """

    list_display = (
        "user",
        "bpm",
        "created",
    )
    ordering = ("-created",)
    list_filter = (
        "user",
        "created",
    )
    search_fields = (
        "user__username",
        "bpm",
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
                    "bpm",
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
