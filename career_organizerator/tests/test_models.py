from django.test import TestCase
from django.db import models as d_db_models

from django.contrib.auth import get_user_model

from career_organizerator.models import (
    BulletPoint,
    ElevatorSpeech,
)


class BulletPointTestCase(TestCase):
    """
    Tests for the BulletPoint model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the BulletPoint model.
        """
        cls.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        cls.bullet_point = BulletPoint.objects.create(
            user=cls.user,
            text="test_bullet_point_text",
        )

    def test_bullet_point_user_verbose_name(self):
        """
        Test that the verbose name of the user field is "User".
        """
        bullet_point_user_verbose_name = BulletPoint._meta.get_field(
            "user"
        ).verbose_name
        self.assertEqual(
            bullet_point_user_verbose_name,
            "User",
        )

    def test_bullet_point_user_help_text(self):
        """
        Test that the help text of the user field is "The user who created
        the bullet point.".
        """
        bullet_point_user_help_text = BulletPoint._meta.get_field(
            "user",
        ).help_text
        self.assertEqual(
            bullet_point_user_help_text,
            "The user who created the bullet point.",
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
            "Text",
        )

    def test_bullet_point_text_help_text(self):
        """
        Test that the help text of the text field is correct.
        """
        bullet_point_text_help_text = BulletPoint._meta.get_field(
            "text",
        ).help_text
        self.assertEqual(
            bullet_point_text_help_text,
            "The text of the bullet point.",
        )

    def test_bullet_point_text_max_length(self):
        """
        Test that the max length of the text field is correct.
        """
        bullet_point_text_max_length = BulletPoint._meta.get_field(
            "text",
        ).max_length
        self.assertEqual(
            bullet_point_text_max_length,
            500,
        )

    def test_bullet_point_dunder_string_method(self):
        """
        Test that the string representation of the BulletPoint model is
        correct.
        """
        bullet_point_dunder_string = str(self.bullet_point)
        self.assertEqual(
            bullet_point_dunder_string,
            "test_bullet_point_text",
        )

    def test_bullet_point_verbose_name_plural(self):
        """
        Test that the verbose name plural of the BulletPoint model is correct.
        """
        bullet_pt_verbose_name_plural = BulletPoint._meta.verbose_name_plural
        self.assertEqual(
            bullet_pt_verbose_name_plural,
            "Bullet Points",
        )


class ElevatorSpeechTestCase(TestCase):
    """
    Tests for the ElevatorSpeech model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the ElevatorSpeech model.
        """
        cls.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password",
        )
        cls.bullet_point = BulletPoint.objects.create(
            user=cls.user,
            text="test_bullet_point_text",
        )
        cls.elevator_speech = ElevatorSpeech.objects.create(
            user=cls.user,
            theme="test_elevator_speech_theme",
            text="test_elevator_speech_text",
        )

    def test_elevator_speech_user_verbose_name(self):
        """
        Test that the verbose name of the user field is "User".
        """
        elevator_speech_user_verbose_name = ElevatorSpeech._meta.get_field(
            "user"
        ).verbose_name
        self.assertEqual(
            elevator_speech_user_verbose_name,
            "User",
        )

    def test_elevator_speech_user_help_text(self):
        """
        Test that the help text of the user field is "The user who created the
        elevator speech.".
        """
        elevator_speech_user_help_text = ElevatorSpeech._meta.get_field(
            "user",
        ).help_text
        self.assertEqual(
            elevator_speech_user_help_text,
            "The user who created the elevator speech.",
        )

    def test_elevator_speech_user_on_delete_is_cascade(self):
        """
        Test that the on_delete behavior of the user field is "models.CASCADE".
        """
        field = ElevatorSpeech._meta.get_field("user")
        elevator_speech_user_on_delete = field.remote_field.on_delete
        self.assertEqual(
            elevator_speech_user_on_delete,
            d_db_models.CASCADE,
        )

    def test_elevator_speech_theme_verbose_name(self):
        """
        Test that the verbose name of the theme field is "Theme".
        """
        elevator_speech_theme_verbose_name = ElevatorSpeech._meta.get_field(
            "theme"
        ).verbose_name
        self.assertEqual(
            elevator_speech_theme_verbose_name,
            "Theme",
        )

    def test_elevator_speech_theme_help_text(self):
        """
        Test that the help text of the theme field is "The theme of the
        elevator speech.".
        """
        elevator_speech_theme_help_text = ElevatorSpeech._meta.get_field(
            "theme",
        ).help_text
        self.assertEqual(
            elevator_speech_theme_help_text,
            "The theme of the elevator speech.",
        )

    def test_elevator_speech_theme_max_length(self):
        """
        Test that the max length of the theme field is "255".
        """
        elevator_speech_theme_max_length = ElevatorSpeech._meta.get_field(
            "theme",
        ).max_length
        self.assertEqual(
            elevator_speech_theme_max_length,
            255,
        )

    def test_elevator_speech_bullet_points_verbose_name(self):
        """
        Test that the verbose name of the bullet_points field is "Bullet
        Points".
        """
        elevator_speech_bullet_points_verbose_name = (
            ElevatorSpeech._meta.get_field(
                "bullet_points"
            ).verbose_name
        )
        self.assertEqual(
            elevator_speech_bullet_points_verbose_name,
            "Bullet Points",
        )

    def test_elevator_speech_bullet_points_help_text(self):
        """
        Test that the help text of the bullet_points field is "The bullet
        points that can be used in the elevator speech.".
        """
        elevator_speech_bullet_points_help_text = (
            ElevatorSpeech._meta.get_field(
                "bullet_points",
            ).help_text
        )
        self.assertEqual(
            elevator_speech_bullet_points_help_text,
            "The bullet points that can be used in the elevator speech.",
        )

    def test_elevator_speech_bullet_points_related_model(self):
        """
        Test that the related model of the bullet_points field is
        "BulletPoint".
        """
        elevator_speech_bullet_points_related_model = (
            ElevatorSpeech._meta.get_field(
                "bullet_points",
            ).remote_field.model
        )
        self.assertEqual(
            elevator_speech_bullet_points_related_model,
            BulletPoint,
        )

    def test_elevator_speech_text_verbose_name(self):
        """
        Test that the verbose name of the text field is "Text".
        """
        elevator_speech_text_verbose_name = ElevatorSpeech._meta.get_field(
            "text"
        ).verbose_name
        self.assertEqual(
            elevator_speech_text_verbose_name,
            "Text",
        )

    def test_elevator_speech_text_help_text(self):
        """
        Test that the help text of the text field is "The text of the elevator
        speech.".
        """
        elevator_speech_text_help_text = ElevatorSpeech._meta.get_field(
            "text",
        ).help_text
        self.assertEqual(
            elevator_speech_text_help_text,
            "The text of the elevator speech.",
        )

    def test_elevator_speech_dunder_string_method(self):
        """
        Test that the string representation of the ElevatorSpeech model is
        "test_elevator_speech_theme".
        """
        elevator_speech_dunder_string = str(self.elevator_speech)
        self.assertEqual(
            elevator_speech_dunder_string,
            "test_elevator_speech_theme",
        )

    def test_elevator_speech_verbose_name_plural(self):
        """
        Test that the verbose name plural of the ElevatorSpeech model is
        "Elevator Speeches".
        """
        elevator_speech_verbose_name_plural = (
            ElevatorSpeech._meta.verbose_name_plural
        )
        self.assertEqual(
            elevator_speech_verbose_name_plural,
            "Elevator Speeches",
        )
