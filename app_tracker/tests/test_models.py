from django.test import TestCase
from django.db import models as d_db_models

from app_tracker.models import (
    OrganizationalConcept,
    LanguageFrameworkSystem,
    Application,
    Note,
    DjangoModel,
)


DATE_TIME_BASE_CREATED_VERBOSE_NAME = "Created"
DATE_TIME_BASE_CREATED_HELP_TEXT = "The date and time this object was created."

DATE_TIME_BASE_UPDATED_VERBOSE_NAME = "Updated"
DATE_TIME_BASE_UPDATED_HELP_TEXT = "The date and time this object was last updated."

ORGANIZATIONAL_CONCEPT_NAME_VERBOSE_NAME = "Name"
ORGANIZATIONAL_CONCEPT_NAME_HELP_TEXT = "The name of the organizational concept."
ORGANIZATIONAL_CONCEPT_NAME_MAX_LENGTH = 50

ORGANIZATIONAL_CONCEPT_DESCRIPTION_VERBOSE_NAME = "Description"
ORGANIZATIONAL_CONCEPT_DESCRIPTION_HELP_TEXT = (
    "The description of the organizational concept."
)

ORGANIZATIONAL_CONCEPT_APPLICATIONS_VERBOSE_NAME = "Application(s)"
ORGANIZATIONAL_CONCEPT_APPLICATIONS_HELP_TEXT = (
    "The application(s) that the organizational concept is associated with."
)
ORGANIZATIONAL_CONCEPT_APPLICATIONS_RELATED_NAME = "organizational_concepts"

ORGANIZATIONAL_CONCEPT_META_VERBOSE_NAME = "Organizational Concept"
ORGANIZATIONAL_CONCEPT_META_VERBOSE_NAME_PLURAL = "Organizational Concepts"

LANGUAGE_FRAMEWORK_SYSTEM_NAME_VERBOSE_NAME = "Name"
LANGUAGE_FRAMEWORK_SYSTEM_NAME_HELP_TEXT = (
    "The name of the language, framework, or system used in the application."
)
LANGUAGE_FRAMEWORK_SYSTEM_NAME_MAX_LENGTH = 30

LANGUAGE_FRAMEWORK_SYSTEM_VERBOSE_NAME_PLURAL = "Language/Framework/Systems"

APPLICATION_PROJECT_VERBOSE_NAME = "Project"
APPLICATION_PROJECT_HELP_TEXT = (
    "The project(s) that the application is associated with."
)
APPLICATION_PROJECT_RELATED_NAME = "applications"

APPLICATION_NAME_VERBOSE_NAME = "Name"
APPLICATION_NAME_HELP_TEXT = "The name of the application."
APPLICATION_NAME_MAX_LENGTH = 255

APPLICATION_DESCRIPTION_VERBOSE_NAME = "Description"
APPLICATION_DESCRIPTION_HELP_TEXT = "The description of the application."

APPLICATION_PRODUCTION_URL_VERBOSE_NAME = "Production URL"
APPLICATION_PRODUCTION_URL_HELP_TEXT = (
    "The URL of the application's production deployment."
)

APPLICATION_REPOSITORY_URL_VERBOSE_NAME = "Repository URL"
APPLICATION_REPOSITORY_URL_HELP_TEXT = "The URL of the application's repository."

APPLICATION_REFERENCE_REPOSITORY_URL_VERBOSE_NAME = "Reference Repository URL"
APPLICATION_REFERENCE_REPOSITORY_URL_HELP_TEXT = (
    "The URL of the application's reference repository."
)

APPLICATION_IS_OFFICIAL_REPOSITORY_VERBOSE_NAME = "Is Official Repository"
APPLICATION_IS_OFFICIAL_REPOSITORY_HELP_TEXT = (
    "Whether or not the application is a repository for an official "
    "app maintained by some other organization."
)

APPLICATION_IS_ARCHIVE_REPOSITORY_VERBOSE_NAME = "Is Archive Repository"
APPLICATION_IS_ARCHIVE_REPOSITORY_HELP_TEXT = (
    "Whether or not the application is a repository for an archived "
    "app that is no longer maintained."
)

APPLICATION_PROJECT_BOARD_URL_VERBOSE_NAME = "Project Board URL"
APPLICATION_PROJECT_BOARD_URL_HELP_TEXT = "The URL of the application's project board."

