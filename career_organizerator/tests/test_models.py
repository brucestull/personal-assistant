from django.contrib.auth import get_user_model
from django.db import models as d_db_models
from django.test import TestCase

from career_organizerator.models import (
    BehavioralInterviewQuestion,
    BulletPoint,
    ElevatorSpeech,
    Purpose,
    QuestionResponse,
    Skill,
)


class PurposeTestCase(TestCase):
    """
    Tests for the Purpose model.
    """

    def test_model_exists_and_has_proper_attributes(self):
        """
        Tests for the `Purpose` model.
        """
        # Test that the `Purpose` model exists.
        self.assertIsNotNone(Purpose)
        # Test that the `Purpose` model is a subclass of `models.Model`.
        self.assertTrue(issubclass(Purpose, d_db_models.Model))
        # Test that the `Purpose` model has a `user` field.
        self.assertTrue(hasattr(Purpose, "user"))
        # Test that the `Purpose` model has a `text` field.
        self.assertTrue(hasattr(Purpose, "text"))
        # Test that the `Purpose` model has a `__str__` method.
        self.assertTrue(hasattr(Purpose, "__str__"))
        # Test that the `Purpose` model has a `Meta` class.
        self.assertTrue(hasattr(Purpose, "Meta"))

    def test_user_field(self):
        """
        Tests for the `Purpose` model `user` field.
        """
        # Test that `user` field uses the proper user model.
        purpose_user_model = Purpose._meta.get_field("user").remote_field.model
        self.assertEqual(
            purpose_user_model,
            get_user_model(),
        )
        # Test that the `user` field has the correct verbose name of "User".
        purpose_user_verbose_name = Purpose._meta.get_field("user").verbose_name
        self.assertEqual(
            purpose_user_verbose_name,
            "User",
        )
        # Test that the `user` field has the correct help text of "The user who
        # created the purpose.".
        purpose_user_help_text = Purpose._meta.get_field("user").help_text
        self.assertEqual(
            purpose_user_help_text,
            "The user who created the purpose.",
        )
        # Test that the `user` field has the correct on_delete behavior of
        # "models.CASCADE".
        field = Purpose._meta.get_field("user")
        purpose_user_on_delete = field.remote_field.on_delete
        self.assertEqual(
            purpose_user_on_delete,
            d_db_models.CASCADE,
        )

    def test_text_field(self):
        """
        Tests for the `Purpose` model `text` field.
        """
        # Test that the `text` field has the correct verbose name of "Text".
        purpose_text_verbose_name = Purpose._meta.get_field("text").verbose_name
        self.assertEqual(
            purpose_text_verbose_name,
            "Text",
        )
        # Test that the `text` field has the correct help text of "The text of
        # the purpose.".
        purpose_text_help_text = Purpose._meta.get_field("text").help_text
        self.assertEqual(
            purpose_text_help_text,
            "The text of the purpose.",
        )
        # Test that the `text` field has the correct max length of "500".
        purpose_text_max_length = Purpose._meta.get_field("text").max_length
        self.assertEqual(
            purpose_text_max_length,
            500,
        )

    def test_dunder_string_method(self):
        """
        Tests for the `Purpose` model `__str__` method.
        """
        # Create a `Customuser` object.
        self.user = get_user_model().objects.create_user(
            username="BunbunKitten",
            password="MeowMeow42",
        )
        # Create a `Purpose` object.
        self.user_purpose = Purpose.objects.create(
            user=self.user,
            text="A Test Purpose Text",
        )
        # Test that the `__str__` method returns the correct string
        # representation of the purpose.
        purpose_dunder_string = str(self.user_purpose)
        self.assertEqual(
            purpose_dunder_string,
            "A Test Purpose Text",
        )

    def test_meta_class(self):
        """
        Tests for the `Purpose` model `Meta` class.
        """
        # Test that the `Meta` class has the correct verbose name plural of
        # "Purposes".
        purpose_verbose_name_plural = Purpose._meta.verbose_name_plural
        self.assertEqual(
            purpose_verbose_name_plural,
            "Purposes",
        )


