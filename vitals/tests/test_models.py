from django.test import TestCase
from django.urls import reverse
from django.db import models as d_db_models

from accounts.models import CustomUser
from vitals.models import DateTimeBase
from vitals.models import BloodPressure
from vitals.models import Pulse


BLANK = ""

TEST_USERNAME = "test_username"
TEST_PASSWORD = "test_password"
TEST_FIRST_NAME = "Test"

BLOOD_PRESSURE_SYSTOLIC = 120
BLOOD_PRESSURE_DIASTOLIC = 80

PULSE = 65

BLOOD_PRESSURE_USER_LABEL = "user"
BLOOD_PRESSURE_USER_RELATED_NAME = "blood_pressures"
BLOOD_PRESSURE_USER_HELP_TEXT = "The user that measures their blood pressure."

BLOOD_PRESSURE_SYSTOLIC_LABEL = "Systolic Blood Pressure"
BLOOD_PRESSURE_SYSTOLIC_HELP_TEXT = "The systolic blood pressure reading."

BLOOD_PRESSURE_DIASTOLIC_LABEL = "Diastolic Blood Pressure"
BLOOD_PRESSURE_DIASTOLIC_HELP_TEXT = "The diastolic blood pressure reading."

BLOOD_PRESSURE_VERBOSE_NAME_PLURAL = "Blood Pressure Measurements"

PULSE_USER_LABEL = "user"
PULSE_USER_RELATED_NAME = "pulses"
PULSE_USER_HELP_TEXT = "The user that measures their pulse."

PULSE_BPM_LABEL = "bpm"
PULSE_BPM_VERBOSE_NAME = "Beats Per Minute"
PULSE_BPM_HELP_TEXT = "The pulse reading."

