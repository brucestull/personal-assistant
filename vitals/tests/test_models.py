from django.test import TestCase
from django.urls import reverse
from django.db import models as d_db_models

from accounts.models import CustomUser
from vitals.models import BloodPressure
from vitals.models import Pulse


BLANK = ""

TEST_USERNAME = "test_username"
TEST_PASSWORD = "test_password"
TEST_FIRST_NAME = "Test"

BLOOD_PRESSURE_SYSTOLIC = 120
BLOOD_PRESSURE_DIASTOLIC = 80

BLOOD_PRESSURE_VERBOSE_NAME_PLURAL = "Blood Pressure Measurements"
BLOOD_PRESSURE_USER_LABEL = "user"
BLOOD_PRESSURE_USER_RELATED_NAME = "blood_pressures"
BLOOD_PRESSURE_USER_HELP_TEXT = "The user that measures their blood pressure."
BLOOD_PRESSURE_SYSTOLIC_HELP_TEXT = "The systolic blood pressure reading."
BLOOD_PRESSURE_DIASTOLIC_HELP_TEXT = "The diastolic blood pressure reading."


class DateTimeBaseModelTest(TestCase):
    pass


class BloodPressureModelTest(TestCase):
    """
    Tests for the `BloodPressure` model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Sets up data for the whole TestCase.
        """
        cls.user = CustomUser.objects.create_user(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            first_name=TEST_FIRST_NAME,
        )
        cls.blood_pressure = BloodPressure.objects.create(
            user=cls.user,
            systolic=BLOOD_PRESSURE_SYSTOLIC,
            diastolic=BLOOD_PRESSURE_DIASTOLIC,
        )
    
    def test_blood_pressure_user_label(self):
        """
        Test the `user` field label.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        user_label = blood_pressure._meta.get_field(BLOOD_PRESSURE_USER_LABEL).verbose_name
        self.assertEqual(user_label, BLOOD_PRESSURE_USER_LABEL)


class PulseModelTest(TestCase):
    pass