class SkillTestCase(TestCase):
    """
    Tests for the Skill model.
    """

    def test_model_exists_and_has_proper_attributes(self):
        """
        Tests for the `Skill` model.
        """
        # Test that the `Skill` model exists.
        self.assertIsNotNone(Skill)
        # Test that the `Skill` model is a subclass of `models.Model`.
        self.assertTrue(issubclass(Skill, d_db_models.Model))
        # Test that the `Skill` model has a `user` field.
        self.assertTrue(hasattr(Skill, "user"))
        # Test that the `Skill` model has a `name` field.
        self.assertTrue(hasattr(Skill, "name"))
        # Test that the `Skill` model has a `__str__` method.
        self.assertTrue(hasattr(Skill, "__str__"))
        # Test that the `Skill` model has a `Meta` class.
        self.assertTrue(hasattr(Skill, "Meta"))

    def test_user_field(self):
        """
        Tests for the `Skill` model `user` field.
        """
        # Test that `user` field uses the proper user model.
        skill_user_model = Skill._meta.get_field("user").remote_field.model
        self.assertEqual(
            skill_user_model,
            get_user_model(),
        )
        # Test that the `user` field has the correct verbose name of "User".
        skill_user_verbose_name = Skill._meta.get_field("user").verbose_name
        self.assertEqual(
            skill_user_verbose_name,
            "User",
        )
        # Test that the `user` field has the correct help text of "The user who
        # created the skill.".
        skill_user_help_text = Skill._meta.get_field("user").help_text
        self.assertEqual(
            skill_user_help_text,
            "The user who created the skill.",
        )
        # Test that the `user` field has the correct on_delete behavior of
        # "models.CASCADE".
        field = Skill._meta.get_field("user")
        skill_user_on_delete = field.remote_field.on_delete
        self.assertEqual(
            skill_user_on_delete,
            d_db_models.CASCADE,
        )

    def test_name_field(self):
        """
        Tests for the `Skill` model `name` field.
        """
        # Test that the `name` field has the correct verbose name of "Name".
        skill_name_verbose_name = Skill._meta.get_field("name").verbose_name
        self.assertEqual(
            skill_name_verbose_name,
            "Name",
        )
        # Test that the `name` field has the correct help text of "The name of
        # the skill.".
        skill_name_help_text = Skill._meta.get_field("name").help_text
        self.assertEqual(
            skill_name_help_text,
            "The name of the skill.",
        )
        # Test that the `name` field has the correct max length of "255".
        skill_name_max_length = Skill._meta.get_field("name").max_length
        self.assertEqual(
            skill_name_max_length,
            255,
        )

    def test_dunder_string_method(self):
        """
        Tests for the `Skill` model `__str__` method.
        """
        # Create a `Customuser` object.
        self.user = get_user_model().objects.create_user(
            username="BunbunKitten",
            password="MeowMeow42",
        )
        # Create a `Skill` object.
        self.user_skill = Skill.objects.create(
            user=self.user,
            name="A Test Skill Name",
        )
        # Test that the `__str__` method returns the correct string
        # representation of the skill.
        skill_dunder_string = str(self.user_skill)
        self.assertEqual(
            skill_dunder_string,
            "A Test Skill Name",
        )

    def test_meta_class(self):
        """
        Tests for the `Skill` model `Meta` class.
        """
        # Test that the `Meta` class has the correct verbose name plural of
        # "Skills".
        skill_verbose_name_plural = Skill._meta.verbose_name_plural
        self.assertEqual(
            skill_verbose_name_plural,
            "Skills",
        )