PULSE_VERBOSE_NAME = "Pulse Measurement"
PULSE_VERBOSE_NAME_PLURAL = "Pulse Measurements"


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

    def test_blood_pressure_created_field_name(self):
        """
        Test the `created` field name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        created_field_name = blood_pressure._meta.get_field("created").name
        self.assertEqual(created_field_name, "created")

    def test_blood_pressure_created_field_verbose_name(self):
        """
        Test the `created` field verbose name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        created_field_verbose_name = blood_pressure._meta.get_field(
            "created"
        ).verbose_name
        self.assertEqual(created_field_verbose_name, "Created")

    def test_blood_pressure_created_field_help_text(self):
        """
        Test the `created` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        created_field_help_text = blood_pressure._meta.get_field("created").help_text
        self.assertEqual(
            created_field_help_text, "The date and time this object was created."
        )

    def test_blood_pressure_created_field_auto_now_add_true(self):
        """
        Test the `created` field auto_now_add=True.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        created_field_auto_now_add = blood_pressure._meta.get_field(
            "created"
        ).auto_now_add
        self.assertTrue(created_field_auto_now_add)

    def test_blood_pressure_updated_field_name(self):
        """
        Test the `updated` field name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        updated_field_name = blood_pressure._meta.get_field("updated").name
        self.assertEqual(updated_field_name, "updated")

    def test_blood_pressure_updated_field_verbose_name(self):
        """
        Test the `updated` field verbose name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        updated_field_verbose_name = blood_pressure._meta.get_field(
            "updated"
        ).verbose_name
        self.assertEqual(updated_field_verbose_name, "Updated")

    def test_blood_pressure_updated_field_help_text(self):
        """
        Test the `updated` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        updated_field_help_text = blood_pressure._meta.get_field("updated").help_text
        self.assertEqual(
            updated_field_help_text, "The date and time this object was last updated."
        )

    def test_blood_pressure_updated_field_auto_now_true(self):
        """
        Test the `updated` field auto_now=True.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        updated_field_auto_now = blood_pressure._meta.get_field("updated").auto_now
        self.assertTrue(updated_field_auto_now)

    def test_blood_pressure_uses_correct_user_model(self):
        """
        Test the `user` field uses the correct user model.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        user_field = blood_pressure._meta.get_field("user")
        self.assertEqual(user_field.related_model, CustomUser)

    def test_blood_pressure_user_label(self):
        """
        Test the `user` field label.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        user_label = blood_pressure._meta.get_field(
            BLOOD_PRESSURE_USER_LABEL
        ).verbose_name
        self.assertEqual(user_label, BLOOD_PRESSURE_USER_LABEL)

    def test_blood_pressure_user_on_delete_cascade(self):
        """
        Test the `user` field on_delete=cascade.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        user_on_delete = blood_pressure._meta.get_field(
            BLOOD_PRESSURE_USER_LABEL
        ).remote_field.on_delete
        self.assertEqual(user_on_delete, d_db_models.CASCADE)

    def test_blood_pressure_user_related_name(self):
        """
        Test the `user` field related name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        user_related_name = blood_pressure._meta.get_field(
            BLOOD_PRESSURE_USER_LABEL
        ).remote_field.related_name
        self.assertEqual(user_related_name, BLOOD_PRESSURE_USER_RELATED_NAME)

    def test_blood_pressure_user_help_text(self):
        """
        Test the `user` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        user_help_text = blood_pressure._meta.get_field(
            BLOOD_PRESSURE_USER_LABEL
        ).help_text
        self.assertEqual(user_help_text, BLOOD_PRESSURE_USER_HELP_TEXT)

    def test_blood_pressure_systolic_field_name(self):
        """
        Test the `systolic` field name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        systolic_field_name = blood_pressure._meta.get_field("systolic").name
        self.assertEqual(systolic_field_name, "systolic")

    def test_blood_pressure_systolic_field_verbose_name(self):
        """
        Test the `systolic` field verbose name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        systolic_field_verbose_name = blood_pressure._meta.get_field(
            "systolic"
        ).verbose_name
        self.assertEqual(systolic_field_verbose_name, "Systolic Blood Pressure")

    def test_blood_pressure_systolic_field_help_text(self):
        """
        Test the `systolic` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        systolic_field_help_text = blood_pressure._meta.get_field("systolic").help_text
        self.assertEqual(
            systolic_field_help_text, "The systolic blood pressure reading."
        )

    def test_blood_pressure_diastolic_field_name(self):
        """
        Test the `diastolic` field name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        diastolic_field_name = blood_pressure._meta.get_field("diastolic").name
        self.assertEqual(diastolic_field_name, "diastolic")

    def test_blood_pressure_diastolic_field_verbose_name(self):
        """
        Test the `diastolic` field verbose name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        diastolic_field_verbose_name = blood_pressure._meta.get_field(
            "diastolic"
        ).verbose_name
        self.assertEqual(diastolic_field_verbose_name, BLOOD_PRESSURE_DIASTOLIC_LABEL)

    def test_blood_pressure_diastolic_field_help_text(self):
        """
        Test the `diastolic` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        diastolic_field_help_text = blood_pressure._meta.get_field(
            "diastolic"
        ).help_text
        self.assertEqual(
            diastolic_field_help_text, "The diastolic blood pressure reading."
        )

    def test_blood_pressure_verbose_name_plural(self):
        """
        Test the plural verbose name of the `BloodPressure` model.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        self.assertEqual(
            str(blood_pressure._meta.verbose_name_plural),
            BLOOD_PRESSURE_VERBOSE_NAME_PLURAL,
        )

    def test_blood_pressure_str_method(self):
        """
        Test the `__str__` method of the `BloodPressure` model.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure.pk)
        self.assertEqual(
            str(blood_pressure),
            f"{blood_pressure.user.username} | {blood_pressure.systolic}/{blood_pressure.diastolic} mmHg",
        )


class PulseModelTest(TestCase):
    """
    Test the `Pulse` model.
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
        cls.pulse = Pulse.objects.create(
            user=cls.user,
            bpm=PULSE,
        )

    def test_pulse_user_label(self):
        """
        Test the `user` field label.
        """
        pulse = Pulse.objects.get(id=self.pulse.pk)
        user_label = pulse._meta.get_field(PULSE_USER_LABEL).verbose_name
        self.assertEqual(user_label, PULSE_USER_LABEL)

    def test_pulse_user_on_delete_cascade(self):
        """
        Test the `user` field on_delete=cascade.
        """
        pulse = Pulse.objects.get(id=self.pulse.pk)
        user_on_delete = pulse._meta.get_field(PULSE_USER_LABEL).remote_field.on_delete
        self.assertEqual(user_on_delete, d_db_models.CASCADE)

    def test_pulse_user_related_name(self):
        """
        Test the `user` field related name.
        """
        pulse = Pulse.objects.get(id=self.pulse.pk)
        user_related_name = pulse._meta.get_field(
            PULSE_USER_LABEL
        ).remote_field.related_name
        self.assertEqual(user_related_name, PULSE_USER_RELATED_NAME)

    def test_pulse_user_help_text(self):
        """
        Test the `user` field help text.
        """
        pulse = Pulse.objects.get(id=self.pulse.pk)
        user_help_text = pulse._meta.get_field(PULSE_USER_LABEL).help_text
        self.assertEqual(user_help_text, PULSE_USER_HELP_TEXT)

    def test_pulse_bpm_field_name(self):
        """
        Test the `bpm` field name.
        """
        pulse = Pulse.objects.get(id=self.pulse.pk)
        bpm_field_name = pulse._meta.get_field("bpm").name
        self.assertEqual(bpm_field_name, "bpm")

    def test_pulse_bpm_field_verbose_name(self):
        """
        Test the `bpm` field verbose name.
        """
        pulse = Pulse.objects.get(id=self.pulse.pk)
        bpm_field_verbose_name = pulse._meta.get_field("bpm").verbose_name
        self.assertEqual(bpm_field_verbose_name, "Beats Per Minute")

    def test_pulse_bpm_field_help_text(self):
        """
        Test the `bpm` field help text.
        """
        pulse = Pulse.objects.get(id=self.pulse.pk)
        bpm_field_help_text = pulse._meta.get_field("bpm").help_text
        self.assertEqual(bpm_field_help_text, "The pulse rate in beats per minute.")

    def test_pulse_verbose_name(self):
        """
        Test the verbose name of the `Pulse` model.
        """
        pulse = Pulse.objects.get(id=self.pulse.pk)
        self.assertEqual(str(pulse._meta.verbose_name), PULSE_VERBOSE_NAME)

    def test_pulse_verbose_name_plural(self):
        """
        Test the plural verbose name of the `Pulse` model.
        """
        pulse = Pulse.objects.get(id=self.pulse.pk)
        self.assertEqual(
            str(pulse._meta.verbose_name_plural), PULSE_VERBOSE_NAME_PLURAL
        )

    def test_pulse_str_method(self):
        """
        Test the `__str__` method of the `Pulse` model.
        """
        pulse = Pulse.objects.get(id=self.pulse.pk)
        self.assertEqual(
            str(pulse), f"{pulse.user.username} | {pulse.bpm} Beats Per Minute"
        )
