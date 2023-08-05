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
        help_text="Designates whether this user's registration has been accepted.",
    )

    def get_user_blood_pressure_range(self):
        """
        Returns the maximum and minimum systolic and diastolic blood pressure readings
        for the current user.

        Attributes:
        - `self` is the current `CustomUser` object.
        - `systolic_min` is the minimum systolic blood pressure reading of all
        the `BloodPressure` objects for the current user.
        - `diastolic_min` is the minimum diastolic blood pressure reading of
        all the `BloodPressure` objects for the current user.
        - `systolic_max` is the maximum systolic blood pressure reading of all
        the `BloodPressure` objects for the current user.
        - `diastolic_max` is the maximum diastolic blood pressure reading of
        all the `BloodPressure` objects for the current user.
        """
        systolic_min = BloodPressure.objects.filter(
            user=self,
        ).order_by("systolic").first().systolic
        diastolic_min = BloodPressure.objects.filter(
            user=self,
        ).order_by("diastolic").first().diastolic
        systolic_max = BloodPressure.objects.filter(
            user=self,
        ).order_by("-systolic").first().systolic
        diastolic_max = BloodPressure.objects.filter(
            user=self,
        ).order_by("-diastolic").first().diastolic
        return {
            "systolic_min": systolic_min,
            "diastolic_min": diastolic_min,
            "systolic_max": systolic_max,
            "diastolic_max": diastolic_max,
        }


    def __str__(self):
        """
        String representation of CustomUser.
        """
        return self.username
