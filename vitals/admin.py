from django.contrib import admin

from vitals.models import BloodPressure, Pulse, Temperature, BodyWeight


@admin.register(BloodPressure)
class VitalsAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `BloodPressure` model.
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
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `Pulse` model.
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


@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `Temperature` model.
    """

    list_display = (
        "subject",
        "measurement",
        "created",
    )
    ordering = ("-created",)
    list_filter = (
        "subject",
        "created",
    )
    search_fields = (
        "subject__username",
        "measurement",
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
                    "subject",
                    "measurement",
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


@admin.register(BodyWeight)
class BodyWeightAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `BodyWeight` model.
    """

    list_display = (
        "subject",
        "measurement",
        "created",
    )
    ordering = ("-created",)
    list_filter = (
        "subject",
        "created",
    )
    search_fields = (
        "subject__username",
        "measurement",
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
                    "subject",
                    "measurement",
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
