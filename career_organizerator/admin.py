from django.contrib import admin

from career_organizerator.models import (
    BehavioralInterviewQuestion,
    BulletPoint,
    ElevatorSpeech,
    Purpose,
    QuestionResponse,
    Skill,
)


@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel
    for the `Purpose` model.
    """

    list_display = (
        "truncated_text",
        "user",
        "created",
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

    def truncated_text(self, obj):
        """
        Truncate `text` to 50 characters.
        """
        return obj.text[:50]


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


@admin.register(BehavioralInterviewQuestion)
class BehavioralInterviewQuestionAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel
    for the `BehavioralInterviewQuestion` model.
    """

    list_display = (
        "truncated_text",
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

    def truncated_text(self, obj):
        """
        Truncate `text` to 30 characters.
        """
        return obj.text[:30]


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel
    for the `QuestionResponse` model.
    """

    list_display = (
        "truncated_text",
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
                    "question",
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

    def truncated_text(self, obj):
        """
        Truncate `text` to 30 characters.
        """
        return obj.text[:30]


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
