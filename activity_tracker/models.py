from django.db import models

from config.settings import AUTH_USER_MODEL


class ActivityType(models.Model):
    """
    Model for the `ActivityType` model.
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Activity Types"

    def __str__(self):
        return self.name


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
    notes = models.TextField()

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.activity_type} on {self.date}"


class ActivityCompleted(models.Model):
    """
    Model for the `ActivityCompleted` model.
    """

    activity = models.ForeignKey(
        "Activity",
        on_delete=models.CASCADE,
        related_name="activity_completed",
    )
    date = models.DateField()

    class Meta:
        verbose_name_plural = "Activities Completed"

    def __str__(self):
        return f"{self.activity} on {self.date}"
