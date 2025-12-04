from unittest.mock import Mock, PropertyMock

from django.contrib import admin
from django.test import RequestFactory, TestCase
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser
from app_tracker.admin import (
    ApplicationAdmin,
    LabelAdmin,
    LanguageFrameworkSystemAdmin,
    OrganizationalConceptAdmin,
    ProjectAdmin,
)
from app_tracker.models import (
    Application,
    LanguageFrameworkSystem,
    OrganizationalConcept,
    Project,
)


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

    def test_date_hierarchy(self):
        self.assertEqual(OrganizationalConceptAdmin.date_hierarchy, "created")

    def test_search_fields(self):
        self.assertEqual(
            OrganizationalConceptAdmin.search_fields,
            (
                "name",
                "description",
                "applications__name",
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

    def test_filter_horizontal(self):
        self.assertEqual(
            OrganizationalConceptAdmin.filter_horizontal,
            ("applications",),
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

    def test_applications_list(self):
        """
        Tests for the 'applications_list' method using real objects.
        """
        app_01 = Application.objects.create(
            name="App 01",
            description="Description 01",
        )
        app_02 = Application.objects.create(
            name="App 02",
            description="Description 02",
        )
        app_03 = Application.objects.create(
            name="App 03",
            description="Description 03",
        )
        org_concept_01 = OrganizationalConcept.objects.create(
            name="Concept 01",
            description="Description 01",
        )
        org_concept_01.applications.add(app_01, app_02)
        org_concept_02 = OrganizationalConcept.objects.create(
            name="Concept 02",
            description="Description 02",
        )
        org_concept_02.applications.add(app_03)
        admin_instance = OrganizationalConceptAdmin(
            model=OrganizationalConcept, admin_site=None
        )

        result_01 = admin_instance.applications_list(obj=org_concept_01)
        self.assertIsInstance(result_01, str)
        self.assertIn("App 01", result_01)
        self.assertIn("App 02", result_01)
        self.assertNotIn("App 03", result_01)

        result_02 = admin_instance.applications_list(obj=org_concept_02)
        self.assertIsInstance(result_02, str)
        self.assertIn("App 03", result_02)
        self.assertNotIn("App 01", result_02)
        self.assertNotIn("App 02", result_02)

    def test_applications_list_mock(self):
        """
        Tests for the 'applications_list' method using a mock.
        """
        mock_obj = Mock()
        mock_applications = Mock()
        type(mock_obj).applications = PropertyMock(
            return_value=mock_applications,
        )

        mock_applications.values_list.return_value = [
            "App 1",
            "App 2",
            "App 3",
        ]

        admin_instance = OrganizationalConceptAdmin(
            model=OrganizationalConcept, admin_site=None
        )

        result = admin_instance.applications_list(obj=mock_obj)
        self.assertEqual(result, "App 1, App 2, App 3")


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
            LanguageFrameworkSystem,
            admin.site,
        )

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

    def test_date_hierarchy(self):
        self.assertEqual(self.admin.date_hierarchy, "created")

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


class ProjectAdminTest(TestCase):
    """
    Tests for 'ProjectAdmin'.
    """

    def test_list_display(self):
        self.assertEqual(
            ProjectAdmin.list_display,
            (
                "name",
                "owner_list",
                "application_list",
                "created",
            ),
        )

    def test_ordering(self):
        self.assertEqual(ProjectAdmin.ordering, ("-created",))

    def test_list_filter(self):
        self.assertEqual(
            ProjectAdmin.list_filter,
            (
                "owner__username",
                "created",
            ),
        )

    def test_date_hierarchy(self):
        self.assertEqual(ProjectAdmin.date_hierarchy, "created")

    def test_search_fields(self):
        self.assertEqual(
            ProjectAdmin.search_fields,
            (
                "name",
                "owner__username",
                "description",
                "applications__name",
            ),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            ProjectAdmin.readonly_fields,
            (
                "created",
                "updated",
            ),
        )

    def test_filter_horizontal(self):
        self.assertEqual(
            ProjectAdmin.filter_horizontal,
            ("owner", "applications"),
        )

    def test_fieldsets(self):
        self.assertEqual(
            ProjectAdmin.fieldsets,
            (
                (
                    None,
                    {
                        "fields": (
                            "name",
                            "owner",
                            "applications",
                            "description",
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

    def test_application_list_method(self):
        """
        Tests for the 'application_list' method using real objects.
        """
        app_01 = Application.objects.create(
            name="App 01",
            description="Description 01",
        )
        app_02 = Application.objects.create(
            name="App 02",
            description="Description 02",
        )
        app_03 = Application.objects.create(
            name="App 03",
            description="Description 03",
        )
        project_01 = Project.objects.create(
            name="Project 01",
            description="Description 01",
        )
        project_01.applications.add(app_01, app_02)
        project_02 = Project.objects.create(
            name="Project 02",
            description="Description 02",
        )
        project_02.applications.add(app_03)

        admin_instance = ProjectAdmin(model=Project, admin_site=None)

        result_01 = admin_instance.application_list(obj=project_01)
        self.assertIsInstance(result_01, str)
        self.assertIn("App 01", result_01)
        self.assertIn("App 02", result_01)
        self.assertNotIn("App 03", result_01)

        result_02 = admin_instance.application_list(obj=project_02)
        self.assertIsInstance(result_02, str)
        self.assertIn("App 03", result_02)
        self.assertNotIn("App 01", result_02)
        self.assertNotIn("App 02", result_02)

    def test_application_list_method_mock(self):
        """
        Tests for the 'application_list' method using a mock.
        """
        mock_obj = Mock()
        mock_applications = Mock()
        type(mock_obj).applications = PropertyMock(
            return_value=mock_applications,
        )

        mock_applications.values_list.return_value = ["app1", "app2", "app3"]

        admin_instance = ProjectAdmin(model=Project, admin_site=None)

        result = admin_instance.application_list(obj=mock_obj)
        self.assertEqual(result, "app1, app2, app3")

    def test_owner_list_method(self):
        """
        Tests for the 'owner_list' method using real objects.
        """
        user_dezzi_kitten = CustomUser.objects.create_user(
            username="DezziKitten",
            email="DezziKitten@purr.scratch",
            password="MeowMeow42",
        )
        user_zeus = CustomUser.objects.create_user(
            username="Zeus",
            email="Zeus@purr.scratch",
            password="MeowMeow42",
        )
        user_apollo = CustomUser.objects.create_user(
            username="Apollo",
            email="Apollo@purr.scratch",
            password="MeowMeow42",
        )
        project_01 = Project.objects.create(
            name="Project 01",
            description="Description 01",
        )
        project_01.owner.add(user_dezzi_kitten, user_zeus)
        project_02 = Project.objects.create(
            name="Project 02",
            description="Description 02",
        )
        project_02.owner.add(user_apollo)
        admin_instance = ProjectAdmin(model=Project, admin_site=None)

        result_01 = admin_instance.owner_list(obj=project_01)
        self.assertIsInstance(result_01, str)
        self.assertIn("DezziKitten", result_01)
        self.assertIn("Zeus", result_01)
        self.assertNotIn("Apollo", result_01)

        result_02 = admin_instance.owner_list(obj=project_02)
        self.assertIsInstance(result_02, str)
        self.assertIn("Apollo", result_02)
        self.assertNotIn("DezziKitten", result_02)
        self.assertNotIn("Zeus", result_02)


class ApplicationAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@email.app",
            password="testpass",
        )
        self.application_01 = Application.objects.create(
            name="Big Django App",
            description="A big Django app.",
        )
        self.admin = ApplicationAdmin(Application, admin.site)

    def test_list_display(self):
        self.assertEqual(
            self.admin.list_display,
            (
                "name",
                "language_framework_systems_list",
                "testing_level",
                "all_tests_passing",
                "has_prod_deployment",
                "has_cicd",
                "is_favorite",
            ),
        )

    def test_ordering(self):
        self.assertEqual(self.admin.ordering, ("-created",))

    def test_list_filter(self):
        self.assertEqual(
            self.admin.list_filter,
            (
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
            ),
        )

    def test_search_fields(self):
        self.assertEqual(
            self.admin.search_fields,
            (
                "name",
                "language_framework_systems__name",
                "project__name",
            ),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            self.admin.readonly_fields,
            ("created", "updated"),
        )

    def test_filter_horizontal(self):
        self.assertEqual(
            self.admin.filter_horizontal,
            ("project", "language_framework_systems"),
        )

    def test_date_hierarchy(self):
        self.assertEqual(self.admin.date_hierarchy, "created")

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

    def test_language_framework_systems_list_method(self):
        """
        Tests for the 'language_framework_systems_list' method using real
        objects.
        """
        lfs_01 = LanguageFrameworkSystem.objects.create(
            name="Python",
        )
        lfs_02 = LanguageFrameworkSystem.objects.create(
            name="Django",
        )
        lfs_03 = LanguageFrameworkSystem.objects.create(
            name="PostgreSQL",
        )
        app_01 = Application.objects.create(
            name="App 01",
            description="Description 01",
        )
        app_01.language_framework_systems.add(lfs_01, lfs_02)
        app_02 = Application.objects.create(
            name="App 02",
            description="Description 02",
        )
        app_02.language_framework_systems.add(lfs_03)
        admin_instance = ApplicationAdmin(model=Application, admin_site=None)

        result_01 = admin_instance.language_framework_systems_list(obj=app_01)
        self.assertIsInstance(result_01, str)
        self.assertIn("Python", result_01)
        self.assertIn("Django", result_01)
        self.assertNotIn("PostgreSQL", result_01)

        result_02 = admin_instance.language_framework_systems_list(obj=app_02)
        self.assertIsInstance(result_02, str)
        self.assertIn("PostgreSQL", result_02)
        self.assertNotIn("Python", result_02)
        self.assertNotIn("Django", result_02)

    def test_language_framework_systems_list_method_mock(self):
        """
        Tests for the 'language_framework_systems_list' method using a mock.
        """
        mock_obj = Mock()
        mock_language_framework_systems = Mock()
        type(mock_obj).language_framework_systems = PropertyMock(
            return_value=mock_language_framework_systems,
        )

        mock_language_framework_systems.values_list.return_value = [
            "lfs1",
            "lfs2",
            "lfs3",
        ]

        admin_instance = ApplicationAdmin(model=Application, admin_site=None)

        result = admin_instance.language_framework_systems_list(obj=mock_obj)
        self.assertEqual(result, "lfs1, lfs2, lfs3")


class LabelAdminTest(TestCase):
    def test_list_display(self):
        self.assertEqual(
            LabelAdmin.list_display,
            (
                "name",
                "hue",
                "description",
                "created",
            ),
        )

    def test_ordering(self):
        self.assertEqual(LabelAdmin.ordering, ("-created",))

    def test_list_filter(self):
        self.assertEqual(
            LabelAdmin.list_filter,
            (
                "application",
                "created",
            ),
        )

    def test_date_hierarchy(self):
        self.assertEqual(LabelAdmin.date_hierarchy, "created")

    def test_search_fields(self):
        self.assertEqual(
            LabelAdmin.search_fields,
            (
                "name",
                "description",
                "application__name",
            ),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            LabelAdmin.readonly_fields,
            (
                "created",
                "updated",
            ),
        )

    def test_filter_horizontal(self):
        self.assertEqual(
            LabelAdmin.filter_horizontal,
            ("application",),
        )

    def test_fieldsets(self):
        self.assertEqual(
            LabelAdmin.fieldsets,
            (
                (
                    None,
                    {
                        "fields": (
                            "name",
                            "hue",
                            "description",
                            "application",
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
