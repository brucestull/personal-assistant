

```python
"""Vitals app models.

This module defines small, focused models for tracking vital signs
and a custom QuerySet/Manager pair that provides convenient summary
statistics for blood pressure measurements.

Conventions used here
---------------------
- Google-style docstrings with Args/Returns/Raises.
- Light typing on queryset helpers for editor support without fighting
  Django's dynamic model attributes.
- `help_text` and `verbose_name` for admin clarity.
- QuerySet methods prefer DB-side aggregation for speed and portability,
  falling back to simple Python calculations for medians.

Dependencies
------------
- `CreatedUpdatedBase`: project base model that provides created/updated
  timestamps (imported from ``base.models``).
- `AUTH_USER_MODEL`: imported from settings to avoid tight coupling to
  a concrete User model.
"""

from __future__ import annotations

from statistics import median
from typing import Any, Dict, Optional

from django.db import models
from django.db.models import Avg, Min, Max

from base.models import CreatedUpdatedBase
from config.settings import AUTH_USER_MODEL


class BloodPressureQuerySet(models.QuerySet):
    """Custom queryset for :class:`BloodPressure` with user scoping and stats."""

    def for_user(self, user) -> "BloodPressureQuerySet":
        """Filter measurements for a single user.

        Args:
            user: A user instance (of ``AUTH_USER_MODEL``).

        Returns:
            BloodPressureQuerySet: Measurements belonging to ``user``.
        """
        return self.filter(user=user)

    def _aggregate_stats(self) -> Dict[str, Optional[float]]:
        """Compute DB-side aggregates (min/max/avg) for systolic/diastolic.

        Uses SQL ``MIN``/``MAX``/``AVG`` via Django's ORM for efficiency.

        Returns:
            dict: Keys include
                - ``systolic_min`` (int | None)
                - ``diastolic_min`` (int | None)
                - ``systolic_max`` (int | None)
                - ``diastolic_max`` (int | None)
                - ``systolic__avg`` (float | None)
                - ``diastolic__avg`` (float | None)
        """
        # DB-side aggregates are typically faster than Python loops and
        # avoid transferring large result sets to application memory.
        return self.aggregate(
            systolic_min=Min("systolic"),
            diastolic_min=Min("diastolic"),
            systolic_max=Max("systolic"),
            diastolic_max=Max("diastolic"),
            systolic__avg=Avg("systolic"),
            diastolic__avg=Avg("diastolic"),
        )

    def _median_stats(self) -> Dict[str, Optional[float]]:
        """Compute Python-side medians for systolic/diastolic.

        Notes:
            Django ORM doesn't offer a portable ``MEDIAN()`` across all DBs.
            Pulling values and using :func:`statistics.median` is simple and
            DB-agnostic. For large datasets, consider a DB that supports
            ``percentile_cont`` (e.g., PostgreSQL) or a materialized view.

        Returns:
            dict: Keys include
                - ``systolic_median`` (float | None)
                - ``diastolic_median`` (float | None)
        """
        s_vals = list(self.values_list("systolic", flat=True))
        d_vals = list(self.values_list("diastolic", flat=True))
        return {
            "systolic_median": median(s_vals) if s_vals else None,
            "diastolic_median": median(d_vals) if d_vals else None,
        }

    def summary(self) -> Dict[str, Optional[float]]:
        """Summarize blood pressure readings in one dict.

        Returns a single dictionary with averages (rounded to 2 decimals),
        medians, and min/max values. Keys are intentionally stable for
        template/view code.

        Returns:
            dict: Keys include
                - ``systolic_average`` (float | None)
                - ``diastolic_average`` (float | None)
                - ``systolic_median`` (float | None)
                - ``diastolic_median`` (float | None)
                - ``systolic_min`` (int | None)
                - ``diastolic_min`` (int | None)
                - ``systolic_max`` (int | None)
                - ``diastolic_max`` (int | None)
        """
        if not self.exists():
            # Maintain a stable shape for consumers even with no data.
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
    """Manager that exposes :class:`BloodPressureQuerySet` helpers on ``.objects``.

    Using ``from_queryset`` keeps IDE/type checker hints intact and ensures
    custom QuerySet methods are available on both the manager and chained
    querysets (e.g., ``BloodPressure.objects.for_user(u).summary()``).
    """

    pass


class BloodPressure(CreatedUpdatedBase):
    """A single blood pressure reading for a user.

    Fields:
        user: Foreign key to the reading owner. Cascades on delete.
        systolic: Systolic pressure (mmHg). Must be a positive small int.
        diastolic: Diastolic pressure (mmHg). Must be a positive small int.
        pulse: Pulse rate (beats per minute). Must be a positive small int.

    Notes:
        - Use ``BloodPressure.objects.for_user(user)`` to scope queries.
        - Use ``.summary()`` on a queryset to get aggregate stats.
    """

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blood_pressures",
        help_text="The user that measures their blood pressure.",
    )
    systolic = models.PositiveSmallIntegerField(
        verbose_name="Systolic Blood Pressure",
        help_text="The systolic blood pressure reading (mmHg).",
    )
    diastolic = models.PositiveSmallIntegerField(
        verbose_name="Diastolic Blood Pressure",
        help_text="The diastolic blood pressure reading (mmHg).",
    )
    pulse = models.PositiveSmallIntegerField(
        verbose_name="Pulse",
        help_text="The pulse rate in beats per minute (bpm).",
    )

    objects = BloodPressureManager()

    class Meta:
        verbose_name_plural = "Blood Pressure Measurements"
        # Optional ordering if you commonly show latest first:
        # ordering = ("-created",)
        # Optional composite index for common filters:
        # indexes = [models.Index(fields=("user", "created"))]

    def __str__(self) -> str:
        """Readable label for admin/lists.

        Returns:
            str: ``"<username> | <sys>/<dia> mmHg | <pulse> bpm"``.
        """
        return (
            f"{self.user.username} | "
            f"{self.systolic} / {self.diastolic} mmHg | {self.pulse} bpm"
        )


class Pulse(CreatedUpdatedBase):
    """A single pulse (heart rate) measurement for a user.

    Fields:
        user: Foreign key to the reading owner. Cascades on delete.
        bpm: Beats per minute. Positive small integer.

    Use Cases:
        - Lightweight model when you only need heart rate without BP.
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
        # ordering = ("-created",)

    def __str__(self) -> str:
        """Readable label for admin/lists.

        Returns:
            str: ``"<username> | <bpm> Beats Per Minute"``.
        """
        return f"{self.user.username} | {self.bpm} Beats Per Minute"


class Temperature(CreatedUpdatedBase):
    """A single body temperature measurement for a subject (user).

    Fields:
        subject: The person whose temperature was measured.
        measurement: Temperature in degrees Fahrenheit, one decimal place.

    Notes:
        - If you track Celsius, consider storing in a canonical unit and
          converting at the edge (serializer/template) or add a unit field.
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
        max_digits=4,  # e.g., 106.5
        decimal_places=1,
        help_text="The temperature measurement in degrees Fahrenheit.",
    )

    class Meta:
        verbose_name = "Temperature Measurement"
        verbose_name_plural = "Temperature Measurements"
        # ordering = ("-created",)

    def __str__(self) -> str:
        """Readable label for admin/lists.

        Returns:
            str: ``"<username> | <temp>°F"``.
        """
        return f"{self.subject.username} | {self.measurement}°F"


class BodyWeight(CreatedUpdatedBase):
    """A single body weight measurement for a subject (user).

    Fields:
        subject: The person whose weight was measured.
        measurement: Body weight in pounds with 2 decimal places.

    Validation:
        - Consider adding a form-level or model-clean validation to enforce
          realistic bounds based on your population.
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
        max_digits=5,  # e.g., 999.99
        decimal_places=2,
        help_text="The body weight measurement in pounds.",
    )

    class Meta:
        verbose_name = "Body Weight Measurement"
        verbose_name_plural = "Body Weight Measurements"
        # ordering = ("-created",)

    def __str__(self) -> str:
        """Readable label for admin/lists.

        Returns:
            str: ``"<username> | <weight> lbs"``.
        """
        return f"{self.subject.username} | {self.measurement} lbs"
```
