from django.test import TestCase
from django.db import models as d_db_models

from accounts.models import CustomUser
from cbt.models import CognativeDistortion
from cbt.models import Thought


COGNATIVE_DISTORTION_NAME = "cognative distortion name"
COGNATIVE_DISTORTION_DESCRIPTION = "cognative distortion description"

THOUGHT_NAME = "thought name"
THOUGHT_DESCRIPTION = "thought description"

TEST_USERNAME = "test_username"
TEST_PASSWORD = "test_password"
TEST_EMAIL = "test.username@email.app"

COGNATIVE_DISTORTION_NAME_LABEL = "Cognative Distortion"
COGNATIVE_DISTORTION_NAME_MAX_LENGTH = 150
COGNATIVE_DISTORTION_NAME_HELP_TEXT = "The name of the cognative distortion."

COGNATIVE_DISTORTION_DESCRIPTION_LABEL = "Description"
COGNATIVE_DISTORTION_DESCRIPTION_HELP_TEXT = (
    "The description of the cognative distortion."
)

COGNATIVE_DISTORTION_META_VERBOSE_NAME = "Cognative Distortion"
COGNATIVE_DISTORTION_META_VERBOSE_NAME_PLURAL = "Cognative Distortions"

THOUGHT_USER_LABEL = "user"
THOUGHT_USER_RELATED_NAME = "thoughts"
THOUGHT_USER_HELP_TEXT = "The user that has the thought."

THOUGHT_COGNATIVE_DISTORTION_RELATED_NAME = "thoughts"

THOUGHT_NAME_LABEL = "Summary"
THOUGHT_NAME_MAX_LENGTH = 250
THOUGHT_NAME_HELP_TEXT = "A summary of the thought."

THOUGHT_COGNATIVE_DISTORTION_LABEL = "cognative distortion"
THOUGHT_COGNATIVE_DISTORTION_RELATED_NAME = "thoughts"
THOUGHT_COGNATIVE_DISTORTION_HELP_TEXT = "The cognative distortion of the thought."

THOUGHT_DESCRIPTION_LABEL = "Description"
THOUGHT_DESCRIPTION_HELP_TEXT = "The description of the thought."

THOUGHT_META_VERBOSE_NAME = "Thought"
THOUGHT_META_VERBOSE_NAME_PLURAL = "Thoughts"


class CognativeDistortionModelTest(TestCase):
    """
    Tests for the CognativeDistortion model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase
        """
        cls.user = CustomUser.objects.create_user(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            email=TEST_EMAIL,
        )
        cls.cognative_distortion = CognativeDistortion.objects.create(
            name=COGNATIVE_DISTORTION_NAME,
            description=COGNATIVE_DISTORTION_DESCRIPTION,
        )

    def test_name_label(self):
        """
        Test that the name label is correct.
        """
        name_label = self.cognative_distortion._meta.get_field("name").verbose_name
        self.assertEqual(name_label, COGNATIVE_DISTORTION_NAME_LABEL)

    def test_name_max_length(self):
        """
        Test that the name max length is correct.
        """
        name_max_length = self.cognative_distortion._meta.get_field("name").max_length
        self.assertEqual(name_max_length, COGNATIVE_DISTORTION_NAME_MAX_LENGTH)

    def test_name_help_text(self):
        """
        Test that the name help text is correct.
        """
        name_help_text = self.cognative_distortion._meta.get_field("name").help_text
        self.assertEqual(name_help_text, COGNATIVE_DISTORTION_NAME_HELP_TEXT)

    def test_description_label(self):
        """
        Test that the description label is correct.
        """
        description_label = self.cognative_distortion._meta.get_field(
            "description"
        ).verbose_name
        self.assertEqual(description_label, COGNATIVE_DISTORTION_DESCRIPTION_LABEL)

    def test_description_help_text(self):
        """
        Test that the description help text is correct.
        """
        description_help_text = self.cognative_distortion._meta.get_field(
            "description"
        ).help_text
        self.assertEqual(
            description_help_text, COGNATIVE_DISTORTION_DESCRIPTION_HELP_TEXT
        )

    def test_dunder_string_method(self):
        """
        Test that the dunder str method is correct.
        """
        self.assertEqual(
            str(self.cognative_distortion),
            (
                f"{self.cognative_distortion.name} "
                f"--- "
                f"{self.cognative_distortion.description[:57] + '...' if len(self.cognative_distortion.description) > 57 else self.cognative_distortion.description}"
            ),
        )

    def test_meta_ordering(self):
        """
        Test that the meta ordering is correct.
        """
        self.assertEqual(self.cognative_distortion._meta.ordering, ["name"])

    def test_meta_verbose_name_plural(self):
        """
        Test that the meta verbose name plural is correct.
        """
        self.assertEqual(
            self.cognative_distortion._meta.verbose_name_plural,
            COGNATIVE_DISTORTION_META_VERBOSE_NAME_PLURAL,
        )

    def test_meta_verbose_name(self):
        """
        Test that the meta verbose name is correct.
        """
        self.assertEqual(
            self.cognative_distortion._meta.verbose_name,
            COGNATIVE_DISTORTION_META_VERBOSE_NAME,
        )


