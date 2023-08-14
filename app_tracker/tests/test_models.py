from django.test import TestCase

from app_tracker.models import DateTimeBase
from app_tracker.models import LanguageFrameworkSystem
from app_tracker.models import Application
from app_tracker.models import Note
from app_tracker.models import DjangoModel


DATE_TIME_BASE_CREATED_VERBOSE_NAME = "Created"
DATE_TIME_BASE_CREATED_HELP_TEXT = "The date and time this object was created."

DATE_TIME_BASE_UPDATED_VERBOSE_NAME = "Updated"
DATE_TIME_BASE_UPDATED_HELP_TEXT = "The date and time this object was last updated."

LANGUAGE_FRAMEWORK_SYSTEM_NAME_VERBOSE_NAME = "Name"
LANGUAGE_FRAMEWORK_SYSTEM_NAME_HELP_TEXT = (
    "The name of the language, framework, or system used in the application."
)
LANGUAGE_FRAMEWORK_SYSTEM_NAME_MAX_LENGTH = 30

LANGUAGE_FRAMEWORK_SYSTEM_VERBOSE_NAME_PLURAL = "Language/Framework/Systems"

APPLICATION_NAME_VERBOSE_NAME = "Name"
APPLICATION_NAME_HELP_TEXT = "The name of the application."
APPLICATION_NAME_MAX_LENGTH = 255

APPLICATION_DESCRIPTION_VERBOSE_NAME = "Description"
APPLICATION_DESCRIPTION_HELP_TEXT = "The description of the application."

APPLICATION_REPOSITORY_URL_VERBOSE_NAME = "Repository URL"
APPLICATION_REPOSITORY_URL_HELP_TEXT = "The URL of the application's repository."

APPLICATION_PRODUCTION_URL_VERBOSE_NAME = "Production URL"
APPLICATION_PRODUCTION_URL_HELP_TEXT = (
    "The URL of the application's production deployment."
)

APPLICATION_PROJECT_BOARD_URL_VERBOSE_NAME = "Project Board URL"
APPLICATION_PROJECT_BOARD_URL_HELP_TEXT = "The URL of the application's project board."

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

APPLICATION_HAS_EMAIL_SENDING_VERBOSE_NAME = "Email Sending"
APPLICATION_HAS_EMAIL_SENDING_HELP_TEXT = (
    "Whether or not the application has email sending capabilities."
)

APPLICATION_REPOSITORY_IS_PUBLIC_VERBOSE_NAME = "Repository is Public"
APPLICATION_REPOSITORY_IS_PUBLIC_HELP_TEXT = (
    "Whether or not the application's repository is public."
)

APPLICATION_TESTING_LEVEL_CHOICES = [
    ("high", "High"),
    ("medium", "Medium"),
    ("low", "Low"),
    ("none", "None"),
]

APPLICATION_TESTING_LEVEL_NAME = "Testing Level"
APPLICATION_TESTING_LEVEL_HELP_TEXT = (
    "The relative amount of testing coverage for the application."
)
APPLICATION_TESTING_LEVEL_MAX_LENGTH = 6

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

DJANGO_MODEL_NAME_VERBOSE_NAME = "name"
DJANGO_MODEL_NAME_HELP_TEXT = "The name of the Django model."
DJANGO_MODEL_NAME_MAX_LENGTH = 255

DJANGO_MODEL_DESCRIPTION_NAME = "description"
DJANGO_MODEL_DESCRIPTION_HELP_TEXT = "The description of the Django model."

DJANGO_MODEL_IS_CURRENT_MODEL_NAME = "is_current_model"
DJANGO_MODEL_IS_CURRENT_MODEL_HELP_TEXT = (
    (
        "'True' if this model is currently used in the application, "
        "'False' if this model is not currently used in the application."
    ),
)

DJANGO_MODEL_APPLICATION_NAME = "application"
DJANGO_MODEL_APPLICATION_RELATED_NAME = "django_models"


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

    def test_testing_level_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field("testing_level").verbose_name
        self.assertEquals(field_label, "testing level")

    def test_language_framework_systems_verbose_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        field_label = application._meta.get_field(
            "language_framework_systems"
        ).verbose_name
        self.assertEquals(field_label, "language framework systems")

    def test_object_name_is_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        expected_object_name = f"{application.name}"
        self.assertEquals(expected_object_name, str(application))

    def test_language_framework_systems_related_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        language_framework_system = LanguageFrameworkSystem.objects.get(id=1)
        application.language_framework_systems.add(language_framework_system)
        related_name = language_framework_system.applications.all()
        self.assertEquals(related_name.count(), 2)


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

    def test_object_name_is_title_and_application_name(self):
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
        self.assertEquals(field_label, "name")

    def test_name_max_length(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        max_length = django_model._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)

    def test_description_verbose_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        field_label = django_model._meta.get_field("description").verbose_name
        self.assertEquals(field_label, "description")

    def test_is_current_model_verbose_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        field_label = django_model._meta.get_field("is_current_model").verbose_name
        self.assertEquals(field_label, "is current model")

    def test_is_current_model_help_text(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        help_text = django_model._meta.get_field("is_current_model").help_text
        self.assertEquals(
            help_text,
            "'True' if this model is currently used in the application, 'False' if this model is not currently used in the application.",
        )

    def test_application_verbose_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        field_label = django_model._meta.get_field("application").verbose_name
        self.assertEquals(field_label, "application")

    def test_application_related_name(self):
        application = Application.objects.get(id=self.application_01.pk)
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        related_name = application.django_models.all()
        self.assertEquals(related_name.count(), 2)

    def test_object_name_is_name(self):
        django_model = DjangoModel.objects.get(id=self.django_model_01.pk)
        expected_object_name = django_model.name
        self.assertEquals(expected_object_name, str(django_model))
