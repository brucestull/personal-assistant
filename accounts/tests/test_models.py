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
    ) / 3
)
DIASTOLIC_AVERAGE = (
    sum(
        [
            BLOOD_PRESSURE_DIASTOLIC_1,
            BLOOD_PRESSURE_DIASTOLIC_2,
            BLOOD_PRESSURE_DIASTOLIC_3,
        ]
    ) / 3
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
    Tests for `CustomUser` model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.

        This specific function name `setUpTestData` is required by Django.
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

    def test_registration_accepted_default_attribute_false(self):
        """
        `CustomUser` model `registration_accepted` field `default` should
        be `False`.

        This tests the `default` attribute of the `registration_accepted`
        field of the `CustomUser` model.
        """
        user = CustomUser.objects.get(id=1)
        field_registration_accepted = user._meta.get_field(
            "registration_accepted",
        )
        self.assertEqual(field_registration_accepted.default, False)

    def test_new_user_has_registration_accepted_false(self):
        """
        A newly created `CustomUser` should have `registration_accepted`
        `False`.

        This tests the actual `default` value of the `registration_accepted`
        field of a newly created user.

        This test may be redundant with
        `test_registration_accepted_default_attribute_false`, since Django
        makes sure to use the `registration_accepted` default value we specify
        in the model, which is tested in
        `test_registration_accepted_default_attribute_false`.
        """
        user = CustomUser.objects.get(id=1)
        self.assertFalse(user.registration_accepted)

    def test_registration_accepted_help_text(self):
        """
        `CustomUser` model `registration_accepted` field `help_text` should
        be `Designates whether this user's registration has been accepted.`.
        """
        user = CustomUser.objects.get(id=1)
        self.assertEqual(
            user._meta.get_field(
                "registration_accepted",
            ).help_text,
            CUSTOM_USER_REGISTRATION_ACCEPTED_HELP_TEXT,
        )

    def test_get_blood_pressure_range_method(self):
        """
        `CustomUser` model `get_blood_pressure_range` method should
        return the minimum and maximum systolic and diastolic blood pressure
        readings for the current user.
        """
        user = CustomUser.objects.get(id=self.user.id)
        self.assertEqual(
            user.get_blood_pressure_range(),
            {
                "systolic_min": SYSTOLIC_MIN,
                "diastolic_min": DIASTOLIC_MIN,
                "systolic_max": SYSTOLIC_MAX,
                "diastolic_max": DIASTOLIC_MAX,
            },
        )

    def test_get_blood_pressure_range_method_with_no_blood_pressures(self):
        """
        `CustomUser` model `get_blood_pressure_range` method should
        return `None` if the current user has no blood pressure readings.
        """
        user = CustomUser.objects.create(
            username=ANOTHER_TEST_USERNAME,
        )
        self.assertIsNone(user.get_blood_pressure_range())

    def test_get_average_and_median_blood_pressure_method_with_bp(self):
        """
        `CustomUser` model `get_average_and_median_blood_pressure` method
        should return the average and median systolic and diastolic blood
        pressure readings for the current user.
        """
        user = CustomUser.objects.get(id=self.user.id)
        self.assertEqual(
            user.get_average_and_median_blood_pressure(),
            {
                "systolic_average": SYSTOLIC_AVERAGE,
                "diastolic_average": DIASTOLIC_AVERAGE,
                "systolic_median": SYSTOLIC_MEDIAN,
                "diastolic_median": DIASTOLIC_MEDIAN,
            },
        )

    def test_get_average_and_median_blood_pressure_method_with_no_bp(self):
        """
        `CustomUser` model `get_average_and_median_blood_pressure` method
        should return `None` for the average and median systolic and diastolic
        blood pressure readings for the current user if there are no blood
        pressures.
        """
        user = CustomUser.objects.get(id=1)
        user.blood_pressures.all().delete()
        self.assertEqual(
            user.get_average_and_median_blood_pressure(),
            {
                "systolic_average": None,
                "diastolic_average": None,
                "systolic_median": None,
                "diastolic_median": None,
            },
        )

    def test_dunder_string_method(self):
        """
        `CustomUser` model `__str__` method should return `username`.
        """
        user = CustomUser.objects.get(id=1)
        self.assertEqual(user.__str__(), user.username)
