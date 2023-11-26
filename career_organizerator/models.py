from django.db import models

from base.models import CreatedUpdatedBase
from config.settings import AUTH_USER_MODEL


class Purpose(CreatedUpdatedBase):
    """
    Model representing a `Purpose`. It encapsulates the rationale behind a user's
    interest in the other models within this application.

    Attributes:
        user (ForeignKey): The user who created the purpose.
        name (CharField): The name of the purpose.
    """

    # `user`: The user who created the purpose.
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="User",
        help_text="The user who created the purpose.",
        on_delete=models.CASCADE,
    )

    # `text`: The detailed explanation or description of the purpose.
    text = models.CharField(
        verbose_name="Text",
        help_text="The text of the purpose.",
        max_length=500,
    )

    def __str__(self):
        """
        Returns the string representation of the purpose.
        """
        return self.text

    class Meta:
        verbose_name_plural = "Purposes"


class Skill(CreatedUpdatedBase):
    """
    This model represents a single skill.

    Attributes:
        user (ForeignKey): The user who created the skill.
        name (CharField): The name of the skill.
    """

    # `user` is the user who created the skill.
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="User",
        help_text="The user who created the skill.",
        on_delete=models.CASCADE,
    )

    # `name` is the name of the skill.
    name = models.CharField(
        verbose_name="Name",
        help_text="The name of the skill.",
        max_length=255,
    )

    def __str__(self):
        """
        Returns the string representation of the skill.
        """
        return self.name

    class Meta:
        verbose_name_plural = "Skills"


class BehavioralInterviewQuestion(CreatedUpdatedBase):
    """
    This model represents a single behavioral interview question.
    """

    # `user` is the user who created the behavioral interview question.
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="User",
        help_text="The user who created the behavioral interview question.",
        on_delete=models.CASCADE,
    )

    # `text` is the text of the behavioral interview question.
    text = models.TextField(
        verbose_name="Text",
        help_text="The text of the behavioral interview question.",
    )

    def __str__(self):
        """
        Returns the string representation of the behavioral interview question.
        """
        return f"{self.text}"

    class Meta:
        verbose_name_plural = "Behavioral Interview Questions"


class QuestionResponse(CreatedUpdatedBase):
    """
    This model represents a single question response.
    """

    # `user` is the user who created the question response.
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="User",
        help_text="The user who created the question response.",
        on_delete=models.CASCADE,
    )

    # `question` is the behavioral interview question that the response is for.
    question = models.ForeignKey(
        BehavioralInterviewQuestion,
        verbose_name="Behavioral Interview Question",
        help_text="The behavioral interview question that the response is for.",
        on_delete=models.CASCADE,
    )

    # `text` is the text of the question response.
    text = models.TextField(
        verbose_name="Text",
        help_text="The text of the question response.",
    )

    def __str__(self):
        """
        Returns the string representation of the question response.
        """
        return self.text

    class Meta:
        verbose_name_plural = "Question Responses"


class BulletPoint(CreatedUpdatedBase):
    """
    This model represents a single bullet point.
    """

    # `user` is the user who created the bullet point.
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="User",
        help_text="The user who created the bullet point.",
        on_delete=models.CASCADE,
    )

    # `text` is the text of the bullet point.
    text = models.TextField(
        verbose_name="Text",
        help_text="The text of the bullet point.",
    )

    def __str__(self):
        """
        Returns the string representation of the bullet point.
        """
        return self.text

    class Meta:
        verbose_name_plural = "Bullet Points"


class ElevatorSpeech(CreatedUpdatedBase):
    """
    This model represents a single elevator speech.
    """

    # `user` is the user who created the elevator speech.
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="User",
        help_text="The user who created the elevator speech.",
        on_delete=models.CASCADE,
    )

    theme = models.CharField(
        verbose_name="Theme",
        help_text="The theme of the elevator speech.",
        max_length=255,
    )

    bullet_points = models.ManyToManyField(
        BulletPoint,
        verbose_name="Bullet Points",
        help_text="The bullet points that can be used in the elevator speech.",
    )

    # `text` is the text of the elevator speech.
    text = models.TextField(
        verbose_name="Text",
        help_text="The text of the elevator speech.",
    )

    def __str__(self):
        """
        Returns the string representation of the elevator speech.
        """
        return self.theme

    class Meta:
        verbose_name_plural = "Elevator Speeches"
