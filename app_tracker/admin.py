# app_tracker/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app_tracker import models

# ---------------------------------------------------------------------------
# Inlines
# ---------------------------------------------------------------------------


class DjangoModelInline(admin.TabularInline):
    """
    Inline for DjangoModel on the Application admin.
    """

    model = models.DjangoModel
    extra = 1
    fields = ("name", "is_current_model")
    show_change_link = True


class NoteInline(admin.TabularInline):
    """
    Inline for Note on the Application admin.
    """

    model = models.Note
    extra = 1
    fields = ("title", "content")
    show_change_link = True


class URLInline(admin.TabularInline):
    """
    Inline for URL on the Application admin.
    """

    model = models.URL
    extra = 1
    fields = ("label", "url", "url_type")
    show_change_link = True


class SSHServerConnectionInline(admin.TabularInline):
    """
    Inline for SSHConnection where this host is the server.
    """

    model = models.SSHConnection
    fk_name = "server"
    extra = 1
    fields = ("client", "key_filename", "key_comment", "encryption_algorithm", "passphrase_protected")  # noqa: E501
    show_change_link = True
    verbose_name = "Incoming SSH Connection (client → this host)"
    verbose_name_plural = "Incoming SSH Connections (clients → this host)"


class SSHClientConnectionInline(admin.TabularInline):
    """
    Inline for SSHConnection where this host is the client.
    """

    model = models.SSHConnection
    fk_name = "client"
    extra = 1
    fields = ("server", "key_filename", "key_comment", "encryption_algorithm", "passphrase_protected")  # noqa: E501
    show_change_link = True
    verbose_name = "Outgoing SSH Connection (this host → server)"
    verbose_name_plural = "Outgoing SSH Connections (this host → servers)"


# ---------------------------------------------------------------------------
# Admin classes
# ---------------------------------------------------------------------------


