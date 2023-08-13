from django.contrib import admin
from django.test import TestCase, RequestFactory
from django.urls import reverse

from app_tracker.admin import LanguageFrameworkSystemAdmin
from app_tracker.admin import ApplicationAdmin
from app_tracker.admin import NoteAdmin
from app_tracker.admin import DjangoModelAdmin

from app_tracker.models import LanguageFrameworkSystem
from app_tracker.models import Application
from app_tracker.models import Note
from app_tracker.models import DjangoModel

from accounts.models import CustomUser


class LanguageFrameworkSystemAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@email.app",
            password="testpass",
        )
        self.language_framework_system_01 = LanguageFrameworkSystem.objects.create(
            name="Python",
        )
        self.language_framework_system_02 = LanguageFrameworkSystem.objects.create(
            name="Django",
        )
        self.admin = LanguageFrameworkSystemAdmin(LanguageFrameworkSystem, admin.site)

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
                "language_framework_systems_list",
                "testing_level",
                "has_prod_deployment",
                "repository_is_public",
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
                "has_custom_user",
                "has_sticky_footer",
                "has_email_sending",
                "repository_is_public",
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
                    None,
                    {
                        "fields": (
                            "name",
                            "description",
                            "repository_url",
                            "language_framework_systems",
                            "repository_is_public",
                            "has_custom_user",
                            "has_sticky_footer",
                            "has_prod_deployment",
                            "has_email_sending",
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
            ),
        )