APPLICATION_IS_FAVORITE_VERBOSE_NAME = "Is Favorite"
APPLICATION_IS_FAVORITE_HELP_TEXT = "Whether or not the application is a favorite."

APPLICATION_HAS_CUSTOM_USER_VERBOSE_NAME = "Has Custom User"
APPLICATION_HAS_CUSTOM_USER_HELP_TEXT = (
    "Whether or not the application has a custom user model."
)

APPLICATION_HAS_STICKY_FOOTER_VERBOSE_NAME = "Has Sticky Footer"
APPLICATION_HAS_STICKY_FOOTER_HELP_TEXT = (
    "Whether or not the application has a sticky footer."
)

APPLICATION_HAS_PROD_DEPLOYMENT_VERBOSE_NAME = "Has Production Deployment"
APPLICATION_HAS_PROD_DEPLOYMENT_HELP_TEXT = (
    "Whether or not the application has a production deployment."
)

APPLICATION_HAS_CICD_VERBOSE_NAME = "Has CI/CD"
APPLICATION_HAS_CICD_HELP_TEXT = (
    "Whether or not the application has CI/CD implemented."
)

APPLICATION_HAS_EMAIL_SENDING_VERBOSE_NAME = "Has Email Sending"
APPLICATION_HAS_EMAIL_SENDING_HELP_TEXT = (
    "Whether or not the application has email sending capabilities."
)

APPLICATION_REPOSITORY_IS_PUBLIC_VERBOSE_NAME = "Repository is Public"
APPLICATION_REPOSITORY_IS_PUBLIC_HELP_TEXT = (
    "Whether or not the application's repository is public."
)

APPLICATION_SETTINGS_IN_ENVIRONMENT_VERBOSE_NAME = "Settings in Environment"
APPLICATION_SETTINGS_IN_ENVIRONMENT_HELP_TEXT = (
    "Whether or not the application's settings are in the environment."
)

APPLICATION_SETTINGS_IN_DOT_ENV_FILE_VERBOSE_NAME = "Settings in Environment File"
APPLICATION_SETTINGS_IN_DOT_ENV_FILE_HELP_TEXT = (
    "Whether or not the application's settings are in an environment file."
)

APPLICATION_SETTINGS_IN_YML_FILE_VERBOSE_NAME = "Settings in YAML File"
APPLICATION_SETTINGS_IN_YML_FILE_HELP_TEXT = (
    "Whether or not the application's settings are in a YAML file."
)

APPLICATION_IS_TEMPLATE_REPOSITORY_VERBOSE_NAME = "Is Template Repository"
APPLICATION_IS_TEMPLATE_REPOSITORY_HELP_TEXT = (
    "Whether or not the application's repository is a template repository."
)

APPLICATION_TESTING_LEVEL_VERBOSE_NAME = "Testing Level"
APPLICATION_TESTING_LEVEL_HELP_TEXT = (
    "The relative amount of testing coverage for the application."
)
APPLICATION_TESTING_LEVEL_MAX_LENGTH = 6
APPLICATION_TESTING_LEVEL_CHOICES = [
    ("high", "High"),
    ("medium", "Medium"),
    ("low", "Low"),
    ("none", "None"),
]

APPLICATION_LANGUAGE_FRAMEWORK_SYSTEMS_VERBOSE_NAME = "Language/Framework/Systems"
APPLICATION_LANGUAGE_FRAMEWORK_SYSTEMS_HELP_TEXT = (
    "The languages, frameworks, and systems used in the application."
)
APPLICATION_LANGUAGE_FRAMEWORK_SYSTEMS_RELATED_NAME = "applications"

NOTE_TITLE_NAME = "title"
NOTE_TITLE_HELP_TEXT = "The title of the note."
NOTE_TITLE_MAX_LENGTH = 255

NOTE_CONTENT_VERBOSE_NAME = "content"
NOTE_CONTENT_HELP_TEXT = "The content of the note."

NOTE_APPLICATION_NAME = "application"
NOTE_APPLICATION_HELP_TEXT = "The application that the note is associated with."
NOTE_APPLICATION_RELATED_NAME = "notes"

DJANGO_MODEL_NAME_VERBOSE_NAME = "Name"
DJANGO_MODEL_NAME_HELP_TEXT = "The name of the Django model."
DJANGO_MODEL_NAME_MAX_LENGTH = 255

DJANGO_MODEL_DESCRIPTION_VERBOSE_NAME = "Description"
DJANGO_MODEL_DESCRIPTION_HELP_TEXT = "The description of the Django model."