class BehavioralInterviewQuestionTestCase(TestCase):
    """
    Tests for the BehavioralInterviewQuestion model.
    """

    def test_behavioral_interview_question_exists_and_has_proper_attributes(self):
        """
        Tests for the `BehavioralInterviewQuestion` model.
        """
        # Test that the `BehavioralInterviewQuestion` model exists.
        self.assertIsNotNone(BehavioralInterviewQuestion)
        # Test that the `BehavioralInterviewQuestion` model is a subclass of
        # `models.Model`.
        self.assertTrue(issubclass(BehavioralInterviewQuestion, d_db_models.Model))
        # Test that the `BehavioralInterviewQuestion` model has a `user` field.
        self.assertTrue(hasattr(BehavioralInterviewQuestion, "user"))
        # Test that the `BehavioralInterviewQuestion` model has a `text` field.
        self.assertTrue(hasattr(BehavioralInterviewQuestion, "text"))
        # Test that the `BehavioralInterviewQuestion` model has a `__str__`
        # method.
        self.assertTrue(hasattr(BehavioralInterviewQuestion, "__str__"))
        # Test that the `BehavioralInterviewQuestion` model has a `Meta` class.
        self.assertTrue(hasattr(BehavioralInterviewQuestion, "Meta"))

    def test_user_field(self):
        """
        Tests for the `BehavioralInterviewQuestion` model `user` field.
        """
        # Test that `user` field uses the proper user model.
        behavioral_interview_question_user_model = (
            BehavioralInterviewQuestion._meta.get_field("user").remote_field.model
        )
        self.assertEqual(
            behavioral_interview_question_user_model,
            get_user_model(),
        )
        # Test that the `user` field has the correct verbose name of "User".
        behavioral_interview_question_user_verbose_name = (
            BehavioralInterviewQuestion._meta.get_field("user").verbose_name
        )
        self.assertEqual(
            behavioral_interview_question_user_verbose_name,
            "User",
        )
        # Test that the `user` field has the correct help text of "The user who
        # created the behavioral interview question.".
        behavioral_interview_question_user_help_text = (
            BehavioralInterviewQuestion._meta.get_field("user").help_text
        )
        self.assertEqual(
            behavioral_interview_question_user_help_text,
            "The user who created the behavioral interview question.",
        )
        # Test that the `user` field has the correct on_delete behavior of
        # "models.CASCADE".
        field = BehavioralInterviewQuestion._meta.get_field("user")
        behavioral_interview_question_user_on_delete = field.remote_field.on_delete
        self.assertEqual(
            behavioral_interview_question_user_on_delete,
            d_db_models.CASCADE,
        )

    def test_text_field(self):
        """
        Tests for the `BehavioralInterviewQuestion` model `text` field.
        """
        # Test that the `text` field has the correct verbose name of "Text".
        behavioral_interview_question_text_verbose_name = (
            BehavioralInterviewQuestion._meta.get_field("text").verbose_name
        )
        self.assertEqual(
            behavioral_interview_question_text_verbose_name,
            "Text",
        )
        # Test that the `text` field has the correct help text of "The text of
        # the behavioral interview question.".
        behavioral_interview_question_text_help_text = (
            BehavioralInterviewQuestion._meta.get_field("text").help_text
        )
        self.assertEqual(
            behavioral_interview_question_text_help_text,
            "The text of the behavioral interview question.",
        )

    def test_dunder_string_method(self):
        """
        Tests for the `BehavioralInterviewQuestion` model `__str__` method.
        """
        # Create a `Customuser` object.
        self.user = get_user_model().objects.create_user(
            username="BunbunKitten",
            password="MeowMeow42",
        )
        # Create a `BehavioralInterviewQuestion` object.
        self.user_behavioral_interview_question = (
            BehavioralInterviewQuestion.objects.create(
                user=self.user,
                text="A Test Behavioral Interview Question Text",
            )
        )
        # Test that the `__str__` method returns the correct string
        # representation of the behavioral interview question.
        behavioral_interview_question_dunder_string = str(
            self.user_behavioral_interview_question
        )
        self.assertEqual(
            behavioral_interview_question_dunder_string,
            "A Test Behavioral Interview Question Text",
        )

    def test_meta_class(self):
        """
        Tests for the `BehavioralInterviewQuestion` model `Meta` class.
        """
        # Test that the `Meta` class has the correct verbose name plural of
        # "Behavioral Interview Questions".
        behavioral_interview_question_verbose_name_plural = (
            BehavioralInterviewQuestion._meta.verbose_name_plural
        )
        self.assertEqual(
            behavioral_interview_question_verbose_name_plural,
            "Behavioral Interview Questions",
        )


