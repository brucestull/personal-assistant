from django.db import models
from django.urls import reverse

from base.models import CreatedUpdatedBase
from config.settings import AUTH_USER_MODEL


class CognitiveDistortion(CreatedUpdatedBase):
    """
    Model class for a user's cognitive distortion.

    This model will be available to all users. So, won't have a `user` field.

    This model will be populated by the admin user. Additions, deletions, and
    updates may be done by the admin user.

    Attributes:
        name (str): The name of the cognitive distortion.
        description (str): The description of the cognitive distortion.
    """

    name = models.CharField(
        verbose_name="Cognative Distortion",
        max_length=150,
        help_text="The name of the cognitive distortion.",
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="The description of the cognitive distortion.",
    )

    def __str__(self):
        """
        String representation of a `CognitiveDistortion` object.
        """
        return f"{self.name} " f"--- " + (
            # Truncate the description to 57 characters, if necessary.
            self.description[:57] + "..."
            if len(self.description) > 57
            else self.description
        )

    class Meta:
        ordering = ["name"]
        verbose_name = "Cognative Distortion"
        verbose_name_plural = "Cognative Distortions"


class Thought(CreatedUpdatedBase):
    """
    Model class for a user's thought.

    This model will be unique to each user. So, will have a `user` field.

    Attributes:
        name (str): The name of the thought.
        description (str): The description of the thought.
        cognitive_distortions (list): The list of cognitive distortions
        associated with the thought.
    """

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="thoughts",
        help_text="The user that has the thought.",
    )
    cognitive_distortion = models.ManyToManyField(
        CognitiveDistortion,
        related_name="thoughts",
        help_text="The cognitive distortion of the thought.",
        blank=True,
    )
    name = models.CharField(
        verbose_name="Summary",
        max_length=250,
        help_text="A summary of the thought.",
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="The description of the thought.",
    )

    def get_absolute_url(self):
        """
        Returns the absolute URL for a `Thought` object.
        """
        return reverse("cbt:thought-detail", kwargs={"pk": self.pk})

    def __str__(self):
        """
        String representation of a `Thought` object.
        """
        return f"{self.user.username} | {self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = "Thought"
        verbose_name_plural = "Thoughts"
