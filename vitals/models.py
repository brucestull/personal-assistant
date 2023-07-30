from django.db import models

from config.settings.common import AUTH_USER_MODEL


class DateTimeBase(models.Model):
    """
    An abstract base class model that provides self-updating `created` and `updated` fields.
    """

    created = models.DateTimeField(
        "Created",
        auto_now_add=True,
        help_text="The date and time this object was created.",
    )
    updated = models.DateTimeField(
        "Updated",
        auto_now=True,
        help_text="The date and time this object was last updated.",
    )

    class Meta:
        abstract = True


class BloodPressure(DateTimeBase):
    """
    Model class for a user's blood pressure.
    """

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blood_pressures",
        help_text="The user that measures their blood pressure.",
    )
    systolic = models.PositiveSmallIntegerField(
        help_text="The systolic blood pressure reading."
    )
    diastolic = models.PositiveSmallIntegerField(
        help_text="The diastolic blood pressure reading."
    )

    class Meta:
        verbose_name_plural = "Blood Pressure Measurements"

    def __str__(self):
        return f"{self.user.username} | {self.systolic}/{self.diastolic} mmHg"


class Pulse(DateTimeBase):
    """
    Model class for a user's pulse.
    """

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pulses",
        help_text="The user that measures their pulse.",
    )
    bpm = models.PositiveSmallIntegerField(
        help_text="The pulse reading."
    )

    class Meta:
        verbose_name = "Pulse Measurement"
        verbose_name_plural = "Pulse Measurements"

    def __str__(self):
        return f"{self.user.username} | {self.bpm} bpm"
