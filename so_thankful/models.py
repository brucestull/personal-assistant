from django.db import models
from django.contrib.auth import get_user_model


class Strength(models.Model):
    """
    Model representing a user's strengths.
    """

    description = models.CharField(max_length=200)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="strengths",
    )

    def __str__(self):
        return f"{self.user.username} - {self.description}"


class Gratitude(models.Model):
    """
    Model representing a user's gratitudes.
    """

    description = models.CharField(max_length=200)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="gratitudes",
    )

    def __str__(self):
        return f"{self.user.username} - {self.description}"


class LovedOne(models.Model):
    """
    Model representing a user's loved ones.
    """

    name = models.CharField(max_length=200)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="loved_ones",
    )

    def __str__(self):
        return f"{self.user.username} - {self.name}"
