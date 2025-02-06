from django.db import models
from django.urls import reverse
from django.utils import timezone

from config.settings import AUTH_USER_MODEL


class ActivityType(models.Model):
    """
    Model for the `ActivityType` model.
    """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activity_types",
    )

    def __str__(self):
        return (
            f"{self.name}"
            # f"- {self.user}"
        )

    class Meta:
        verbose_name_plural = "Activity Types"


class Activity(models.Model):
    """
    Model for the `Activity` model.
    """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    activity_type = models.ForeignKey(
        ActivityType,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    notes = models.TextField(
        blank=True,
        help_text="Any notes for the activity.",
    )

    def __str__(self):
        return f"{self.name} - {self.activity_type}"

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "Activities"


class ActivityCompleted(models.Model):
    """
    Model for the `ActivityCompleted` model.
    """

    activity = models.ForeignKey(
        "Activity",
        on_delete=models.CASCADE,
        related_name="completed_activity",
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities_completed",
    )
    date = models.DateTimeField(
        help_text="The date and time the activity was completed.",
        default=timezone.now,
    )

    def __str__(self):
        return f"{self.activity} on {self.date}"

    class Meta:
        verbose_name_plural = "Activities Completed"
