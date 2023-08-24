from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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
    Inherit from `admin.ModelAdmin` so we can customize the admin panel
    for the `Application` model.
    """

    # Items in the `list_display` attribute will be displayed as columns
    # in the admin panel.
    list_display = (
        "name",
        "repository_is_public",
        # We can use the `language_framework_systems_list` method, defined
        # below, to display the `LanguageFrameworkSystem` objects associated
        # with the `Application` object.
        "language_framework_systems_list",
        "testing_level",
        "has_prod_deployment",
    )
    # The `ordering` attribute will order the `Application` objects in the
    # admin panel.
    ordering = ("-created",)
    # The `list_filter` attribute will display filters in the admin panel.
    list_filter = (
        "language_framework_systems",
        "testing_level",
        "has_prod_deployment",
        "has_custom_user",
        "has_sticky_footer",
        "has_email_sending",
        "repository_is_public",
        "is_template_repository",
    )
    # The `search_fields` attribute will display a search bar in the admin
    # panel.
    # It will allow searching for `Application` objects by the `name` and
    # `language_framework_systems__name` fields.
    search_fields = (
        "name",
        "language_framework_systems__name",
    )
    # The `readonly_fields` attribute will make the `created` and `updated`
    # fields read-only in the admin panel.
    readonly_fields = (
        "created",
        "updated",
    )
    # The `fieldsets` attribute will group fields in the admin panel.
    # The first item in the tuple is the title of the fieldset.
    # The second item in the tuple is a dictionary of the fields in the
    # fieldset.
    fieldsets = (
        (
            _("General"),
            {
                "fields": (
                    "name",
                    "description",
                    "production_url",
                    "repository_url",
                    "reference_repository_url",
                    "project_board_url",
                    "is_favorite",
                ),
                "classes": ("wide", "extrapretty"),
            },
        ),
        (
            _("Language/Framework/Systems"),
            {
                "fields": ("language_framework_systems",),
                "classes": ("wide", "extrapretty"),
            },
        ),
        (
            _("Miscellaneous"),
            {
                "fields": (
                    (
                        "has_custom_user",
                        "has_sticky_footer",
                        "has_prod_deployment",
                    ),
                    (
                        "has_email_sending",
                        "repository_is_public",
                        "is_template_repository",
                    ),
                        "testing_level",
                ),
                "classes": ("wide", "extrapretty", "collapse"),
            },
        ),
        (
            _("Environment Settings"),
            {
                "fields": (
                    "settings_in_environment",
                    "settings_in_dot_env_file",
                    "settings_in_dot_yml_file",
                ),
                "classes": ("wide", "extrapretty", "collapse"),
                # "classes": ("wide", "extrapretty"),
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created",
                    "updated",
                ),
                "classes": ("wide", "extrapretty", "collapse"),
            },
        ),
    )

    def language_framework_systems_list(self, obj):
        """
        Return a list of the `LanguageFrameworkSystem` objects associated
        with the `Application` object.

        :param obj: The `Application` object.
        :return: A queryset of the `LanguageFrameworkSystem` objects associated
        with the `Application` object.
        """
        return list(obj.language_framework_systems.all())

    # Set the `short_description` attribute of the `language_framework_systems_list` method
    # to "Language Framework Systems" so that the `Language Framework Systems` column in the
    # admin panel will display "Language Framework Systems" instead of "Language Framework Systems List".
    language_framework_systems_list.short_description = "Languages-Frameworks-Systems"


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