class ThoughtModelTest(TestCase):
    """
    Tests for the Thought model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase
        """
        cls.user = CustomUser.objects.create_user(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            email=TEST_EMAIL,
        )
        cls.cognative_distortion = CognativeDistortion.objects.create(
            name=COGNATIVE_DISTORTION_NAME,
            description=COGNATIVE_DISTORTION_DESCRIPTION,
        )
        cls.thought = Thought.objects.create(
            user=cls.user,
            cognative_distortion=cls.cognative_distortion,
            name=THOUGHT_NAME,
            description=THOUGHT_DESCRIPTION,
        )

    def test_user_label(self):
        """
        Test that the user label is correct.
        """
        user_label = self.thought._meta.get_field("user").verbose_name
        self.assertEqual(user_label, THOUGHT_USER_LABEL)

    def test_user_related_name(self):
        """
        Test that the `related_name` argument of the `Thought` model is set correctly.
        """
        # We created one thought and added it to the user, so the count
        # should be 1.
        self.assertEqual(self.user.thoughts.count(), 1)
        # We created one thought and added it to the user, so the first
        # thought should be the one we created.
        self.assertEqual(self.user.thoughts.first(), self.thought)

    def test_user_help_text(self):
        """
        Test that the user help text is correct.
        """
        user_help_text = self.thought._meta.get_field("user").help_text
        self.assertEqual(user_help_text, THOUGHT_USER_HELP_TEXT)

    def test_cognative_distortion_label(self):
        """
        Test that the cognative distortion label is correct.
        """
        cognative_distortion_label = self.thought._meta.get_field(
            "cognative_distortion"
        ).verbose_name
        self.assertEqual(cognative_distortion_label, THOUGHT_COGNATIVE_DISTORTION_LABEL)

    def test_cognative_distortion_help_text(self):
        """
        Test that the cognative distortion help text is correct.
        """
        cognative_distortion_help_text = self.thought._meta.get_field(
            "cognative_distortion"
        ).help_text
        self.assertEqual(
            cognative_distortion_help_text,
            THOUGHT_COGNATIVE_DISTORTION_HELP_TEXT,
        )

    def test_name_label(self):
        """
        Test that the name label is correct.
        """
        name_label = self.thought._meta.get_field("name").verbose_name
        self.assertEqual(name_label, THOUGHT_NAME_LABEL)

    def test_name_max_length(self):
        """
        Test that the name max length is correct.
        """
        name_max_length = self.thought._meta.get_field("name").max_length
        self.assertEqual(name_max_length, THOUGHT_NAME_MAX_LENGTH)

    def test_name_help_text(self):
        """
        Test that the name help text is correct.
        """
        name_help_text = self.thought._meta.get_field("name").help_text
        self.assertEqual(name_help_text, THOUGHT_NAME_HELP_TEXT)

    def test_description_label(self):
        """
        Test that the description label is correct.
        """
        description_label = self.thought._meta.get_field("description").verbose_name
        self.assertEqual(description_label, THOUGHT_DESCRIPTION_LABEL)

    def test_description_help_text(self):
        """
        Test that the description help text is correct.
        """
        description_help_text = self.thought._meta.get_field("description").help_text
        self.assertEqual(description_help_text, THOUGHT_DESCRIPTION_HELP_TEXT)

    def test_dunder_string_method(self):
        """
        Test that the dunder str method is correct.
        """
        self.assertEqual(
            str(self.thought),
            (f"{self.thought.user.username} | {self.thought.name}"),
        )

    def test_meta_ordering(self):
        """
        Test that the meta ordering is correct.
        """
        self.assertEqual(self.thought._meta.ordering, ["name"])

    def test_meta_verbose_name(self):
        """
        Test that the meta verbose name is correct.
        """
        self.assertEqual(self.thought._meta.verbose_name, THOUGHT_META_VERBOSE_NAME)

    def test_meta_verbose_name_plural(self):
        """
        Test that the meta verbose name plural is correct.
        """
        self.assertEqual(
            self.thought._meta.verbose_name_plural,
            THOUGHT_META_VERBOSE_NAME_PLURAL,
        )
