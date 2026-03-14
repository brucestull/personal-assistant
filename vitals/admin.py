# vitals/admin.py

from django.contrib import admin

from vitals.models import BloodPressure, BodyWeight, Pulse, Temperature


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
                    "note",
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
    list_display = ("subject", "measurement", "created")
    ordering = ("-created",)
    list_filter = ("subject", "created")
    search_fields = (
        "subject__username",
    )  # keep; 'measurement' is numeric—search may be odd
    readonly_fields = ("created", "updated")
    fieldsets = (
        (None, {"fields": ("subject", "measurement")}),
        ("Dates", {"fields": ("created", "updated")}),
    )

    # Performance: load related user in changelist
    list_select_related = ("subject",)

    # Nice UX for many users
    autocomplete_fields = ("subject",)

    # # Optional: if you want non-superusers in admin to only see their own records
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs if request.user.is_superuser else qs.filter(subject=request.user)

    # Optional: default subject to the admin user creating the record
    def save_model(self, request, obj, form, change):
        if not change and not obj.subject_id:
            obj.subject = request.user
        super().save_model(request, obj, form, change)
