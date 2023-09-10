from statistics import median

from django.contrib.auth.models import AbstractUser
from django.db import models

from vitals.models import BloodPressure


class CustomUser(AbstractUser):
    """
    A `CustomUser` so we can add our own functionality for site users.
    """

    # `registration_accepted` is used to control access to the site.
    registration_accepted = models.BooleanField(
        default=False,
        help_text=(
            "Designates whether this user's registration has "
            "been accepted."
        )
    )

    def get_blood_pressure_range(self):
        """
        Returns the maximum and minimum systolic and diastolic blood
        pressure readings for the current user.

        Attributes:
        - `self` is the current `CustomUser` object.
        - `systolic_min` is the minimum systolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `diastolic_min` is the minimum diastolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `systolic_max` is the maximum systolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `diastolic_max` is the maximum diastolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        """
        if BloodPressure.objects.filter(user=self).count() == 0:
            # TODO: Determine if there is a better way to handle this.
            """
            {
                "systolic_min": None,
                "diastolic_min": None,
                "systolic_max": None,
                "diastolic_max": None,
            }
            """
            return None
        else:
            systolic_min = (
                BloodPressure.objects.filter(
                    user=self,
                )
                .order_by("systolic")
                .first()
                .systolic
            )
            diastolic_min = (
                BloodPressure.objects.filter(
                    user=self,
                )
                .order_by("diastolic")
                .first()
                .diastolic
            )
            systolic_max = (
                BloodPressure.objects.filter(
                    user=self,
                )
                .order_by("-systolic")
                .first()
                .systolic
            )
            diastolic_max = (
                BloodPressure.objects.filter(
                    user=self,
                )
                .order_by("-diastolic")
                .first()
                .diastolic
            )
            return {
                "systolic_min": systolic_min,
                "diastolic_min": diastolic_min,
                "systolic_max": systolic_max,
                "diastolic_max": diastolic_max,
            }

    def get_average_and_median_blood_pressure(self):
        """
        Returns the average and median systolic and diastolic blood
        pressure readings for the current user.

        Attributes:
        - `self` is the current `CustomUser` object.
        - `systolic_average` is the average systolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `diastolic_average` is the average diastolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `systolic_median` is the median systolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        - `diastolic_median` is the median diastolic blood pressure
        reading of all the `BloodPressure` objects for the current user.
        """
        systolic_average = (
            BloodPressure.objects.filter(
                user=self,
            )
            .values_list("systolic", flat=True)
            .aggregate(models.Avg("systolic"))
        )
        diastolic_average = (
            BloodPressure.objects.filter(
                user=self,
            )
            .values_list("diastolic", flat=True)
            .aggregate(models.Avg("diastolic"))
        )
        if BloodPressure.objects.filter(user=self).count() == 0:
            return {
                "systolic_average": None,
                "diastolic_average": None,
                "systolic_median": None,
                "diastolic_median": None,
            }
        else:
            systolic_median = median(
                BloodPressure.objects.filter(
                    user=self,
                ).values_list("systolic", flat=True)
            )
            diastolic_median = median(
                BloodPressure.objects.filter(
                    user=self,
                ).values_list("diastolic", flat=True)
            )
            return {
                "systolic_average": round(
                    systolic_average["systolic__avg"],
                    2,
                ),
                "diastolic_average": round(
                    diastolic_average["diastolic__avg"],
                    2,
                ),
                "systolic_median": systolic_median,
                "diastolic_median": diastolic_median,
            }

    def __str__(self):
        """
        String representation of CustomUser.
        """
        return self.username
