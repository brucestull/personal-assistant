from django.contrib import admin

from app_tracker.models import LanguageFrameworkSystem
from app_tracker.models import Application
from app_tracker.models import Note
from app_tracker.models import DjangoModel


@admin.register(LanguageFrameworkSystem)
class LanguageFrameworkSystemAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for the `LanguageFrameworkSystem` model.
    """

    list_display = (
        "name",
        "created",
    )
    ordering = ("-created",)
    list_filter = ("created",)
    search_fields = ("name",)
    readonly_fields = (
        "created",
        "updated",
    )
    fieldsets = (
        (
            None,
            {"fields": ("name",)},
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


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for the `Application` model.
    """

    list_display = (
        "name",
        "created",
    )
    ordering = ("-created",)
    list_filter = ("created",)
    search_fields = ("name",)
    readonly_fields = (
        "created",
        "updated",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "repository_url",
                    "language_framework_systems",
                    "has_custom_user",
                    "has_sticky_footer",
                    "has_prod_deployment",
                    "testing_level",
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


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for the `Note` model.
    """

    list_display = (
        "title",
        "content",
        "application",
        "created",
    )
    ordering = ("-created",)
    list_filter = (
        "application",
        "created",
    )
    search_fields = ("application__name",)
    readonly_fields = (
        "created",
        "updated",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "content",
                    "application",
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


@admin.register(DjangoModel)
class DjangoModelAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for the `DjangoModel` model.
    """

    list_display = (
        "name",
        "is_current_model",
        "application",
    )
    ordering = ("-created",)
    list_filter = (
        "application",
        "created",
    )
    search_fields = ("application__name",)
    readonly_fields = (
        "created",
        "updated",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "is_current_model",
                    "application",
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
