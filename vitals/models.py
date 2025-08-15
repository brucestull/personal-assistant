# vitals/models.py
from statistics import median
from django.db import models
from django.db.models import Avg, Min, Max

from base.models import CreatedUpdatedBase
from config.settings import AUTH_USER_MODEL


class BloodPressureQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)

    def _aggregate_stats(self):
        # DB-side aggregates for min/max/avg
        return self.aggregate(
            systolic_min=Min("systolic"),
            diastolic_min=Min("diastolic"),
            systolic_max=Max("systolic"),
            diastolic_max=Max("diastolic"),
            systolic__avg=Avg("systolic"),
            diastolic__avg=Avg("diastolic"),
        )

    def _median_stats(self):
        # Python-side medians (portable across DBs)
        s_vals = list(self.values_list("systolic", flat=True))
        d_vals = list(self.values_list("diastolic", flat=True))
        return {
            "systolic_median": median(s_vals) if s_vals else None,
            "diastolic_median": median(d_vals) if d_vals else None,
        }

    def summary(self):
        """
        Returns a single dict with averages, medians, and range.
        Keys match what your views/templates expect.
        """
        if not self.exists():
            return {
                "systolic_average": None,
                "diastolic_average": None,
                "systolic_median": None,
                "diastolic_median": None,
                "systolic_min": None,
                "diastolic_min": None,
                "systolic_max": None,
                "diastolic_max": None,
            }

        agg = self._aggregate_stats()
        meds = self._median_stats()
        return {
            "systolic_average": (
                round(agg["systolic__avg"], 2)
                if agg["systolic__avg"] is not None
                else None
            ),
            "diastolic_average": (
                round(agg["diastolic__avg"], 2)
                if agg["diastolic__avg"] is not None
                else None
            ),
            **meds,
            "systolic_min": agg["systolic_min"],
            "diastolic_min": agg["diastolic_min"],
            "systolic_max": agg["systolic_max"],
            "diastolic_max": agg["diastolic_max"],
        }


class BloodPressureManager(models.Manager.from_queryset(BloodPressureQuerySet)):
    pass


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

    objects = BloodPressureManager()

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
