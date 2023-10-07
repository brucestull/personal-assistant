from django.db import models
# from statistics import median

from config.settings.common import AUTH_USER_MODEL
from base.models import CreatedUpdatedBase


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

    # Use the `@staticmethod` decorator to define a static method.
    # A `static method` is a method that doesn't need to be called on an
    # instance of the class.
    # An `instance of the class` means an object created from the class.
    # A `static method` is a method that doesn't need `self` as the first
    # argument.
    # A `BloodPressure` object is not needed to call the
    # `get_average_and_median` method.
    # a_specific_blood_pressure_object =
    # BloodPressure.objects.get(systolic=120, diastolic=80) is not needed.
    # BloodPressure.get_average_and_median() is enough.
    # @staticmethod
    # def get_average_and_median():
    #     """
    #     Method to get the average and median of the systolic and diastolic
    #     blood pressure readings of all the `systolic` and `diastolic`
    #     values of `BloodPressure` objects.
    #     """
    #     systolic_values = BloodPressure.objects.values_list(
    #         "systolic",
    #         flat=True,
    #     )
    #     diastolic_values = BloodPressure.objects.values_list(
    #         "diastolic",
    #         flat=True,
    #     )
    #     if len(systolic_values) == 0:
    #         return {
    #             "systolic_average": None,
    #             "diastolic_average": None,
    #             "systolic_median": None,
    #             "diastolic_median": None,
    #         }
    #     else:
    #         systolic_average = sum(systolic_values) / len(systolic_values)
    #         diastolic_average = sum(diastolic_values) / len(diastolic_values)
    #         systolic_median = median(systolic_values)
    #         diastolic_median = median(diastolic_values)
    #     return {
    #         "systolic_average": round(systolic_average, 2),
    #         "diastolic_average": round(diastolic_average, 2),
    #         "systolic_median": round(systolic_median, 2),
    #         "diastolic_median": round(diastolic_median, 2),
    #     }

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
