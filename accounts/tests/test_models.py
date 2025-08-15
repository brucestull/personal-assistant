# accounts/tests/test_models.py
from django.test import TestCase

from accounts.models import CustomUser
from vitals.models import BloodPressure

A_TEST_USERNAME = "ACustomUser"
ANOTHER_TEST_USERNAME = "AnotherCustomUser"

CUSTOM_USER_REGISTRATION_ACCEPTED_HELP_TEXT = (
    "Designates whether this user's registration has been accepted."
)

BLOOD_PRESSURE_SYSTOLIC_1 = 120
BLOOD_PRESSURE_DIASTOLIC_1 = 80
BLOOD_PRESSURE_PULSE_1 = 73
BLOOD_PRESSURE_SYSTOLIC_2 = 110
BLOOD_PRESSURE_DIASTOLIC_2 = 70
BLOOD_PRESSURE_PULSE_2 = 73
BLOOD_PRESSURE_SYSTOLIC_3 = 115
BLOOD_PRESSURE_DIASTOLIC_3 = 75
BLOOD_PRESSURE_PULSE_3 = 73

SYSTOLIC_MIN = min(
    BLOOD_PRESSURE_SYSTOLIC_1,
    BLOOD_PRESSURE_SYSTOLIC_2,
    BLOOD_PRESSURE_SYSTOLIC_3,
)
DIASTOLIC_MIN = min(
    BLOOD_PRESSURE_DIASTOLIC_1,
    BLOOD_PRESSURE_DIASTOLIC_2,
    BLOOD_PRESSURE_DIASTOLIC_3,
)
SYSTOLIC_MAX = max(
    BLOOD_PRESSURE_SYSTOLIC_1,
    BLOOD_PRESSURE_SYSTOLIC_2,
    BLOOD_PRESSURE_SYSTOLIC_3,
)
DIASTOLIC_MAX = max(
    BLOOD_PRESSURE_DIASTOLIC_1,
    BLOOD_PRESSURE_DIASTOLIC_2,
    BLOOD_PRESSURE_DIASTOLIC_3,
)

SYSTOLIC_AVERAGE = (
    sum(
        [
            BLOOD_PRESSURE_SYSTOLIC_1,
            BLOOD_PRESSURE_SYSTOLIC_2,
            BLOOD_PRESSURE_SYSTOLIC_3,
        ]
    )
    / 3
)
DIASTOLIC_AVERAGE = (
    sum(
        [
            BLOOD_PRESSURE_DIASTOLIC_1,
            BLOOD_PRESSURE_DIASTOLIC_2,
            BLOOD_PRESSURE_DIASTOLIC_3,
        ]
    )
    / 3
)
SYSTOLIC_MEDIAN = sorted(
    [
        BLOOD_PRESSURE_SYSTOLIC_1,
        BLOOD_PRESSURE_SYSTOLIC_2,
        BLOOD_PRESSURE_SYSTOLIC_3,
    ]
)[1]
DIASTOLIC_MEDIAN = sorted(
    [
        BLOOD_PRESSURE_DIASTOLIC_1,
        BLOOD_PRESSURE_DIASTOLIC_2,
        BLOOD_PRESSURE_DIASTOLIC_3,
    ]
)[1]


class CustomUserModelTest(TestCase):
    """
    Tests for `CustomUser` model (registration & __str__) and
    the BloodPressure stats now provided by `vitals` (QuerySet.summary()).
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.
        """
        cls.user = CustomUser.objects.create(
            username=A_TEST_USERNAME,
        )
        cls.blood_pressure_1 = BloodPressure.objects.create(
            user=cls.user,
            systolic=BLOOD_PRESSURE_SYSTOLIC_1,
            diastolic=BLOOD_PRESSURE_DIASTOLIC_1,
            pulse=BLOOD_PRESSURE_PULSE_1,
        )
        cls.blood_pressure_2 = BloodPressure.objects.create(
            user=cls.user,
            systolic=BLOOD_PRESSURE_SYSTOLIC_2,
            diastolic=BLOOD_PRESSURE_DIASTOLIC_2,
            pulse=BLOOD_PRESSURE_PULSE_2,
        )
        cls.blood_pressure_3 = BloodPressure.objects.create(
            user=cls.user,
            systolic=BLOOD_PRESSURE_SYSTOLIC_3,
            diastolic=BLOOD_PRESSURE_DIASTOLIC_3,
            pulse=BLOOD_PRESSURE_PULSE_3,
        )

    # --- CustomUser field tests ---

    def test_registration_accepted_default_attribute_false(self):
        user = CustomUser.objects.get(id=self.user.id)
        field_registration_accepted = user._meta.get_field("registration_accepted")
        self.assertEqual(field_registration_accepted.default, False)

    def test_new_user_has_registration_accepted_false(self):
        user = CustomUser.objects.get(id=self.user.id)
        self.assertFalse(user.registration_accepted)

    def test_registration_accepted_help_text(self):
        user = CustomUser.objects.get(id=self.user.id)
        self.assertEqual(
            user._meta.get_field("registration_accepted").help_text,
            CUSTOM_USER_REGISTRATION_ACCEPTED_HELP_TEXT,
        )

    def test_dunder_string_method(self):
        user = CustomUser.objects.get(id=self.user.id)
        self.assertEqual(str(user), user.username)

    # --- BloodPressure stats (moved to vitals) ---

    def test_blood_pressure_range_via_summary(self):
        """
        The BloodPressure QuerySet.summary() should include min/max for systolic/diastolic. # noqa: E501
        """
        summary = BloodPressure.objects.for_user(self.user).summary()
        self.assertEqual(
            {
                "systolic_min": summary["systolic_min"],
                "diastolic_min": summary["diastolic_min"],
                "systolic_max": summary["systolic_max"],
                "diastolic_max": summary["diastolic_max"],
            },
            {
                "systolic_min": SYSTOLIC_MIN,
                "diastolic_min": DIASTOLIC_MIN,
                "systolic_max": SYSTOLIC_MAX,
                "diastolic_max": DIASTOLIC_MAX,
            },
        )

    def test_blood_pressure_averages_and_medians_via_summary(self):
        """
        The BloodPressure QuerySet.summary() should include average (rounded to 2dp) and median. # noqa: E501
        """
        summary = BloodPressure.objects.for_user(self.user).summary()
        # Averages are rounded to 2 decimals; use assertAlmostEqual to avoid float issues. # noqa: E501
        self.assertAlmostEqual(
            summary["systolic_average"], float(SYSTOLIC_AVERAGE), places=2
        )
        self.assertAlmostEqual(
            summary["diastolic_average"], float(DIASTOLIC_AVERAGE), places=2
        )
        self.assertEqual(summary["systolic_median"], SYSTOLIC_MEDIAN)
        self.assertEqual(summary["diastolic_median"], DIASTOLIC_MEDIAN)

    def test_summary_with_no_blood_pressures(self):
        """
        Summary should return all None values when the user has no BP readings.
        """
        empty_user = CustomUser.objects.create(username=ANOTHER_TEST_USERNAME)
        summary = BloodPressure.objects.for_user(empty_user).summary()
        self.assertEqual(
            summary,
            {
                "systolic_average": None,
                "diastolic_average": None,
                "systolic_median": None,
                "diastolic_median": None,
                "systolic_min": None,
                "diastolic_min": None,
                "systolic_max": None,
                "diastolic_max": None,
            },
        )
