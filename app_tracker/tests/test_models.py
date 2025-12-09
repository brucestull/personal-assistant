from django.db import models as d_db_models
from django.test import TestCase

from accounts.models import CustomUser
from app_tracker.models import (Application, DjangoModel, Host, Label,
                                LanguageFrameworkSystem, Note,
                                OrganizationalConcept, Project)


class OrganizationalConceptModelTest(TestCase):
    """
    Tests for the `OrganizationalConcept` model.
    """

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.organizational_concept_01 = OrganizationalConcept.objects.create(
            name="Organizational Concept Name One",
            description="Organizational Concept Description One",
        )
        cls.organizational_concept_02 = OrganizationalConcept.objects.create(
            name="Organizational Concept Name Two",
            description="Organizational Concept Description Two",
        )

    def test_name_verbose_name(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        field_label = organizational_concept._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Name")

    def test_name_help_text(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        help_text = organizational_concept._meta.get_field("name").help_text
        self.assertEqual(help_text, "The name of the organizational concept.")

    def test_name_max_length(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        max_length = organizational_concept._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    def test_name_unique_true(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        unique = organizational_concept._meta.get_field("name").unique
        self.assertEqual(unique, True)

    def test_description_verbose_name(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        field_label = organizational_concept._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "Description")

    def test_description_help_text(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        help_text = organizational_concept._meta.get_field("description").help_text
        self.assertEqual(help_text, "The description of the organizational concept.")

    def test_description_null_true(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        null = organizational_concept._meta.get_field("description").null
        self.assertEqual(null, True)

    def test_description_blank_true(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        blank = organizational_concept._meta.get_field("description").blank
        self.assertEqual(blank, True)

    def test_applications_uses_correct_model(self):
        """
        `applications` field should use the `Application` model.
        """
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        self.assertEqual(
            organizational_concept._meta.get_field("applications").related_model,
            Application,
        )

    def test_applications_verbose_name(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        field_label = organizational_concept._meta.get_field(
            "applications"
        ).verbose_name
        self.assertEqual(field_label, "Application(s)")

    def test_applications_help_text(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        help_text = organizational_concept._meta.get_field("applications").help_text
        self.assertEqual(
            help_text,
            "The application(s) that the organizational concept is associated with.",
        )

    def test_applications_blank_true(self):
        """
        `applications` field attribute `blank` attribute should be `True`.
        """
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        blank = organizational_concept._meta.get_field("applications").blank
        self.assertEqual(blank, True)

    def test_dunder_string_method(self):
        org_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        expected_dunder_string = (
            f"{org_concept.name} | Applications Count: "
            f"{org_concept.applications.count()}"
        )
        self.assertEqual(expected_dunder_string, str(org_concept))

    def test_meta_verbose_name(self):
        self.assertEqual(
            # str(OrganizationalConcept._meta.verbose_name),
            OrganizationalConcept._meta.verbose_name,
            "Organizational Concept",
        )

    def test_meta_verbose_name_plural(self):
        self.assertEqual(
            # str(OrganizationalConcept._meta.verbose_name_plural),
            OrganizationalConcept._meta.verbose_name_plural,
            "Organizational Concepts",
        )


class LanguageFrameworkSystemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.lfs_01 = LanguageFrameworkSystem.objects.create(name="Python")
        cls.lfs_02 = LanguageFrameworkSystem.objects.create(name="Django")

    def test_name_verbose_name(self):
        language_framework_system = LanguageFrameworkSystem.objects.get(
            id=self.lfs_01.pk
        )
        field_label = language_framework_system._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Name")

    def test_name_help_text(self):
        language_framework_system = LanguageFrameworkSystem.objects.get(
            id=self.lfs_01.pk
        )
        help_text = language_framework_system._meta.get_field("name").help_text
        self.assertEqual(
            help_text,
            "The name of the language, framework, or system used in the application.",
        )

    def test_name_max_length(self):
        language_framework_system = LanguageFrameworkSystem.objects.get(
            id=self.lfs_01.pk
        )
        max_length = language_framework_system._meta.get_field("name").max_length
        self.assertEqual(max_length, 30)

    def test_name_unique_true(self):
        language_framework_system = LanguageFrameworkSystem.objects.get(
            id=self.lfs_01.pk
        )
        unique = language_framework_system._meta.get_field("name").unique
        self.assertEqual(unique, True)

    def test_dunder_string_method(self):
        language_framework_system = LanguageFrameworkSystem.objects.get(
            id=self.lfs_01.pk
        )
        expected_object_name = f"{language_framework_system.name}"
        self.assertEqual(expected_object_name, str(language_framework_system))

    def test_meta_verbose_name_plural(self):
        self.assertEqual(
            # str(LanguageFrameworkSystem._meta.verbose_name_plural),
            LanguageFrameworkSystem._meta.verbose_name_plural,
            "Language/Framework/Systems",
        )


class ProjectModelTest(TestCase):
    """
    Tests for the `Project` model.
    """

    def test_name_verbose_name(self):
        field_verbose_name = Project._meta.get_field("name").verbose_name
        self.assertEqual(field_verbose_name, "Name")

    def test_name_help_text(self):
        field_help_text = Project._meta.get_field("name").help_text
        self.assertEqual(field_help_text, "The name of the project.")

    def test_name_max_length(self):
        field_max_length = Project._meta.get_field("name").max_length
        self.assertEqual(field_max_length, 255)

    def test_name_unique_true(self):
        field_unique = Project._meta.get_field("name").unique
        self.assertTrue(field_unique)

    def test_owner_uses_correct_model(self):
        """
        `owner` field should use the `User` model.
        """
        self.assertEqual(
            Project._meta.get_field("owner").related_model,
            CustomUser,
        )

    def test_owner_verbose_name(self):
        field_verbose_name = Project._meta.get_field("owner").verbose_name
        self.assertEqual(field_verbose_name, "Owner(s)")

    def test_owner_help_text(self):
        field_help_text = Project._meta.get_field("owner").help_text
        self.assertEqual(field_help_text, "The owner(s) of the project.")

    def test_owner_related_name(self):
        field_related_name = Project._meta.get_field("owner").related_query_name()
        self.assertEqual(field_related_name, "projects")

    def test_description_verbose_name(self):
        field_verbose_name = Project._meta.get_field("description").verbose_name
        self.assertEqual(field_verbose_name, "Description")

    def test_description_help_text(self):
        field_help_text = Project._meta.get_field("description").help_text
        self.assertEqual(field_help_text, "The description of the project.")

    def test_description_null_true(self):
        field_null = Project._meta.get_field("description").null
        self.assertTrue(field_null)

    def test_description_blank_true(self):
        field_blank = Project._meta.get_field("description").blank
        self.assertTrue(field_blank)

    def test_dunder_string_method(self):
        project = Project.objects.create(name="Project Name")
        expected_dunder_string = f"{project.name}"
        self.assertEqual(expected_dunder_string, str(project))


class ApplicationModelTest(TestCase):
    """
    Tests for the `Application` model.
    """

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.lfs_01 = LanguageFrameworkSystem.objects.create(
            name="Python",
        )
        cls.lfs_02 = LanguageFrameworkSystem.objects.create(
            name="Django",
        )
        cls.application_01 = Application.objects.create(
            name="Personal Assistant",
            description="A personal assistant application.",
            has_custom_user=True,
            has_sticky_footer=False,
            has_prod_deployment=True,
            testing_level="high",
        )
        cls.application_01.language_framework_systems.add(cls.lfs_01)
        cls.application_02 = Application.objects.create(
            name="App Tracker",
            description="An application for tracking applications.",
            has_custom_user=False,
            has_sticky_footer=True,
            has_prod_deployment=False,
            testing_level="medium",
        )
        cls.application_02.language_framework_systems.add(cls.lfs_01)

    def test_project_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("project").verbose_name
        self.assertEqual(field_label, "Project")

    def test_project_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("project").help_text
        self.assertEqual(
            help_text, "The project(s) that the application is associated with."
        )

    def test_project_related_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        related_query_name = application._meta.get_field("project").related_query_name()
        self.assertEqual(related_query_name, "applications")

    def test_project_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("project").blank
        self.assertTrue(blank)

    def test_name_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Name")

    def test_name_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("name").help_text
        self.assertEqual(help_text, "The name of the application.")

    def test_name_max_length(self):
        application = Application.objects.get(id=self.application_01.pk)
        max_length = application._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_name_unique_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        unique = application._meta.get_field("name").unique
        self.assertEqual(unique, True)

    def test_description_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "Description")

    def test_description_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("description").help_text
        self.assertEqual(help_text, "The description of the application.")

    def test_description_null_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        null = application._meta.get_field("description").null
        self.assertEqual(null, True)

    def test_description_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("description").blank
        self.assertEqual(blank, True)

    def test_production_url_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("production_url").verbose_name
        self.assertEqual(field_label, "Production URL")

    def test_production_url_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("production_url").help_text
        self.assertEqual(
            help_text, "The URL of the application's production deployment."
        )

    def test_production_url_null_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        null = application._meta.get_field("production_url").null
        self.assertEqual(null, True)

    def test_production_url_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("production_url").blank
        self.assertEqual(blank, True)

    def test_repository_url_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("repository_url").verbose_name
        self.assertEqual(field_label, "Repository URL")

    def test_repository_url_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("repository_url").help_text
        self.assertEqual(help_text, "The URL of the application's repository.")

    def test_repository_url_null_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        null = application._meta.get_field("repository_url").null
        self.assertEqual(null, True)

    def test_repository_url_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("repository_url").blank
        self.assertEqual(blank, True)

    def test_reference_repository_url_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "reference_repository_url"
        ).verbose_name
        self.assertEqual(field_label, "Reference Repository URL")

    def test_reference_repository_url_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("reference_repository_url").help_text
        self.assertEqual(
            help_text, "The URL of the application's reference repository."
        )

    def test_reference_url_field(self):
        """
        `reference_url` should have the following attributes and values:
        - `verbose_name` should be "Reference URL"
        - `help_text` should be "The URL of the application's reference."
        - `null` should be `True`
        - `blank` should be `True`
        """
        reference_url_field = Application._meta.get_field("reference_url")
        self.assertEqual(
            reference_url_field.verbose_name,
            "Reference URL",
        )
        self.assertEqual(
            reference_url_field.help_text,
            "The URL of the application's reference.",
        )
        self.assertTrue(reference_url_field.null)
        self.assertTrue(reference_url_field.blank)

    def test_is_official_repository_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("is_official_repository").verbose_name
        self.assertEqual(field_label, "Is Official Repository")

    def test_is_official_repository_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("is_official_repository").help_text
        self.assertEqual(
            help_text,
            "Whether or not the application is a repository for an official "
            "app maintained by some other organization.",
        )

    def test_is_official_repository_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("is_official_repository").default
        self.assertFalse(default)

    def test_is_adapted_repository(self):
        is_adapted_repository_field = Application._meta.get_field(
            "is_adapted_repository"
        )
        self.assertEqual(
            is_adapted_repository_field.verbose_name,
            "Is Adapted Repository",
        )
        self.assertEqual(
            is_adapted_repository_field.help_text,
            "Whether or not the application is a repository adapted from some "
            "other source.",
        )
        self.assertFalse(is_adapted_repository_field.default)

    def test_is_archive_repository_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("is_archive_repository").verbose_name
        self.assertEqual(field_label, "Is Archive Repository")

    def test_is_archive_repository_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("is_archive_repository").help_text
        self.assertEqual(
            help_text,
            "Whether or not the application is a repository for an archived "
            "app that is no longer maintained.",
        )

    def test_is_archive_repository_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("is_archive_repository").default
        self.assertFalse(default)

    def test_project_board_url_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("project_board_url").verbose_name
        self.assertEqual(field_label, "Project Board URL")

    def test_project_board_url_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("project_board_url").help_text
        self.assertEqual(help_text, "The URL of the application's project board.")

    def test_project_board_url_null_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        null = application._meta.get_field("project_board_url").null
        # NOTE: These two tests do the same thing:
        # self.assertEqual(null, True)
        # self.assertTrue(null)
        self.assertTrue(null)

    def test_project_board_url_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("project_board_url").blank
        self.assertTrue(blank)

    def test_is_favorite_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("is_favorite").verbose_name
        self.assertEqual(field_label, "Is Favorite")

    def test_is_favorite_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("is_favorite").help_text
        self.assertEqual(help_text, "Whether or not the application is a favorite.")

    def test_is_favorite_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("is_favorite").default
        self.assertFalse(default)

    def test_is_simple_example_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("is_simple_example").verbose_name
        self.assertEqual(field_label, "Is Simple Example")

    def test_is_simple_example_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("is_simple_example").help_text
        self.assertEqual(
            help_text, "Whether or not the application is a simple example."
        )

    def test_is_simple_example_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("is_simple_example").default
        self.assertFalse(default)

    def test_has_custom_user_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("has_custom_user").verbose_name
        self.assertEqual(field_label, "Has Custom User")

    def test_has_custom_user_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("has_custom_user").help_text
        self.assertEqual(
            help_text, "Whether or not the application has a custom user model."
        )

    def test_has_custom_user_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_custom_user").default
        self.assertFalse(default)
        # NOTE: Alternatively:
        # self.assertEqual(default, False)

    def test_has_sticky_footer_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("has_sticky_footer").verbose_name
        self.assertEqual(field_label, "Has Sticky Footer")

    def test_has_sticky_footer_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("has_sticky_footer").help_text
        self.assertEqual(
            help_text, "Whether or not the application has a sticky footer."
        )

    def test_has_sticky_footer_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_sticky_footer").default
        self.assertFalse(default)

    def test_has_prod_deployment_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("has_prod_deployment").verbose_name
        self.assertEqual(field_label, "Has Production Deployment")

    def test_has_prod_deployment_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("has_prod_deployment").help_text
        self.assertEqual(
            help_text, "Whether or not the application has a production deployment."
        )

    def test_has_prod_deployment_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_prod_deployment").default
        self.assertFalse(default)

    def test_has_cicd_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("has_cicd").verbose_name
        self.assertEqual(field_label, "Has CI/CD")

    def test_has_cicd_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("has_cicd").help_text
        self.assertEqual(
            help_text, "Whether or not the application has CI/CD implemented."
        )

    def test_has_cicd_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_cicd").default
        self.assertFalse(default)

    def test_has_email_sending_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("has_email_sending").verbose_name
        self.assertEqual(field_label, "Has Email Sending")

    def test_has_email_sending_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("has_email_sending").help_text
        self.assertEqual(
            help_text, "Whether or not the application has email sending capabilities."
        )

    def test_has_email_sending_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_email_sending").default
        self.assertFalse(default)

    def test_repository_is_public_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("repository_is_public").verbose_name
        self.assertEqual(field_label, "Repository is Public")

    def test_repository_is_public_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("repository_is_public").help_text
        self.assertEqual(
            help_text, "Whether or not the application's repository is public."
        )

    def test_repository_is_public_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("repository_is_public").default
        self.assertFalse(default)

    def test_settings_in_environment_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "settings_in_environment"
        ).verbose_name
        self.assertEqual(field_label, "Settings in Environment")

    def test_settings_in_environment_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("settings_in_environment").help_text
        self.assertEqual(
            help_text,
            "Whether or not the application's settings are in the environment.",
        )

    def test_settings_in_environment_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("settings_in_environment").default
        self.assertFalse(default)

    def test_settings_in_dot_env_file_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "settings_in_dot_env_file"
        ).verbose_name
        self.assertEqual(field_label, "Settings in Environment File")

    def test_settings_in_dot_env_file_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("settings_in_dot_env_file").help_text
        self.assertEqual(
            help_text,
            "Whether or not the application's settings are in an environment file.",
        )

    def test_settings_in_dot_env_file_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("settings_in_dot_env_file").default
        self.assertFalse(default)

    def test_settings_in_dot_yml_file_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "settings_in_dot_yml_file"
        ).verbose_name
        self.assertEqual(field_label, "Settings in YAML File")

    def test_settings_in_dot_yml_file_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("settings_in_dot_yml_file").help_text
        self.assertEqual(
            help_text, "Whether or not the application's settings are in a YAML file."
        )

    def test_settings_in_dot_yml_file_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("settings_in_dot_yml_file").default
        self.assertFalse(default)

    def test_is_template_repository_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("is_template_repository").verbose_name
        self.assertEqual(field_label, "Is Template Repository")

    def test_is_template_repository_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("is_template_repository").help_text
        self.assertEqual(
            help_text,
            "Whether or not the application's repository is a template repository.",
        )

    def test_is_template_repository_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("is_template_repository").default
        self.assertFalse(default)

    def test_is_pending_deployment_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("is_pending_deployment").verbose_name
        self.assertEqual(field_label, "Is Pending Deployment")

    def test_is_pending_deployment_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("is_pending_deployment").help_text
        self.assertEqual(
            help_text,
            "Whether or not the application is pending deployment to a server "
            "(e.g., packages like DuckDNS, Docker Engine, or Jenkins yet to be "
            "implemented on a server).",
        )

    def test_is_pending_deployment_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("is_pending_deployment").default
        self.assertFalse(default)

    def test_testing_level_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("testing_level").verbose_name
        self.assertEqual(field_label, "Testing Level")

    def test_testing_level_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("testing_level").help_text
        self.assertEqual(
            help_text, "The relative amount of testing coverage for the application."
        )

    def test_testing_level_max_length(self):
        application = Application.objects.get(id=self.application_01.pk)
        max_length = application._meta.get_field("testing_level").max_length
        self.assertEqual(max_length, 6)

    def test_testing_level_choices_has_four_choices(self):
        application = Application.objects.get(id=self.application_01.pk)
        choices = application._meta.get_field("testing_level").choices
        self.assertEqual(len(choices), 4)

    def test_testing_level_choices_has_correct_choices(self):
        application = Application.objects.get(id=self.application_01.pk)
        choices = application._meta.get_field("testing_level").choices
        self.assertEqual(
            choices,
            [
                ("high", "High"),
                ("medium", "Medium"),
                ("low", "Low"),
                ("none", "None"),
            ],
        )

    def test_testing_level_null_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        null = application._meta.get_field("testing_level").null
        self.assertTrue(null)

    def test_testing_level_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("testing_level").blank
        self.assertTrue(blank)

    def test_all_tests_passing_verbose_name(self):
        all_tests_passing_field = Application._meta.get_field("all_tests_passing")
        self.assertEqual(
            all_tests_passing_field.verbose_name,
            "All Tests Passing",
        )

    def test_all_tests_passing_help_text(self):
        all_tests_passing_field = Application._meta.get_field("all_tests_passing")
        self.assertEqual(
            all_tests_passing_field.help_text,
            "Whether or not all tests are passing.",
        )

    def test_all_tests_passing_default_false(self):
        all_tests_passing_field = Application._meta.get_field("all_tests_passing")
        self.assertFalse(all_tests_passing_field.default)

    def test_language_framework_systems_uses_proper_model(self):
        application = Application.objects.get(id=self.application_01.pk)
        field = application._meta.get_field("language_framework_systems")
        self.assertEqual(field.related_model, LanguageFrameworkSystem)

    def test_language_framework_systems_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "language_framework_systems"
        ).verbose_name
        self.assertEqual(field_label, "Language/Framework/Systems")

    def test_language_framework_systems_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("language_framework_systems").help_text
        self.assertEqual(
            help_text, "The languages, frameworks, and systems used in the application."
        )

    def test_language_framework_systems_related_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        related_name = application._meta.get_field(
            "language_framework_systems"
        ).related_query_name()
        self.assertEqual(related_name, "applications")

    def test_language_framework_systems_dunder_string_method(self):
        application = Application.objects.get(id=self.application_01.pk)
        expected_object_name = application.name
        self.assertEqual(expected_object_name, str(application))


class LabelModelTest(TestCase):
    """
    Tests for the `Label` model.
    """

    def test_name_field(self):
        """
        Name field should have the following properties:
        - verbose_name: "Name"
        - help_text: "The name of the label."
        - max_length: 50
        - unique: True
        """
        name_field = Label._meta.get_field("name")
        self.assertEqual(name_field.verbose_name, "Name")
        self.assertEqual(name_field.help_text, "The name of the label.")
        self.assertEqual(name_field.max_length, 50)
        self.assertEqual(name_field.unique, True)

    def test_hue_field(self):
        """
        Hue field should have the following properties:
        - verbose_name: "Hue"
        - help_text: "The color of the label tag (e.g. '#2BDCC7', '#FF0000',
        'ocre')."
        - max_length: 25
        - null: True
        - blank: True
        """
        hue_field = Label._meta.get_field("hue")
        self.assertEqual(hue_field.verbose_name, "Hue")
        self.assertEqual(
            hue_field.help_text,
            "The color of the label tag (e.g. '#2BDCC7', '#FF0000', 'ocre').",
        )
        self.assertEqual(hue_field.max_length, 25)
        self.assertTrue(hue_field.null)
        self.assertTrue(hue_field.blank)

    def test_description_field(self):
        """
        Description field should have the following properties:
        - verbose_name: "Description"
        - help_text: "The description of the label."
        - null: True
        - blank: True
        """
        description_field = Label._meta.get_field("description")
        self.assertEqual(description_field.verbose_name, "Description")
        self.assertEqual(description_field.help_text, "The description of the label.")
        self.assertTrue(description_field.null)
        self.assertTrue(description_field.blank)

    def test_application_field(self):
        """
        Application field should have the following properties:
        - verbose_name: "Application"
        - help_text: "The application to which the label belongs."
        - many_to_many: True
        - blank: True
        """
        application_field = Label._meta.get_field("application")
        self.assertEqual(
            application_field.verbose_name,
            "Application(s)",
        )
        self.assertEqual(
            application_field.help_text,
            ("The application(s) that the label is associated with."),
        )
        self.assertEqual(application_field.many_to_many, True)
        self.assertTrue(application_field.blank)

    def test_dunder_string_method(self):
        """
        The dunder string method should return the label's name.
        """
        label = Label.objects.create(
            name="Test Label",
            hue="#2BDCC7",
            description="This is a test label.",
        )
        self.assertEqual(str(label), "Test Label")


class NoteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.application_01 = Application.objects.create(
            name="Personal Assistant",
            description="A personal assistant application.",
            has_custom_user=True,
            has_sticky_footer=False,
            has_prod_deployment=True,
            testing_level="high",
        )
        cls.note_01 = Note.objects.create(
            title="Note Title One",
            content="Note Content One",
            application=cls.application_01,
        )
        cls.note_02 = Note.objects.create(
            title="Note Title Two",
            content="Note Content Two",
            application=cls.application_01,
        )
        # Add the two notes to the application
        cls.application_01.notes.add(
            cls.note_01,
            cls.note_02,
        )

    def test_title_verbose_name(self):
        note = Note.objects.get(id=self.note_01.pk)
        field_label = note._meta.get_field("title").verbose_name
        self.assertEqual(field_label, "title")

    def test_title_max_length(self):
        note = Note.objects.get(id=self.note_01.pk)
        max_length = note._meta.get_field("title").max_length
        self.assertEqual(max_length, 255)

    def test_content_verbose_name(self):
        note = Note.objects.get(id=self.note_01.pk)
        field_label = note._meta.get_field("content").verbose_name
        self.assertEqual(field_label, "content")

    def test_application_verbose_name(self):
        note = Note.objects.get(id=self.note_01.pk)
        field_label = note._meta.get_field("application").verbose_name
        self.assertEqual(field_label, "application")

    def test_application_related_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        related_name = application.notes.all()
        self.assertEqual(related_name.count(), 2)

    def test_dunder_string_method(self):
        note = Note.objects.get(id=self.note_01.pk)
        expected_object_name = f"{note.title} - {note.application.name}"
        self.assertEqual(expected_object_name, str(note))


class DjangoModelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.application_01 = Application.objects.create(
            name="Personal Assistant",
            description="A personal assistant application.",
            has_custom_user=True,
            has_sticky_footer=False,
            has_prod_deployment=True,
            testing_level="high",
        )
        cls.django_model_01 = DjangoModel.objects.create(
            name="Django Model Name One",
            description="Django Model Description One",
            is_current_model=True,
            application=cls.application_01,
        )
        cls.django_model_02 = DjangoModel.objects.create(
            name="Django Model Name Two",
            description="Django Model Description Two",
            is_current_model=False,
            application=cls.application_01,
        )
        # Add the two django models to the application
        cls.application_01.django_models.add(
            cls.django_model_01,
            cls.django_model_02,
        )

    def test_name_verbose_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        field_label = django_model._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Name")

    def test_name_help_text(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        help_text = django_model._meta.get_field("name").help_text
        self.assertEqual(help_text, "The name of the Django model.")

    def test_name_max_length(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        max_length = django_model._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_name_unique_true(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        is_unique = django_model._meta.get_field("name").unique
        self.assertEqual(is_unique, True)
        self.assertTrue(is_unique)

    def test_description_verbose_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        field_label = django_model._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "Description")

    def test_description_help_text(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        help_text = django_model._meta.get_field("description").help_text
        self.assertEqual(help_text, "The description of the Django model.")

    def test_is_current_model_verbose_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        field_label = django_model._meta.get_field("is_current_model").verbose_name
        self.assertEqual(
            field_label,
            "Is Current Model",
        )

    def test_is_current_model_help_text(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        help_text = django_model._meta.get_field("is_current_model").help_text
        self.assertEqual(
            help_text,
            "'True' if this model is currently used in the application, "
            "'False' if this model is not currently used in the application.",
        )

    def test_is_current_model_default_false(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        default = django_model._meta.get_field("is_current_model").default
        self.assertEqual(default, False)
        self.assertFalse(default)

    def test_application_verbose_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        field_label = django_model._meta.get_field("application").verbose_name
        self.assertEqual(field_label, "Application")

    def test_application_on_delete_cascade(self):
        field = DjangoModel._meta.get_field("application")
        self.assertEqual(field.remote_field.on_delete, d_db_models.CASCADE)

    def test_application_related_name(self):
        """
        This tests the related_name of the application field. Though we are
        not testing the model field option value directly, we are using the
        field option `related_name` of `django_models` to confirm the related
        name gets the realted objects.
        """
        application = Application.objects.get(id=self.application_01.pk)
        # An error would happen here if the related_name of `django_models`
        # was not set correctly.
        related_name = application.django_models.all()
        self.assertEqual(related_name.count(), 2)

    def test_dunder_string_method(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        expected_object_name = django_model.name
        self.assertEqual(expected_object_name, str(django_model))


class HostModelTest(TestCase):
    """
    Tests for the `Host` model.
    """

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.host_active = Host.objects.create(
            name="Active Host",
            host_name="active-host",
            ip_address="192.168.1.10",
            status=Host.HostStatus.ACTIVE,
        )
        cls.host_paused = Host.objects.create(
            name="Paused Host",
            host_name="paused-host",
            ip_address="192.168.1.20",
            status=Host.HostStatus.PAUSED,
        )
        cls.host_retired = Host.objects.create(
            name="Retired Host",
            host_name="retired-host",
            ip_address="192.168.1.30",
            status=Host.HostStatus.RETIRED,
        )

    def test_status_field_exists(self):
        """Test that the status field exists on the Host model."""
        host = Host.objects.get(id=self.host_active.pk)
        self.assertTrue(hasattr(host, "status"))

    def test_status_default_value(self):
        """Test that the status field defaults to ACTIVE."""
        host = Host.objects.create(
            name="Default Status Host",
            host_name="default-host",
            ip_address="192.168.1.40",
        )
        self.assertEqual(host.status, Host.HostStatus.ACTIVE)

    def test_status_verbose_name(self):
        """Test the verbose_name of the status field."""
        host = Host.objects.get(id=self.host_active.pk)
        field_label = host._meta.get_field("status").verbose_name
        self.assertEqual(field_label, "Status")

    def test_status_help_text(self):
        """Test the help_text of the status field."""
        host = Host.objects.get(id=self.host_active.pk)
        help_text = host._meta.get_field("status").help_text
        self.assertEqual(
            help_text, "The current status of the host (Active, Paused, or Retired)."
        )

    def test_status_max_length(self):
        """Test the max_length of the status field."""
        host = Host.objects.get(id=self.host_active.pk)
        max_length = host._meta.get_field("status").max_length
        self.assertEqual(max_length, 10)

    def test_status_choices(self):
        """Test that the status field has the correct choices."""
        host = Host.objects.get(id=self.host_active.pk)
        choices = host._meta.get_field("status").choices
        expected_choices = [
            ("ACTIVE", "Active"),
            ("PAUSED", "Paused"),
            ("RETIRED", "Retired"),
        ]
        self.assertEqual(list(choices), expected_choices)

    def test_archived_at_field_exists(self):
        """Test that the archived_at field exists on the Host model."""
        host = Host.objects.get(id=self.host_active.pk)
        self.assertTrue(hasattr(host, "archived_at"))

    def test_archived_at_verbose_name(self):
        """Test the verbose_name of the archived_at field."""
        host = Host.objects.get(id=self.host_active.pk)
        field_label = host._meta.get_field("archived_at").verbose_name
        self.assertEqual(field_label, "Archived At")

    def test_archived_at_help_text(self):
        """Test the help_text of the archived_at field."""
        host = Host.objects.get(id=self.host_active.pk)
        help_text = host._meta.get_field("archived_at").help_text
        self.assertEqual(
            help_text, "The date and time when the host was paused or retired."
        )

    def test_archived_at_null_true(self):
        """Test that the archived_at field allows null values."""
        host = Host.objects.get(id=self.host_active.pk)
        null = host._meta.get_field("archived_at").null
        self.assertEqual(null, True)

    def test_archived_at_blank_true(self):
        """Test that the archived_at field allows blank values."""
        host = Host.objects.get(id=self.host_active.pk)
        blank = host._meta.get_field("archived_at").blank
        self.assertEqual(blank, True)

    def test_visible_on_dashboard_returns_only_active(self):
        """Test that visible_on_dashboard() returns only ACTIVE hosts."""
        visible_hosts = Host.objects.visible_on_dashboard()
        self.assertEqual(visible_hosts.count(), 1)
        self.assertEqual(visible_hosts.first().status, Host.HostStatus.ACTIVE)

    def test_visible_on_dashboard_excludes_paused(self):
        """Test that visible_on_dashboard() excludes PAUSED hosts."""
        visible_hosts = Host.objects.visible_on_dashboard()
        paused_in_visible = visible_hosts.filter(status=Host.HostStatus.PAUSED)
        self.assertEqual(paused_in_visible.count(), 0)

    def test_visible_on_dashboard_excludes_retired(self):
        """Test that visible_on_dashboard() excludes RETIRED hosts."""
        visible_hosts = Host.objects.visible_on_dashboard()
        retired_in_visible = visible_hosts.filter(status=Host.HostStatus.RETIRED)
        self.assertEqual(retired_in_visible.count(), 0)

    def test_all_statuses_can_be_queried(self):
        """Test that all status types can be queried independently."""
        active_hosts = Host.objects.filter(status=Host.HostStatus.ACTIVE)
        paused_hosts = Host.objects.filter(status=Host.HostStatus.PAUSED)
        retired_hosts = Host.objects.filter(status=Host.HostStatus.RETIRED)

        self.assertEqual(active_hosts.count(), 1)
        self.assertEqual(paused_hosts.count(), 1)
        self.assertEqual(retired_hosts.count(), 1)

    def test_host_status_enum_values(self):
        """Test that HostStatus enum has correct values."""
        self.assertEqual(Host.HostStatus.ACTIVE, "ACTIVE")
        self.assertEqual(Host.HostStatus.PAUSED, "PAUSED")
        self.assertEqual(Host.HostStatus.RETIRED, "RETIRED")

    def test_host_status_enum_labels(self):
        """Test that HostStatus enum has correct labels."""
        self.assertEqual(Host.HostStatus.ACTIVE.label, "Active")
        self.assertEqual(Host.HostStatus.PAUSED.label, "Paused")
        self.assertEqual(Host.HostStatus.RETIRED.label, "Retired")