class QuestionResponseTestCase(TestCase):
    """
    Tests for the QuestionResponse model.
    """

    def test_question_response_exists_and_has_proper_attributes(self):
        """
        Tests for the `QuestionResponse` model.
        """
        # Test that the `QuestionResponse` model exists.
        self.assertIsNotNone(QuestionResponse)
        # Test that the `QuestionResponse` model is a subclass of
        # `models.Model`.
        self.assertTrue(issubclass(QuestionResponse, d_db_models.Model))
        # Test that the `QuestionResponse` model has a `user` field.
        self.assertTrue(hasattr(QuestionResponse, "user"))
        # Test that the `QuestionResponse` model has a `question` field.
        self.assertTrue(hasattr(QuestionResponse, "question"))
        # Test that the `QuestionResponse` model has a `text` field.
        self.assertTrue(hasattr(QuestionResponse, "text"))
        # Test that the `QuestionResponse` model has a `__str__` method.
        self.assertTrue(hasattr(QuestionResponse, "__str__"))
        # Test that the `QuestionResponse` model has a `Meta` class.
        self.assertTrue(hasattr(QuestionResponse, "Meta"))

    def test_user_field(self):
        """
        Tests for the `QuestionResponse` model `user` field.
        """
        # Test that `user` field uses the proper user model.
        question_response_user_model = QuestionResponse._meta.get_field(
            "user"
        ).remote_field.model
        self.assertEqual(
            question_response_user_model,
            get_user_model(),
        )
        # Test that the `user` field has the correct verbose name of "User".
        question_response_user_verbose_name = QuestionResponse._meta.get_field(
            "user"
        ).verbose_name
        self.assertEqual(
            question_response_user_verbose_name,
            "User",
        )
        # Test that the `user` field has the correct help text of "The user who
        # created the question response.".
        question_response_user_help_text = QuestionResponse._meta.get_field(
            "user"
        ).help_text
        self.assertEqual(
            question_response_user_help_text,
            "The user who created the question response.",
        )
        # Test that the `user` field has the correct on_delete behavior of
        # "models.CASCADE".
        field = QuestionResponse._meta.get_field("user")
        question_response_user_on_delete = field.remote_field.on_delete
        self.assertEqual(
            question_response_user_on_delete,
            d_db_models.CASCADE,
        )

    def test_question_field(self):
        """
        Tests for the `QuestionResponse` model `question` field.
        """
        # Test that `question` field uses the proper user model.
        question_response_question_model = QuestionResponse._meta.get_field(
            "question"
        ).remote_field.model
        self.assertEqual(
            question_response_question_model,
            BehavioralInterviewQuestion,
        )
        # Test that the `question` field has the correct verbose name of
        # "Behavioral Interview Question".
        question_response_question_verbose_name = QuestionResponse._meta.get_field(
            "question"
        ).verbose_name
        self.assertEqual(
            question_response_question_verbose_name,
            "Behavioral Interview Question",
        )
        # Test that the `question` field has the correct help text of "The
        # behavioral interview question that the response is for.".
        question_response_question_help_text = QuestionResponse._meta.get_field(
            "question"
        ).help_text
        self.assertEqual(
            question_response_question_help_text,
            "The behavioral interview question that the response is for.",
        )
        # Test that the `question` field has the correct on_delete behavior of
        # "models.CASCADE".
        field = QuestionResponse._meta.get_field("question")
        question_response_question_on_delete = field.remote_field.on_delete
        self.assertEqual(
            question_response_question_on_delete,
            d_db_models.CASCADE,
        )

    def test_text_field(self):
        """
        Tests for the `QuestionResponse` model `text` field.
        """
        # Test that the `text` field has the correct verbose name of "Text".
        question_response_text_verbose_name = QuestionResponse._meta.get_field(
            "text"
        ).verbose_name
        self.assertEqual(
            question_response_text_verbose_name,
            "Text",
        )
        # Test that the `text` field has the correct help text of "The text of
        # the question response.".
        question_response_text_help_text = QuestionResponse._meta.get_field(
            "text"
        ).help_text
        self.assertEqual(
            question_response_text_help_text,
            "The text of the question response.",
        )

    def test_dunder_string_method(self):
        """
        Tests for the `QuestionResponse` model `__str__` method.
        """
        # Create a `Customuser` object.
        self.user = get_user_model().objects.create_user(
            username="BunbunKitten",
            password="MeowMeow42",
        )
        # Create a `BehavioralInterviewQuestion` object.
        self.user_behavioral_interview_question = (
            BehavioralInterviewQuestion.objects.create(
                user=self.user,
                text="A Test Behavioral Interview Question Text",
            )
        )
        # Create a `QuestionResponse` object.
        self.user_question_response = QuestionResponse.objects.create(
            user=self.user,
            question=self.user_behavioral_interview_question,
            text="A Test Question Response Text",
        )
        # Test that the `__str__` method returns the correct string
        # representation of the question response.
        question_response_dunder_string = str(self.user_question_response)
        self.assertEqual(
            question_response_dunder_string,
            "A Test Question Response Text",
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

    def test_user_verbose_name(self):
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

    def test_user_help_text(self):
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

    def test_user_on_delete_is_cascade(self):
        """
        Test that the on_delete behavior of the user field is "models.CASCADE".
        """
        field = ElevatorSpeech._meta.get_field("user")
        elevator_speech_user_on_delete = field.remote_field.on_delete
        self.assertEqual(
            elevator_speech_user_on_delete,
            d_db_models.CASCADE,
        )

    def test_theme_verbose_name(self):
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

    def test_theme_help_text(self):
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

    def test_theme_max_length(self):
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

    def test_bullet_points_verbose_name(self):
        """
        Test that the verbose name of the bullet_points field is "Bullet
        Points".
        """
        elevator_speech_bullet_points_verbose_name = ElevatorSpeech._meta.get_field(
            "bullet_points"
        ).verbose_name
        self.assertEqual(
            elevator_speech_bullet_points_verbose_name,
            "Bullet Points",
        )

    def test_bullet_points_help_text(self):
        """
        Test that the help text of the bullet_points field is "The bullet
        points that can be used in the elevator speech.".
        """
        elevator_speech_bullet_points_help_text = ElevatorSpeech._meta.get_field(
            "bullet_points",
        ).help_text
        self.assertEqual(
            elevator_speech_bullet_points_help_text,
            "The bullet points that can be used in the elevator speech.",
        )

    def test_bullet_points_related_model(self):
        """
        Test that the related model of the bullet_points field is
        "BulletPoint".
        """
        elevator_speech_bullet_points_related_model = ElevatorSpeech._meta.get_field(
            "bullet_points",
        ).remote_field.model
        self.assertEqual(
            elevator_speech_bullet_points_related_model,
            BulletPoint,
        )

    def test_text_verbose_name(self):
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

    def test_text_help_text(self):
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

    def test_dunder_string_method(self):
        """
        Test that the string representation of the ElevatorSpeech model is
        "test_elevator_speech_theme".
        """
        elevator_speech_dunder_string = str(self.elevator_speech)
        self.assertEqual(
            elevator_speech_dunder_string,
            "test_elevator_speech_theme",
        )

    def test_verbose_name_plural(self):
        """
        Test that the verbose name plural of the ElevatorSpeech model is
        "Elevator Speeches".
        """
        elevator_speech_verbose_name_plural = ElevatorSpeech._meta.verbose_name_plural
        self.assertEqual(
            elevator_speech_verbose_name_plural,
            "Elevator Speeches",
        )
