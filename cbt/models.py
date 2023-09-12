from django.db import models

from base.models import CreatedUpdatedBase
from config.settings.common import AUTH_USER_MODEL


class CognativeDistortion(CreatedUpdatedBase):
    """
    Model class for a user's cognative distortion.

    This model will be available to all users. So, won't have a `user` field.

    This model will be populated by the admin user. Additions, deletions, and
    updates may be done by the admin user.

    Attributes:
        name (str): The name of the cognative distortion.
        description (str): The description of the cognative distortion.
    """

    name = models.CharField(
        verbose_name="Cognative Distortion",
        max_length=150,
        help_text="The name of the cognative distortion.",
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="The description of the cognative distortion.",
    )

    def __str__(self):
        """
        String representation of a `CognativeDistortion` object.
        """
        return (
            f"{self.name} "
            f"--- "
            # Truncate the description to 57 characters, if necessary.
            + (
                self.description[:57] + \
                '...' if len(self.description) > 57 else self.description
            )
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
        cognative_distortions (list): The list of cognative distortions
        associated with the thought.
    """

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="thoughts",
        help_text="The user that has the thought.",
    )
    cognative_distortion = models.ManyToManyField(
        CognativeDistortion,
        related_name="thoughts",
        help_text="The cognative distortion of the thought."
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

    def __str__(self):
        """
        String representation of a `Thought` object.
        """
        return f"{self.user.username} | {self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = "Thought"
        verbose_name_plural = "Thoughts"
