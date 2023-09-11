from django.contrib import admin
from django.test import TestCase, RequestFactory

from django.utils.translation import gettext_lazy as _

from app_tracker.admin import OrganizationalConceptAdmin
from app_tracker.admin import LanguageFrameworkSystemAdmin
from app_tracker.admin import ApplicationAdmin

from app_tracker.models import LanguageFrameworkSystem
from app_tracker.models import Application

from accounts.models import CustomUser


class OrganizationalConceptAdminTest(TestCase):
    """
    Test OrganizationalConceptAdmin
    """

    def test_list_display(self):
        self.assertEqual(
            OrganizationalConceptAdmin.list_display,
            (
                "name",
                "description",
                "applications_list",
                "created",
            ),
        )

    def test_ordering(self):
        self.assertEqual(OrganizationalConceptAdmin.ordering, ("-created",))

    def test_list_filter(self):
        self.assertEqual(
            OrganizationalConceptAdmin.list_filter,
            ("created",),
        )

    def test_search_fields(self):
        self.assertEqual(
            OrganizationalConceptAdmin.search_fields,
            (
                "name",
                "description",
            ),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            OrganizationalConceptAdmin.readonly_fields,
            (
                "created",
                "updated",
            ),
        )

    def test_fieldsets(self):
        self.assertEqual(
            OrganizationalConceptAdmin.fieldsets,
            (
                (
                    None,
                    {
                        "fields": (
                            "name",
                            "description",
                            "applications",
                        ),
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
            ),
        )


class LanguageFrameworkSystemAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@email.app",
            password="testpass",
        )
        self.lfs_01 = LanguageFrameworkSystem.objects.create(
            name="Python",
        )
        self.lfs_02 = LanguageFrameworkSystem.objects.create(
            name="Django",
        )
        self.admin = LanguageFrameworkSystemAdmin(
            LanguageFrameworkSystem, admin.site)

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            ("name", "created"),
        )

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ("-created",))

    def test_list_filter(self):
        self.assertEqual(
            self.admin.list_filter,
            ("created",),
        )

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            ("name",),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            self.admin.readonly_fields,
            ("created", "updated"),
        )

    def test_fieldsets(self):
        self.assertEqual(
            self.admin.fieldsets,
            (
                (
                    None,
                    {
                        "fields": ("name",),
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
            ),
        )


class ApplicationAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@email.app",
            password="testpass",
        )
        self.application_01 = (
            Application.objects.create(
                name="Big Django App",
                description="A big Django app.",
            ),
        )
        self.admin = ApplicationAdmin(Application, admin.site)

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            (
                "name",
                "repository_is_public",
                "language_framework_systems_list",
                "testing_level",
                "has_prod_deployment",
            ),
        )

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ("-created",))

    def test_list_filter(self):
        self.assertEqual(
            self.admin.list_filter,
            (
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
            ),
        )

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            (
                "name",
                "language_framework_systems__name",
            ),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            self.admin.readonly_fields,
            ("created", "updated"),
        )

    def test_fieldsets(self):
        self.assertEqual(
            self.admin.fieldsets,
            (
                (
                    _("General"),
                    {
                        "fields": (
                            "name",
                            "project",
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
                            "testing_level",
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
            ),
        )
