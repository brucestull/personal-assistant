from django.test import TestCase
from django.db import models as d_db_models

from career_organizerator.models import (
    BulletPoint,
    ElevatorSpeech,
)


BULLET_POINT_USER_VERBOSE_NAME = "User"
BULLET_POINT_USER_HELP_TEXT = "The user who created the bullet point."

BULLET_POINT_TEXT_VERBOSE_NAME = "Text"
BULLET_POINT_TEXT_HELP_TEXT = "The text of the bullet point."
BULLET_POINT_TEXT_MAX_LENGTH = 500

BULLET_POINT_VERBOSE_NAME_PLURAL = "Bullet Points"

ELEVATOR_SPEECH_USER_VERBOSE_NAME = "User"
ELEVATOR_SPEECH_USER_HELP_TEXT = "The user who created the elevator speech."

ELEVATOR_SPEECH_THEME_VERBOSE_NAME = "Theme"
ELEVATOR_SPEECH_THEME_HELP_TEXT = "The theme of the elevator speech."

ELEVATOR_SPEECH_BULLET_POINTS_VERBOSE_NAME = "Bullet Points"
ELEVATOR_SPEECH_BULLET_POINTS_HELP_TEXT = (
    "The bullet points that can be used in the elevator speech."
)

ELEVATOR_SPEECH_TEXT_VERBOSE_NAME = "Text"
ELEVATOR_SPEECH_TEXT_HELP_TEXT = "The text of the elevator speech."

ELEVATOR_SPEECH_VERBOSE_NAME_PLURAL = "Elevator Speeches"


TEST_USER_USERNAME = "test_user"
TEST_USER_PASSWORD = "test_password"

TEST_BULLET_POINT_TEXT = "test_text"

TEST_ELEVATOR_SPEECH_THEME = "test_theme"
TEST_ELEVATOR_SPEECH_TEXT = "test_text"


class BulletPointTestCase(TestCase):
    """
    Tests for the BulletPoint model.
    """

    def test_bullet_point_user_verbose_name(self):
        """
        Test that the verbose name of the user field is correct.
        """
        bullet_point_user_verbose_name = BulletPoint._meta.get_field(
            "user"
        ).verbose_name
        self.assertEqual(
            bullet_point_user_verbose_name,
            BULLET_POINT_USER_VERBOSE_NAME,
        )

    def test_bullet_point_user_help_text(self):
        """
        Test that the help text of the user field is correct.
        """
        bullet_point_user_help_text = BulletPoint._meta.get_field(
            "user"
        ).help_text
        self.assertEqual(
            bullet_point_user_help_text,
            BULLET_POINT_USER_HELP_TEXT,
        )

    def test_bullet_point_user_on_delete_is_cascade(self):
        """
        Test that the on_delete behavior of the user field is correct.
        """
        field = BulletPoint._meta.get_field("user")
        bullet_point_user_on_delete = field.remote_field.on_delete
        self.assertEqual(
            bullet_point_user_on_delete,
            d_db_models.CASCADE,
        )

    def test_bullet_point_text_verbose_name(self):
        """
        Test that the verbose name of the text field is correct.
        """
        bullet_point_text_verbose_name = BulletPoint._meta.get_field(
            "text"
        ).verbose_name
        self.assertEqual(
            bullet_point_text_verbose_name,
            BULLET_POINT_TEXT_VERBOSE_NAME,
        )

    def test_bullet_point_text_help_text(self):
        """
        Test that the help text of the text field is correct.
        """
        bullet_point_text_help_text = BulletPoint._meta.get_field(
            "text"
        ).help_text
        self.assertEqual(
            bullet_point_text_help_text,
            BULLET_POINT_TEXT_HELP_TEXT,
        )

    def test_bullet_point_text_max_length(self):
        """
        Test that the max length of the text field is correct.
        """
        bullet_point_text_max_length = BulletPoint._meta.get_field(
            "text"
        ).max_length
        self.assertEqual(
            bullet_point_text_max_length,
            BULLET_POINT_TEXT_MAX_LENGTH,
        )

