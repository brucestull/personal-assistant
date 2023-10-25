from django.db import models

from base.models import CreatedUpdatedBase
from config.settings import AUTH_USER_MODEL


class BloodPressure(CreatedUpdatedBase):
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
        verbose_name="Systolic Blood Pressure",
        help_text="The systolic blood pressure reading.",
    )
    diastolic = models.PositiveSmallIntegerField(
        verbose_name="Diastolic Blood Pressure",
        help_text="The diastolic blood pressure reading.",
    )
    pulse = models.PositiveSmallIntegerField(
        verbose_name="Pulse",
        help_text="The pulse rate in beats per minute.",
    )

    class Meta:
        verbose_name_plural = "Blood Pressure Measurements"

    def __str__(self):
        return (
            f"{self.user.username} | "
            f"{self.systolic} / {self.diastolic} mmHg | {self.pulse} bpm"
        )


class Pulse(CreatedUpdatedBase):
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
        verbose_name="Beats Per Minute",
        help_text="The pulse rate in beats per minute.",
    )

    class Meta:
        verbose_name = "Pulse Measurement"
        verbose_name_plural = "Pulse Measurements"

    def __str__(self):
        return f"{self.user.username} | {self.bpm} Beats Per Minute"


class Temperature(CreatedUpdatedBase):
    """
    Model for `subject` temperature `measurement`.
    """

    subject = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="Subject",
        on_delete=models.CASCADE,
        related_name="temperatures",
        help_text="The subject that gets their temperature measured.",
    )
    measurement = models.DecimalField(
        verbose_name="Temperature Measurement",
        max_digits=4,
        decimal_places=1,
        help_text="The temperature measurement in degrees Fahrenheit.",
    )

    class Meta:
        verbose_name = "Temperature Measurement"
        verbose_name_plural = "Temperature Measurements"

    def __str__(self):
        return f"{self.subject.username} | {self.measurement}°F"


class BodyWeight(CreatedUpdatedBase):
    """
    Model for `subject` body weight `measurement`.
    """

    subject = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="Subject",
        on_delete=models.CASCADE,
        related_name="body_weights",
        help_text="The subject that gets their body weight measured.",
    )
    measurement = models.DecimalField(
        verbose_name="Body Weight Measurement",
        max_digits=5,
        decimal_places=2,
        help_text="The body weight measurement in pounds.",
    )

    class Meta:
        verbose_name = "Body Weight Measurement"
        verbose_name_plural = "Body Weight Measurements"

    def __str__(self):
        return f"{self.subject.username} | {self.measurement} lbs"