DJANGO_MODEL_IS_CURRENT_MODEL_VERBOSE_NAME = "Is Current Model"
DJANGO_MODEL_IS_CURRENT_MODEL_HELP_TEXT = (
    "'True' if this model is currently used in the application, "
    "'False' if this model is not currently used in the application."
)

DJANGO_MODEL_APPLICATION_VERBOSE_NAME = "Application"
DJANGO_MODEL_APPLICATION_RELATED_NAME = "django_models"


TEST_ORGANIZATIONAL_CONCEPT_NAME_01 = "Organizational Concept Name One"
TEST_ORGANIZATIONAL_CONCEPT_NAME_02 = "Organizational Concept Name Two"

TEST_ORGANIZATIONAL_CONCEPT_DESCRIPTION_01 = "Organizational Concept Description One"
TEST_ORGANIZATIONAL_CONCEPT_DESCRIPTION_02 = "Organizational Concept Description Two"

TEST_LANGUAGE_FRAMEWORK_SYSTEM_NAME_01 = "Python"
TEST_LANGUAGE_FRAMEWORK_SYSTEM_NAME_02 = "Django"

TEST_APPLICATION_NAME_01 = "Personal Assistant"
TEST_APPLICATION_NAME_02 = "App Tracker"

TEST_APPLICATION_DESCRIPTION_01 = "A personal assistant application."
TEST_APPLICATION_DESCRIPTION_02 = "An application for tracking applications."

TEST_NOTE_TITLE_01 = "Note Title One"
TEST_NOTE_TITLE_02 = "Note Title Two"
TEST_NOTE_CONTENT_01 = "Note Content One"
TEST_NOTE_CONTENT_02 = "Note Content Two"

TEST_DJANGO_MODEL_NAME_01 = "Django Model Name One"
TEST_DJANGO_MODEL_NAME_02 = "Django Model Name Two"
TEST_DJANGO_MODEL_DESCRIPTION_01 = "Django Model Description One"
TEST_DJANGO_MODEL_DESCRIPTION_02 = "Django Model Description Two"


