from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app_tracker.models import (
    OrganizationalConcept,
    LanguageFrameworkSystem,
    Project,
    Application,
    Label,
    Note,
    DjangoModel,
)


@admin.register(OrganizationalConcept)
class OrganizationalConceptAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel
    for the `OrganizationalConcept` model.
    """

    list_display = (
        "name",
        "description",
        "applications_list",
        "created",
    )
    ordering = ("-created",)
    list_filter = ("created",)
    search_fields = (
        "name",
        "description",
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
                    "name",
                    "description",
                    "applications",
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

    def applications_list(self, obj):
        """
        Return a list of the `Application` objects associated with the
        `OrganizationalConcept` object.

        :param obj: The `OrganizationalConcept` object.
        :return: A queryset of the `Application` objects associated with the
        `OrganizationalConcept` object.
        """
        return list(obj.applications.all())

    applications_list.short_description = "Application(s)"


@admin.register(LanguageFrameworkSystem)
class LanguageFrameworkSystemAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `LanguageFrameworkSystem` model.
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


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `Project` model.
    """

    list_display = (
        "name",
        "owner_list",
        "application_list",
        "created",
    )
    ordering = ("-created",)
    list_filter = (
        "owner__username",
        "created",
    )
    search_fields = (
        "name",
        "owner__username",
        "description",
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
                    "name",
                    "owner",
                    "description",
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

    def application_list(self, obj):
        """
        Return a list of the `Application` objects associated with the
        `Project` object.

        :param obj: The `Project` object.
        :return: A queryset of the `Application` objects associated with
        the `Project` object.
        """
        return list(obj.applications.all())

    # Set the `short_description` attribute of the `application_list` method
    # to "Applications" so that the `Applications` column in the admin panel
    # will display "Applications" instead of "Application List".
    application_list.short_description = "Application(s)"

    def owner_list(self, obj):
        """
        Return a list of the `CustomUser` objects associated with the
        `Project` object.

        :param obj: The `Project` object.
        :return: A queryset of the `CustomUser` objects associated with the
        `Project` object.
        """
        return list(obj.owner.all())

    # Set the `short_description` attribute of the `owner_list` method
    # to "Owners" so that the `Owners` column in the admin panel
    # will display "Owners" instead of "Owner List".
    owner_list.short_description = "Owner(s)"


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
        # We can use the `language_framework_systems_list` method, defined
        # below, to display the `LanguageFrameworkSystem` objects associated
        # with the `Application` object.
        "language_framework_systems_list",
        "all_tests_passing",
        "testing_level",
        "has_prod_deployment",
    )
    # The `ordering` attribute will order the `Application` objects in the
    # admin panel.
    ordering = ("-created",)
    # The `list_filter` attribute will display filters in the admin panel.
    list_filter = (
        "is_favorite",
        "language_framework_systems",
        "testing_level",
        "has_prod_deployment",
        "has_cicd",
        "is_simple_example",
        "has_custom_user",
        "has_sticky_footer",
        "has_email_sending",
        "repository_is_public",
        "is_template_repository",
        "is_official_repository",
        "is_archive_repository",
        "settings_in_environment",
        "settings_in_dot_env_file",
        "settings_in_dot_yml_file",
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
                    "project",
                    "description",
                    "production_url",
                    "repository_url",
                    "reference_url",
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
                        "testing_level",
                        "all_tests_passing",
                    ),
                    (
                        "has_custom_user",
                        "has_sticky_footer",
                        "has_prod_deployment",
                        "has_email_sending",
                    ),
                    (
                        "has_cicd",
                        "is_simple_example",
                    ),
                    (
                        "repository_is_public",
                        "is_template_repository",
                    ),
                    (
                        "is_official_repository",
                        "is_adapted_repository",
                        "is_archive_repository",
                    ),
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
        :return: A queryset of the `LanguageFrameworkSystem` objects
        associated with the `Application` object.
        """
        return list(obj.language_framework_systems.all())

    # Set the `short_description` attribute of the
    # `language_framework_systems_list` method to "Language Framework Systems"
    # so that the `Language Framework Systems` column in the admin panel will
    # display "Language Framework Systems" instead of
    # "Language Framework Systems List".
    language_framework_systems_list.short_description = (
        "Languages-Frameworks-Systems"
    )


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `Label` model.
    """

    list_display = (
        "name",
        "hue",
        "description",
        "created",
    )
    ordering = ("-created",)
    list_filter = (
        "application",
        "created",
    )
    search_fields = ("label__name",)
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
                    "hue",
                    "description",
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


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `Note` model.
    """

    list_display = (
        "title",
        "application",
        "content",
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
    Inherit from `admin.ModelAdmin` so we can customize the admin panel for
    the `DjangoModel` model.
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
