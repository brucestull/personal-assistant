from django.contrib import admin

from career_organizerator.models import BulletPoint, ElevatorSpeech, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel
    for the `Skill` model.
    """

    list_display = (
        "name",
        "created",
        "user",
    )
    ordering = ("-created",)
    list_filter = ("created",)
    search_fields = (
        "name",
        "user__username",
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
                    "name",
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


@admin.register(BulletPoint)
class BulletPointAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel
    for the `BulletPoint` model.
    """

    list_display = (
        "text",
        "created",
        "user",
    )
    ordering = ("-created",)
    list_filter = ("created",)
    search_fields = (
        "text",
        "user__username",
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
                    "text",
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


@admin.register(ElevatorSpeech)
class ElevatorSpeechAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel
    for the `ElevatorSpeech` model.
    """

    list_display = (
        "theme",
        "created",
        "user",
    )
    ordering = ("-created",)
    list_filter = ("created",)
    search_fields = (
        "theme",
        "user__username",
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
                    "theme",
                    "text",
                    "bullet_points",
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