class OrganizationalConceptModelTest(TestCase):
    """
    Tests for the `OrganizationalConcept` model.
    """

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.organizational_concept_01 = OrganizationalConcept.objects.create(
            name=TEST_ORGANIZATIONAL_CONCEPT_NAME_01,
            description=TEST_ORGANIZATIONAL_CONCEPT_DESCRIPTION_01,
        )
        cls.organizational_concept_02 = OrganizationalConcept.objects.create(
            name=TEST_ORGANIZATIONAL_CONCEPT_NAME_02,
            description=TEST_ORGANIZATIONAL_CONCEPT_DESCRIPTION_02,
        )

    def test_name_verbose_name(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        field_label = organizational_concept._meta.get_field("name").verbose_name
        self.assertEquals(field_label, ORGANIZATIONAL_CONCEPT_NAME_VERBOSE_NAME)

    def test_name_help_text(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        help_text = organizational_concept._meta.get_field("name").help_text
        self.assertEquals(help_text, ORGANIZATIONAL_CONCEPT_NAME_HELP_TEXT)

    def test_name_max_length(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        max_length = organizational_concept._meta.get_field("name").max_length
        self.assertEquals(max_length, ORGANIZATIONAL_CONCEPT_NAME_MAX_LENGTH)

    def test_name_unique_true(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        unique = organizational_concept._meta.get_field("name").unique
        self.assertEquals(unique, True)

    def test_description_verbose_name(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        field_label = organizational_concept._meta.get_field("description").verbose_name
        self.assertEquals(field_label, ORGANIZATIONAL_CONCEPT_DESCRIPTION_VERBOSE_NAME)

    def test_description_help_text(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        help_text = organizational_concept._meta.get_field("description").help_text
        self.assertEquals(help_text, ORGANIZATIONAL_CONCEPT_DESCRIPTION_HELP_TEXT)

    def test_description_null_true(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        null = organizational_concept._meta.get_field("description").null
        self.assertEquals(null, True)

    def test_description_blank_true(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        blank = organizational_concept._meta.get_field("description").blank
        self.assertEquals(blank, True)

    def test_applications_uses_correct_model(self):
        """
        `applications` field should use the `Application` model.
        """
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        self.assertEquals(
            organizational_concept._meta.get_field("applications").related_model,
            Application,
        )

    def test_applications_verbose_name(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        field_label = organizational_concept._meta.get_field("applications").verbose_name
        self.assertEquals(field_label, ORGANIZATIONAL_CONCEPT_APPLICATIONS_VERBOSE_NAME)

    def test_applications_help_text(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        help_text = organizational_concept._meta.get_field("applications").help_text
        self.assertEquals(help_text, ORGANIZATIONAL_CONCEPT_APPLICATIONS_HELP_TEXT)

    def test_applications_blank_true(self):
        """
        `applications` field attribute `blank` attribute should be `True`.
        """
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        blank = organizational_concept._meta.get_field("applications").blank
        self.assertEquals(blank, True)

    def test_dunder_string_method(self):
        organizational_concept = OrganizationalConcept.objects.get(
            id=self.organizational_concept_01.pk
        )
        expected_object_name = f"{organizational_concept.name}"
        expected_dunder_string = f"{organizational_concept.name}{' - ' if organizational_concept.applications.all() else ''}{organizational_concept.applications.all() if organizational_concept.applications.all() else ''}"
        self.assertEquals(expected_dunder_string, str(organizational_concept))

    def test_meta_verbose_name(self):
        self.assertEquals(
            # str(OrganizationalConcept._meta.verbose_name),
            OrganizationalConcept._meta.verbose_name,
            ORGANIZATIONAL_CONCEPT_META_VERBOSE_NAME,
        )

    def test_meta_verbose_name_plural(self):
        self.assertEquals(
            # str(OrganizationalConcept._meta.verbose_name_plural),
            OrganizationalConcept._meta.verbose_name_plural,
            ORGANIZATIONAL_CONCEPT_META_VERBOSE_NAME_PLURAL,
        )


class LanguageFrameworkSystemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.lfs_01 = LanguageFrameworkSystem.objects.create(
            name=TEST_LANGUAGE_FRAMEWORK_SYSTEM_NAME_01
        )
        cls.lfs_02 = LanguageFrameworkSystem.objects.create(
            name=TEST_LANGUAGE_FRAMEWORK_SYSTEM_NAME_02
        )

    def test_name_verbose_name(self):
        language_framework_system = LanguageFrameworkSystem.objects.get(
            id=self.lfs_01.pk
        )
        field_label = language_framework_system._meta.get_field("name").verbose_name
        self.assertEquals(field_label, LANGUAGE_FRAMEWORK_SYSTEM_NAME_VERBOSE_NAME)

    def test_name_help_text(self):
        language_framework_system = LanguageFrameworkSystem.objects.get(
            id=self.lfs_01.pk
        )
        help_text = language_framework_system._meta.get_field("name").help_text
        self.assertEquals(help_text, LANGUAGE_FRAMEWORK_SYSTEM_NAME_HELP_TEXT)

    def test_name_max_length(self):
        language_framework_system = LanguageFrameworkSystem.objects.get(
            id=self.lfs_01.pk
        )
        max_length = language_framework_system._meta.get_field("name").max_length
        self.assertEquals(max_length, 30)

    def test_name_unique_true(self):
        language_framework_system = LanguageFrameworkSystem.objects.get(
            id=self.lfs_01.pk
        )
        unique = language_framework_system._meta.get_field("name").unique
        self.assertEquals(unique, True)

    def test_dunder_string_method(self):
        language_framework_system = LanguageFrameworkSystem.objects.get(
            id=self.lfs_01.pk
        )
        expected_object_name = f"{language_framework_system.name}"
        self.assertEquals(expected_object_name, str(language_framework_system))

    def test_meta_verbose_name_plural(self):
        self.assertEquals(
            # str(LanguageFrameworkSystem._meta.verbose_name_plural),
            LanguageFrameworkSystem._meta.verbose_name_plural,
            LANGUAGE_FRAMEWORK_SYSTEM_VERBOSE_NAME_PLURAL,
        )


class ApplicationModelTest(TestCase):
    """
    Tests for the `Application` model.
    """

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.lfs_01 = LanguageFrameworkSystem.objects.create(
            name=TEST_LANGUAGE_FRAMEWORK_SYSTEM_NAME_01,
        )
        cls.lfs_02 = LanguageFrameworkSystem.objects.create(
            name=TEST_LANGUAGE_FRAMEWORK_SYSTEM_NAME_02,
        )
        cls.application_01 = Application.objects.create(
            name=TEST_APPLICATION_NAME_01,
            description=TEST_APPLICATION_DESCRIPTION_01,
            has_custom_user=True,
            has_sticky_footer=False,
            has_prod_deployment=True,
            testing_level="high",
        )
        cls.application_01.language_framework_systems.add(cls.lfs_01)
        cls.application_02 = Application.objects.create(
            name=TEST_APPLICATION_NAME_02,
            description=TEST_APPLICATION_DESCRIPTION_02,
            has_custom_user=False,
            has_sticky_footer=True,
            has_prod_deployment=False,
            testing_level="medium",
        )
        cls.application_02.language_framework_systems.add(cls.lfs_01)

    def test_project_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("project").verbose_name
        self.assertEquals(field_label, APPLICATION_PROJECT_VERBOSE_NAME)

    def test_project_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("project").help_text
        self.assertEquals(help_text, APPLICATION_PROJECT_HELP_TEXT)

    def test_project_related_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        related_query_name = application._meta.get_field("project").related_query_name()
        self.assertEquals(related_query_name, APPLICATION_PROJECT_RELATED_NAME)

    def test_project_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("project").blank
        self.assertTrue(blank)

    def test_name_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("name").verbose_name
        self.assertEquals(field_label, APPLICATION_NAME_VERBOSE_NAME)

    def test_name_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("name").help_text
        self.assertEquals(help_text, APPLICATION_NAME_HELP_TEXT)

    def test_name_max_length(self):
        application = Application.objects.get(id=self.application_01.pk)
        max_length = application._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)

    def test_name_unique_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        unique = application._meta.get_field("name").unique
        self.assertEquals(unique, True)

    def test_description_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("description").verbose_name
        self.assertEquals(field_label, APPLICATION_DESCRIPTION_VERBOSE_NAME)

    def test_description_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("description").help_text
        self.assertEquals(help_text, APPLICATION_DESCRIPTION_HELP_TEXT)

    def test_description_null_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        null = application._meta.get_field("description").null
        self.assertEquals(null, True)

    def test_description_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("description").blank
        self.assertEquals(blank, True)

    def test_production_url_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("production_url").verbose_name
        self.assertEquals(field_label, APPLICATION_PRODUCTION_URL_VERBOSE_NAME)

    def test_production_url_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("production_url").help_text
        self.assertEquals(help_text, APPLICATION_PRODUCTION_URL_HELP_TEXT)

    def test_production_url_null_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        null = application._meta.get_field("production_url").null
        self.assertEquals(null, True)

    def test_production_url_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("production_url").blank
        self.assertEquals(blank, True)

    def test_repository_url_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("repository_url").verbose_name
        self.assertEquals(field_label, APPLICATION_REPOSITORY_URL_VERBOSE_NAME)

    def test_repository_url_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("repository_url").help_text
        self.assertEquals(help_text, APPLICATION_REPOSITORY_URL_HELP_TEXT)

    def test_repository_url_null_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        null = application._meta.get_field("repository_url").null
        self.assertEquals(null, True)

    def test_repository_url_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("repository_url").blank
        self.assertEquals(blank, True)

    def test_reference_repository_url_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "reference_repository_url"
        ).verbose_name
        self.assertEquals(
            field_label, APPLICATION_REFERENCE_REPOSITORY_URL_VERBOSE_NAME
        )

    def test_reference_repository_url_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("reference_repository_url").help_text
        self.assertEquals(help_text, APPLICATION_REFERENCE_REPOSITORY_URL_HELP_TEXT)

    def test_is_official_repository_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("is_official_repository").verbose_name
        self.assertEquals(field_label, APPLICATION_IS_OFFICIAL_REPOSITORY_VERBOSE_NAME)

    def test_is_official_repository_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("is_official_repository").help_text
        self.assertEquals(help_text, APPLICATION_IS_OFFICIAL_REPOSITORY_HELP_TEXT)

    def test_is_official_repository_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("is_official_repository").default
        self.assertFalse(default)

    def test_is_archive_repository_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("is_archive_repository").verbose_name
        self.assertEquals(field_label, APPLICATION_IS_ARCHIVE_REPOSITORY_VERBOSE_NAME)

    def test_is_archive_repository_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("is_archive_repository").help_text
        self.assertEquals(help_text, APPLICATION_IS_ARCHIVE_REPOSITORY_HELP_TEXT)

    def test_is_archive_repository_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("is_archive_repository").default
        self.assertFalse(default)

    def test_project_board_url_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("project_board_url").verbose_name
        self.assertEquals(field_label, APPLICATION_PROJECT_BOARD_URL_VERBOSE_NAME)

    def test_project_board_url_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("project_board_url").help_text
        self.assertEquals(help_text, APPLICATION_PROJECT_BOARD_URL_HELP_TEXT)

    def test_project_board_url_null_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        null = application._meta.get_field("project_board_url").null
        # NOTE: These two tests do the same thing:
        # self.assertEquals(null, True)
        # self.assertTrue(null)
        self.assertTrue(null)

    def test_project_board_url_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("project_board_url").blank
        self.assertTrue(blank)

    def test_is_favorite_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("is_favorite").verbose_name
        self.assertEquals(field_label, APPLICATION_IS_FAVORITE_VERBOSE_NAME)

    def test_is_favorite_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("is_favorite").help_text
        self.assertEquals(help_text, APPLICATION_IS_FAVORITE_HELP_TEXT)

    def test_is_favorite_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("is_favorite").default
        self.assertFalse(default)

    def test_has_custom_user_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("has_custom_user").verbose_name
        self.assertEquals(field_label, APPLICATION_HAS_CUSTOM_USER_VERBOSE_NAME)

    def test_has_custom_user_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("has_custom_user").help_text
        self.assertEquals(help_text, APPLICATION_HAS_CUSTOM_USER_HELP_TEXT)

    def test_has_custom_user_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_custom_user").default
        self.assertFalse(default)
        # NOTE: Alternatively:
        # self.assertEquals(default, False)

    def test_has_sticky_footer_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("has_sticky_footer").verbose_name
        self.assertEquals(field_label, APPLICATION_HAS_STICKY_FOOTER_VERBOSE_NAME)

    def test_has_sticky_footer_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("has_sticky_footer").help_text
        self.assertEquals(help_text, APPLICATION_HAS_STICKY_FOOTER_HELP_TEXT)

    def test_has_sticky_footer_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_sticky_footer").default
        self.assertFalse(default)

    def test_has_prod_deployment_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("has_prod_deployment").verbose_name
        self.assertEquals(field_label, APPLICATION_HAS_PROD_DEPLOYMENT_VERBOSE_NAME)

    def test_has_prod_deployment_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("has_prod_deployment").help_text
        self.assertEquals(help_text, APPLICATION_HAS_PROD_DEPLOYMENT_HELP_TEXT)

    def test_has_prod_deployment_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_prod_deployment").default
        self.assertFalse(default)

    def test_has_cicd_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("has_cicd").verbose_name
        self.assertEquals(field_label, APPLICATION_HAS_CICD_VERBOSE_NAME)

    def test_has_cicd_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("has_cicd").help_text
        self.assertEquals(help_text, APPLICATION_HAS_CICD_HELP_TEXT)

    def test_has_cicd_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_cicd").default
        self.assertFalse(default)

    def test_has_email_sending_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("has_email_sending").verbose_name
        self.assertEquals(field_label, APPLICATION_HAS_EMAIL_SENDING_VERBOSE_NAME)

    def test_has_email_sending_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("has_email_sending").help_text
        self.assertEquals(help_text, APPLICATION_HAS_EMAIL_SENDING_HELP_TEXT)

    def test_has_email_sending_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("has_email_sending").default
        self.assertFalse(default)

    def test_repository_is_public_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("repository_is_public").verbose_name
        self.assertEquals(field_label, APPLICATION_REPOSITORY_IS_PUBLIC_VERBOSE_NAME)

    def test_repository_is_public_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("repository_is_public").help_text
        self.assertEquals(help_text, APPLICATION_REPOSITORY_IS_PUBLIC_HELP_TEXT)

    def test_repository_is_public_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("repository_is_public").default
        self.assertFalse(default)

    def test_settings_in_environment_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "settings_in_environment"
        ).verbose_name
        self.assertEquals(field_label, APPLICATION_SETTINGS_IN_ENVIRONMENT_VERBOSE_NAME)

    def test_settings_in_environment_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("settings_in_environment").help_text
        self.assertEquals(help_text, APPLICATION_SETTINGS_IN_ENVIRONMENT_HELP_TEXT)

    def test_settings_in_environment_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("settings_in_environment").default
        self.assertFalse(default)

    def test_settings_in_dot_env_file_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "settings_in_dot_env_file"
        ).verbose_name
        self.assertEquals(
            field_label, APPLICATION_SETTINGS_IN_DOT_ENV_FILE_VERBOSE_NAME
        )

    def test_settings_in_dot_env_file_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("settings_in_dot_env_file").help_text
        self.assertEquals(help_text, APPLICATION_SETTINGS_IN_DOT_ENV_FILE_HELP_TEXT)

    def test_settings_in_dot_env_file_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("settings_in_dot_env_file").default
        self.assertFalse(default)

    def test_settings_in_dot_yml_file_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "settings_in_dot_yml_file"
        ).verbose_name
        self.assertEquals(field_label, APPLICATION_SETTINGS_IN_YML_FILE_VERBOSE_NAME)

    def test_settings_in_dot_yml_file_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("settings_in_dot_yml_file").help_text
        self.assertEquals(help_text, APPLICATION_SETTINGS_IN_YML_FILE_HELP_TEXT)

    def test_settings_in_dot_yml_file_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("settings_in_dot_yml_file").default
        self.assertFalse(default)

    def test_is_template_repository_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("is_template_repository").verbose_name
        self.assertEquals(field_label, APPLICATION_IS_TEMPLATE_REPOSITORY_VERBOSE_NAME)

    def test_is_template_repository_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("is_template_repository").help_text
        self.assertEquals(help_text, APPLICATION_IS_TEMPLATE_REPOSITORY_HELP_TEXT)

    def test_is_template_repository_default_false(self):
        application = Application.objects.get(id=self.application_01.pk)
        default = application._meta.get_field("is_template_repository").default
        self.assertFalse(default)

    def test_testing_level_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("testing_level").verbose_name
        self.assertEquals(field_label, APPLICATION_TESTING_LEVEL_VERBOSE_NAME)

    def test_testing_level_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("testing_level").help_text
        self.assertEquals(help_text, APPLICATION_TESTING_LEVEL_HELP_TEXT)

    def test_testing_level_max_length(self):
        application = Application.objects.get(id=self.application_01.pk)
        max_length = application._meta.get_field("testing_level").max_length
        self.assertEquals(max_length, APPLICATION_TESTING_LEVEL_MAX_LENGTH)

    def test_testing_level_choices_has_four_choices(self):
        application = Application.objects.get(id=self.application_01.pk)
        choices = application._meta.get_field("testing_level").choices
        self.assertEquals(len(choices), 4)

    def test_testing_level_choices_has_correct_choices(self):
        application = Application.objects.get(id=self.application_01.pk)
        choices = application._meta.get_field("testing_level").choices
        self.assertEquals(choices, APPLICATION_TESTING_LEVEL_CHOICES)

    def test_testing_level_null_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        null = application._meta.get_field("testing_level").null
        self.assertTrue(null)

    def test_testing_level_blank_true(self):
        application = Application.objects.get(id=self.application_01.pk)
        blank = application._meta.get_field("testing_level").blank
        self.assertTrue(blank)

    def test_language_framework_systems_uses_proper_model(self):
        application = Application.objects.get(id=self.application_01.pk)
        field = application._meta.get_field("language_framework_systems")
        self.assertEquals(field.related_model, LanguageFrameworkSystem)

    def test_language_framework_systems_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "language_framework_systems"
        ).verbose_name
        self.assertEquals(
            field_label, APPLICATION_LANGUAGE_FRAMEWORK_SYSTEMS_VERBOSE_NAME
        )

    def test_language_framework_systems_help_text(self):
        application = Application.objects.get(id=self.application_01.pk)
        help_text = application._meta.get_field("language_framework_systems").help_text
        self.assertEquals(help_text, APPLICATION_LANGUAGE_FRAMEWORK_SYSTEMS_HELP_TEXT)

    def test_language_framework_systems_related_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        related_name = application._meta.get_field(
            "language_framework_systems"
        ).related_query_name()
        self.assertEquals(
            related_name, APPLICATION_LANGUAGE_FRAMEWORK_SYSTEMS_RELATED_NAME
        )

    def test_language_framework_systems_dunder_string_method(self):
        application = Application.objects.get(id=self.application_01.pk)
        expected_object_name = application.name
        self.assertEquals(expected_object_name, str(application))


class NoteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.application_01 = Application.objects.create(
            name=TEST_APPLICATION_NAME_01,
            description=TEST_APPLICATION_DESCRIPTION_01,
            has_custom_user=True,
            has_sticky_footer=False,
            has_prod_deployment=True,
            testing_level="high",
        )
        cls.note_01 = Note.objects.create(
            title=TEST_NOTE_TITLE_01,
            content=TEST_NOTE_CONTENT_01,
            application=cls.application_01,
        )
        cls.note_02 = Note.objects.create(
            title=TEST_NOTE_TITLE_02,
            content=TEST_NOTE_CONTENT_02,
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
        self.assertEquals(field_label, "title")

    def test_title_max_length(self):
        note = Note.objects.get(id=self.note_01.pk)
        max_length = note._meta.get_field("title").max_length
        self.assertEquals(max_length, 255)

    def test_content_verbose_name(self):
        note = Note.objects.get(id=self.note_01.pk)
        field_label = note._meta.get_field("content").verbose_name
        self.assertEquals(field_label, "content")

    def test_application_verbose_name(self):
        note = Note.objects.get(id=self.note_01.pk)
        field_label = note._meta.get_field("application").verbose_name
        self.assertEquals(field_label, "application")

    def test_application_related_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        note = Note.objects.get(id=self.note_01.pk)
        related_name = application.notes.all()
        self.assertEquals(related_name.count(), 2)

    def test_dunder_string_method(self):
        note = Note.objects.get(id=self.note_01.pk)
        expected_object_name = f"{note.title} - {note.application.name}"
        self.assertEquals(expected_object_name, str(note))


class DjangoModelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.application_01 = Application.objects.create(
            name=TEST_APPLICATION_NAME_01,
            description=TEST_APPLICATION_DESCRIPTION_01,
            has_custom_user=True,
            has_sticky_footer=False,
            has_prod_deployment=True,
            testing_level="high",
        )
        cls.django_model_01 = DjangoModel.objects.create(
            name=TEST_DJANGO_MODEL_NAME_01,
            description=TEST_DJANGO_MODEL_DESCRIPTION_01,
            is_current_model=True,
            application=cls.application_01,
        )
        cls.django_model_02 = DjangoModel.objects.create(
            name=TEST_DJANGO_MODEL_NAME_02,
            description=TEST_DJANGO_MODEL_DESCRIPTION_02,
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
        self.assertEquals(field_label, DJANGO_MODEL_NAME_VERBOSE_NAME)

    def test_name_help_text(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        help_text = django_model._meta.get_field("name").help_text
        self.assertEquals(help_text, DJANGO_MODEL_NAME_HELP_TEXT)

    def test_name_max_length(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        max_length = django_model._meta.get_field("name").max_length
        self.assertEquals(max_length, DJANGO_MODEL_NAME_MAX_LENGTH)

    def test_name_unique_true(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        is_unique = django_model._meta.get_field("name").unique
        self.assertEquals(is_unique, True)
        self.assertTrue(is_unique)

    def test_name_max_length(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        max_length = django_model._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)

    def test_description_verbose_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        field_label = django_model._meta.get_field("description").verbose_name
        self.assertEquals(field_label, DJANGO_MODEL_DESCRIPTION_VERBOSE_NAME)

    def test_description_help_text(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        help_text = django_model._meta.get_field("description").help_text
        self.assertEquals(help_text, DJANGO_MODEL_DESCRIPTION_HELP_TEXT)

    def test_is_current_model_verbose_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        field_label = django_model._meta.get_field("is_current_model").verbose_name
        self.assertEquals(
            field_label,
            DJANGO_MODEL_IS_CURRENT_MODEL_VERBOSE_NAME,
        )

    def test_is_current_model_help_text(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        help_text = django_model._meta.get_field("is_current_model").help_text
        self.assertEquals(
            help_text,
            DJANGO_MODEL_IS_CURRENT_MODEL_HELP_TEXT,
        )

    def test_is_current_model_default_false(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        default = django_model._meta.get_field("is_current_model").default
        self.assertEquals(default, False)
        self.assertFalse(default)

    def test_application_verbose_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        field_label = django_model._meta.get_field("application").verbose_name
        self.assertEquals(field_label, DJANGO_MODEL_APPLICATION_VERBOSE_NAME)

    def test_application_on_delete_cascade(self):
        field = DjangoModel._meta.get_field("application")
        self.assertEqual(field.remote_field.on_delete, d_db_models.CASCADE)

    def test_application_related_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        related_name = application.django_models.all()
        self.assertEquals(related_name.count(), 2)

    def test_dunder_string_method(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        expected_object_name = django_model.name
        self.assertEquals(expected_object_name, str(django_model))
