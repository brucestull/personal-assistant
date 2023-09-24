from django.contrib import admin
from unittest.mock import Mock, PropertyMock
from django.test import TestCase, RequestFactory

from django.utils.translation import gettext_lazy as _

from app_tracker.admin import (
    OrganizationalConceptAdmin,
    LanguageFrameworkSystemAdmin,
    ProjectAdmin,
    ApplicationAdmin,
    LabelAdmin,
)

from app_tracker.models import (
    OrganizationalConcept,
    LanguageFrameworkSystem,
    Project,
    Application,
)

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

    def test_applications_list(self):
        """
        Tests for the 'applications_list' method using real objects.
        """
        self.app_01 = Application.objects.create(
            name="App 01",
            description="Description 01",
        )
        self.app_02 = Application.objects.create(
            name="App 02",
            description="Description 02",
        )
        self.app_03 = Application.objects.create(
            name="App 03",
            description="Description 03",
        )
        self.org_concept_01 = OrganizationalConcept.objects.create(
            name="Concept 01",
            description="Description 01",
        )
        self.org_concept_01.applications.add(self.app_01, self.app_02)
        self.org_concept_02 = OrganizationalConcept.objects.create(
            name="Concept 02",
            description="Description 02",
        )
        self.org_concept_02.applications.add(self.app_03)
        admin_instance = OrganizationalConceptAdmin(
            model=OrganizationalConcept, admin_site=None
        )
        result_01 = admin_instance.applications_list(obj=self.org_concept_01)
        self.assertEqual(len(result_01), 2)
        self.assertIn(self.app_01, result_01)
        self.assertIn(self.app_02, result_01)
        self.assertNotIn(self.app_03, result_01)
        result_02 = admin_instance.applications_list(obj=self.org_concept_02)
        self.assertEqual(len(result_02), 1)
        self.assertIn(self.app_03, result_02)
        self.assertNotIn(self.app_01, result_02)

    def test_applications_list_mock(self):
        """
        Tests for the 'applications_list' method using a mock.
        """
        # Set up the mock
        mock_obj = Mock()
        mock_applications = Mock()
        type(mock_obj).applications = PropertyMock(
            return_value=mock_applications,
        )

        # Define the fake applications list
        fake_applications = ["app1", "app2", "app3"]
        mock_applications.all.return_value = fake_applications

        # Initialize your admin class
        admin_instance = OrganizationalConceptAdmin(
            model=OrganizationalConcept, admin_site=None
        )

        # Call the method and check the result
        result = admin_instance.applications_list(obj=mock_obj)
        self.assertEqual(result, fake_applications)


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

    def test_search_fields(self):
        self.assertEqual(
            ProjectAdmin.search_fields,
            (
                "name",
                "owner__username",
                "description",
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
        self.app_01 = Application.objects.create(
            name="App 01",
            description="Description 01",
        )
        self.app_02 = Application.objects.create(
            name="App 02",
            description="Description 02",
        )
        self.app_03 = Application.objects.create(
            name="App 03",
            description="Description 03",
        )
        self.project_01 = Project.objects.create(
            name="Project 01",
            description="Description 01",
        )
        self.project_01.applications.add(self.app_01, self.app_02)
        self.project_02 = Project.objects.create(
            name="Project 02",
            description="Description 02",
        )
        # Either of these two lines to relate project to application will work.
        # self.project_02.applications.add(self.app_03)
        # self.app_03.project.add(self.project_02)
        self.project_02.applications.add(self.app_03)
        admin_instance = ProjectAdmin(model=Project, admin_site=None)
        result_01 = admin_instance.application_list(obj=self.project_01)
        self.assertEqual(len(result_01), 2)
        self.assertIn(self.app_01, result_01)
        self.assertIn(self.app_02, result_01)
        self.assertNotIn(self.app_03, result_01)
        result_02 = admin_instance.application_list(obj=self.project_02)
        self.assertEqual(len(result_02), 1)
        self.assertIn(self.app_03, result_02)
        self.assertNotIn(self.app_01, result_02)

    def test_application_list_method_mock(self):
        """
        Tests for the 'application_list' method using a mock.
        """
        # Set up the mock
        mock_obj = Mock()
        mock_applications = Mock()
        type(mock_obj).applications = PropertyMock(
            return_value=mock_applications,
        )

        # Define the fake applications list
        fake_applications = ["app1", "app2", "app3"]
        mock_applications.all.return_value = fake_applications

        # Initialize your admin class
        admin_instance = ProjectAdmin(model=Project, admin_site=None)

        # Call the method and check the result
        result = admin_instance.application_list(obj=mock_obj)
        self.assertEqual(result, fake_applications)

    def test_owner_list_method(self):
        """
        Tests for the 'owner_list' method using real objects.
        """
        self.user_dezzi_kitten = CustomUser.objects.create_user(
            username="DezziKitten",
            email="DezziKitten@purr.scratch",
            password="MeowMeow42",
        )
        self.user_zeus = CustomUser.objects.create_user(
            username="Zeus",
            email="Zeus@purr.scratch",
            password="MeowMeow42",
        )
        self.user_apollo = CustomUser.objects.create_user(
            username="Apollo",
            email="Apollo@purr.scratch",
            password="MeowMeow42",
        )
        self.project_01 = Project.objects.create(
            name="Project 01",
            description="Description 01",
        )
        self.project_01.owner.add(self.user_dezzi_kitten, self.user_zeus)
        self.project_02 = Project.objects.create(
            name="Project 02",
            description="Description 02",
        )
        self.project_02.owner.add(self.user_apollo)
        admin_instance = ProjectAdmin(model=Project, admin_site=None)
        result_01 = admin_instance.owner_list(obj=self.project_01)
        self.assertEqual(len(result_01), 2)
        self.assertIn(self.user_dezzi_kitten, result_01)
        self.assertIn(self.user_zeus, result_01)
        self.assertNotIn(self.user_apollo, result_01)
        result_02 = admin_instance.owner_list(obj=self.project_02)
        self.assertEqual(len(result_02), 1)
        self.assertIn(self.user_apollo, result_02)
        self.assertNotIn(self.user_dezzi_kitten, result_02)


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
                "all_tests_passing",
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
        self.lfs_01 = LanguageFrameworkSystem.objects.create(
            name="Python",
        )
        self.lfs_02 = LanguageFrameworkSystem.objects.create(
            name="Django",
        )
        self.lfs_03 = LanguageFrameworkSystem.objects.create(
            name="PostgreSQL",
        )
        self.app_01 = Application.objects.create(
            name="App 01",
            description="Description 01",
        )
        self.app_01.language_framework_systems.add(self.lfs_01, self.lfs_02)
        self.app_02 = Application.objects.create(
            name="App 02",
            description="Description 02",
        )
        self.app_02.language_framework_systems.add(self.lfs_03)
        admin_instance = ApplicationAdmin(model=Application, admin_site=None)
        result_01 = admin_instance.language_framework_systems_list(
            obj=self.app_01,
        )
        self.assertEqual(len(result_01), 2)
        self.assertIn(self.lfs_01, result_01)
        self.assertIn(self.lfs_02, result_01)
        self.assertNotIn(self.lfs_03, result_01)
        result_02 = admin_instance.language_framework_systems_list(
            obj=self.app_02,
        )
        self.assertEqual(len(result_02), 1)
        self.assertIn(self.lfs_03, result_02)
        self.assertNotIn(self.lfs_01, result_02)

    def test_language_framework_systems_list_method_mock(self):
        """
        Tests for the 'language_framework_systems_list' method using a mock.
        """
        # Set up the mock
        mock_obj = Mock()
        mock_language_framework_systems = Mock()
        type(mock_obj).language_framework_systems = PropertyMock(
            return_value=mock_language_framework_systems,
        )

        # Define the fake language_framework_systems list
        fake_language_framework_systems = ["lfs1", "lfs2", "lfs3"]
        mock_language_framework_systems.all.return_value = (
            fake_language_framework_systems
        )

        # Initialize your admin class
        admin_instance = ApplicationAdmin(model=Application, admin_site=None)

        # Call the method and check the result
        result = admin_instance.language_framework_systems_list(obj=mock_obj)
        self.assertEqual(result, fake_language_framework_systems)


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

    def test_search_fields(self):
        self.assertEqual(
            LabelAdmin.search_fields,
            ("label__name",),
        )

    def test_readonly_fields(self):
        self.assertEqual(
            LabelAdmin.readonly_fields,
            (
                "created",
                "updated",
            ),
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