@admin.register(models.OrganizationalConcept)
class OrganizationalConceptAdmin(admin.ModelAdmin):
    """
    Admin configuration for OrganizationalConcept.
    """

    list_display = (
        "name",
        "description",
        "applications_list",
        "created",
    )
    ordering = ("-created",)
    list_filter = ("created",)
    date_hierarchy = "created"
    search_fields = (
        "name",
        "description",
        "applications__name",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    filter_horizontal = ("applications",)
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
        Return a comma-separated list of associated Applications.
        """
        names = obj.applications.values_list("name", flat=True)
        return ", ".join(names) if names else "—"

    applications_list.short_description = "Application(s)"


@admin.register(models.LanguageFrameworkSystem)
class LanguageFrameworkSystemAdmin(admin.ModelAdmin):
    """
    Admin configuration for LanguageFrameworkSystem.
    """

    list_display = (
        "name",
        "created",
    )
    ordering = ("-created",)
    list_filter = ("created",)
    date_hierarchy = "created"
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


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for Project.
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
    date_hierarchy = "created"
    search_fields = (
        "name",
        "owner__username",
        "description",
        "applications__name",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    filter_horizontal = ("owner", "applications")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "owner",
                    "applications",
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
        Return a comma-separated list of Applications on this Project.
        """
        names = obj.applications.values_list("name", flat=True)
        return ", ".join(names) if names else "—"

    application_list.short_description = "Application(s)"

    def owner_list(self, obj):
        """
        Return a comma-separated list of Owners on this Project.
        """
        names = [str(owner) for owner in obj.owner.all()]
        return ", ".join(names) if names else "—"

    owner_list.short_description = "Owner(s)"


@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Application.
    """

    list_display = (
        "name",
        "language_framework_systems_list",
        "testing_level",
        "all_tests_passing",
        "has_prod_deployment",
        "has_cicd",
        "is_favorite",
        "is_pending_deployment",
    )
    ordering = ("-created",)
    list_filter = (
        "is_favorite",
        "is_pending_deployment",
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
    search_fields = (
        "name",
        "language_framework_systems__name",
        "project__name",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    filter_horizontal = ("project", "language_framework_systems")
    date_hierarchy = "created"
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
                        "is_pending_deployment",
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
    inlines = [DjangoModelInline, NoteInline, URLInline]

    def language_framework_systems_list(self, obj):
        """
        Return a comma-separated list of Language/Framework/Systems.
        """
        names = obj.language_framework_systems.values_list("name", flat=True)
        return ", ".join(names) if names else "—"

    language_framework_systems_list.short_description = "Languages/Frameworks/Systems"


@admin.register(models.Label)
class LabelAdmin(admin.ModelAdmin):
    """
    Admin configuration for Label.
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
    date_hierarchy = "created"
    search_fields = (
        "name",
        "description",
        "application__name",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    filter_horizontal = ("application",)
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


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Admin configuration for Note.
    """

    list_display = (
        "title",
        "application",
        "short_content",
        "created",
    )
    ordering = ("-created",)
    list_filter = (
        "application",
        "created",
    )
    date_hierarchy = "created"
    search_fields = (
        "title",
        "content",
        "application__name",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    autocomplete_fields = ("application",)
    list_select_related = ("application",)
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

    def short_content(self, obj):
        """
        Truncated note content for list display.
        """
        if not obj.content:
            return ""
        return (obj.content[:75] + "…") if len(obj.content) > 75 else obj.content

    short_content.short_description = "Content"


@admin.register(models.DjangoModel)
class DjangoModelAdmin(admin.ModelAdmin):
    """
    Admin configuration for DjangoModel.
    """

    list_display = (
        "name",
        "application",
        "is_current_model",
        "created",
    )
    ordering = ("-created",)
    list_filter = (
        "application",
        "is_current_model",
        "created",
    )
    date_hierarchy = "created"
    search_fields = (
        "name",
        "description",
        "application__name",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    autocomplete_fields = ("application",)
    list_select_related = ("application",)
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


@admin.register(models.OperatingSystem)
class OperatingSystemAdmin(admin.ModelAdmin):
    """
    Admin configuration for OperatingSystem.
    """

    search_fields = ["name", "code_name"]
    list_display = ["name", "code_name"]
    ordering = ["name"]


@admin.register(models.Host)
class HostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Host.
    """

    list_display = [
        "host_name",
        "ram",
        "form_factor",
        "ip_address",
        "status",
        "operating_system",
        "environment",
        "created",
    ]
    list_filter = ["status", "environment", "operating_system", "form_factor"]
    date_hierarchy = "created"
    search_fields = ["host_name", "ip_address", "notes", "name"]
    ordering = ["host_name"]
    autocomplete_fields = ["operating_system", "applications"]
    filter_horizontal = ["applications"]
    readonly_fields = ("created", "updated")
    list_select_related = ("operating_system",)
    actions = ["mark_as_active", "mark_as_paused", "mark_as_retired"]
    inlines = [SSHServerConnectionInline, SSHClientConnectionInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "operating_system",
                    "host_name",
                    "mac_address",
                    "ram",
                    "form_factor",
                    "ip_address",
                    "environment",
                    "notes",
                    "applications",
                )
            },
        ),
        (
            "Status",
            {
                "fields": ("status", "archived_at"),
            },
        ),
        (
            "Dates",
            {
                "fields": ("created", "updated"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.action(description="Mark selected hosts as Active")
    def mark_as_active(self, request, queryset):
        """
        Bulk action to mark hosts as ACTIVE.
        """
        updated = queryset.update(
            status=models.Host.HostStatus.ACTIVE, archived_at=None
        )
        self.message_user(
            request,
            f"{updated} host(s) marked as Active.",
        )

    @admin.action(description="Mark selected hosts as Paused")
    def mark_as_paused(self, request, queryset):
        """
        Bulk action to mark hosts as PAUSED.
        """
        from django.utils import timezone

        updated = queryset.update(
            status=models.Host.HostStatus.PAUSED, archived_at=timezone.now()
        )
        self.message_user(
            request,
            f"{updated} host(s) marked as Paused.",
        )

    @admin.action(description="Mark selected hosts as Retired")
    def mark_as_retired(self, request, queryset):
        """
        Bulk action to mark hosts as RETIRED.
        """
        from django.utils import timezone

        updated = queryset.update(
            status=models.Host.HostStatus.RETIRED, archived_at=timezone.now()
        )
        self.message_user(
            request,
            f"{updated} host(s) marked as Retired.",
        )


@admin.register(models.URL)
class URLAdmin(admin.ModelAdmin):
    """
    Admin configuration for the URL model.
    """

    list_display = (
        "label",
        "url_type",
        "application",
        "url",
        "created",
    )
    ordering = ("-created",)
    list_filter = (
        "url_type",
        "application",
        "created",
    )
    date_hierarchy = "created"
    search_fields = (
        "label",
        "url",
        "description",
        "application__name",
    )
    readonly_fields = (
        "created",
        "updated",
    )
    autocomplete_fields = ("application",)
    list_select_related = ("application",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "label",
                    "url",
                    "url_type",
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


@admin.register(models.SSHConnection)
class SSHConnectionAdmin(admin.ModelAdmin):
    """
    Admin configuration for SSHConnection.
    """

    list_display = (
        "server",
        "client",
        "encryption_algorithm",
        "key_filename",
        "key_comment",
        "passphrase_protected",
        "created",
    )
    list_filter = ("encryption_algorithm", "passphrase_protected")
    date_hierarchy = "created"
    search_fields = (
        "server__host_name",
        "client__host_name",
        "key_filename",
        "key_comment",
    )
    ordering = ("server", "client")
    autocomplete_fields = ("server", "client")
    readonly_fields = ("created", "updated")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "server",
                    "client",
                    "key_filename",
                    "key_comment",
                    "encryption_algorithm",
                    "passphrase_protected",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created",
                    "updated",
                ),
                "classes": ("collapse",),
            },
        ),
    )
