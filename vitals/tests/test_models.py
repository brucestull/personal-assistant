from django.db import models as d_db_models
from django.test import TestCase

from accounts.models import CustomUser
from vitals.models import BloodPressure, Pulse, Temperature, BodyWeight

BLANK = ""

TEST_USERNAME = "test_username"
TEST_PASSWORD = "test_password"
TEST_FIRST_NAME = "Test"

BLOOD_PRESSURE_SYSTOLIC_1 = 120
BLOOD_PRESSURE_DIASTOLIC_1 = 80
BLOOD_PRESSURE_PULSE_1 = 71
BLOOD_PRESSURE_SYSTOLIC_2 = 110
BLOOD_PRESSURE_DIASTOLIC_2 = 70
BLOOD_PRESSURE_PULSE_2 = 71
BLOOD_PRESSURE_SYSTOLIC_3 = 115
BLOOD_PRESSURE_DIASTOLIC_3 = 75
BLOOD_PRESSURE_PULSE_3 = 71

BLOOD_PRESSURE_SYSTOLIC_AVERAGE = 115
BLOOD_PRESSURE_DIASTOLIC_AVERAGE = 75
BLOOD_PRESSURE_SYSTOLIC_MEDIAN = 115
BLOOD_PRESSURE_DIASTOLIC_MEDIAN = 75


PULSE_1 = 65
PULSE_2 = 70

BLOOD_PRESSURE_USER_LABEL = "user"
BLOOD_PRESSURE_USER_RELATED_NAME = "blood_pressures"
BLOOD_PRESSURE_USER_HELP_TEXT = "The user that measures their blood pressure."

BLOOD_PRESSURE_SYSTOLIC_LABEL = "Systolic Blood Pressure"
BLOOD_PRESSURE_SYSTOLIC_HELP_TEXT = "The systolic blood pressure reading."

BLOOD_PRESSURE_DIASTOLIC_LABEL = "Diastolic Blood Pressure"
BLOOD_PRESSURE_DIASTOLIC_HELP_TEXT = "The diastolic blood pressure reading."

BLOOD_PRESSURE_PULSE_LABEL = "Pulse"
BLOOD_PRESSURE_PULSE_HELP_TEXT = "The pulse rate in beats per minute."

BLOOD_PRESSURE_VERBOSE_NAME_PLURAL = "Blood Pressure Measurements"

PULSE_USER_LABEL = "user"
PULSE_USER_RELATED_NAME = "pulses"
PULSE_USER_HELP_TEXT = "The user that measures their pulse."

PULSE_BPM_LABEL = "bpm"
PULSE_BPM_VERBOSE_NAME = "Beats Per Minute"
PULSE_BPM_HELP_TEXT = "The pulse reading."

PULSE_VERBOSE_NAME = "Pulse Measurement"
PULSE_VERBOSE_NAME_PLURAL = "Pulse Measurements"

TEMPERATURE_SUBJECT_VERBOSE_NAME = "Subject"
TEMPERATURE_SUBJECT_RELATED_NAME = "temperatures"
TEMPERATURE_SUBJECT_HELP_TEXT = "The subject that gets their temperature measured."

TEMPERATURE_MEASUREMENT_VERBOSE_NAME = "Temperature Measurement"
TEMPERATURE_MEASUREMENT_MAX_DIGITS = 4
TEMPERATURE_MEASUREMENT_DECIMAL_PLACES = 1
TEMPERATURE_MEASUREMENT_HELP_TEXT = "The temperature measurement in degrees Fahrenheit."

TEMPERATURE_VERBOSE_NAME = "Temperature Measurement"
TEMPERATURE_VERBOSE_NAME_PLURAL = "Temperature Measurements"

TEMPERATURE_1 = 98.6


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

    def test_created_field_name(self):
        """
        Test the `created` field name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        created_field_name = blood_pressure._meta.get_field("created").name
        self.assertEqual(created_field_name, "created")

    def test_created_field_verbose_name(self):
        """
        Test the `created` field verbose name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        created_field_verbose_name = blood_pressure._meta.get_field(
            "created"
        ).verbose_name
        self.assertEqual(created_field_verbose_name, "Created")

    def test_created_field_help_text(self):
        """
        Test the `created` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        created_field_help_text = blood_pressure._meta.get_field("created").help_text
        self.assertEqual(
            created_field_help_text,
            "The date and time this object was created.",
        )

    def test_created_field_auto_now_add_true(self):
        """
        Test the `created` field auto_now_add=True.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        created_field_auto_now_add = blood_pressure._meta.get_field(
            "created"
        ).auto_now_add
        self.assertTrue(created_field_auto_now_add)

    def test_updated_field_name(self):
        """
        Test the `updated` field name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        updated_field_name = blood_pressure._meta.get_field("updated").name
        self.assertEqual(updated_field_name, "updated")

    def test_updated_field_verbose_name(self):
        """
        Test the `updated` field verbose name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        updated_field_verbose_name = blood_pressure._meta.get_field(
            "updated"
        ).verbose_name
        self.assertEqual(updated_field_verbose_name, "Updated")

    def test_updated_field_help_text(self):
        """
        Test the `updated` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        updated_field_help_text = blood_pressure._meta.get_field("updated").help_text
        self.assertEqual(
            updated_field_help_text,
            "The date and time this object was last updated.",
        )

    def test_updated_field_auto_now_true(self):
        """
        Test the `updated` field auto_now=True.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        updated_field_auto_now = blood_pressure._meta.get_field("updated").auto_now
        self.assertTrue(updated_field_auto_now)

    def test_uses_correct_user_model(self):
        """
        Test the `user` field uses the correct user model.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        user_field = blood_pressure._meta.get_field("user")
        self.assertEqual(user_field.related_model, CustomUser)

    def test_user_label(self):
        """
        Test the `user` field label.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        user_label = blood_pressure._meta.get_field(
            BLOOD_PRESSURE_USER_LABEL
        ).verbose_name
        self.assertEqual(user_label, BLOOD_PRESSURE_USER_LABEL)

    def test_user_on_delete_cascade(self):
        """
        Test the `user` field on_delete=cascade.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        user_on_delete = blood_pressure._meta.get_field(
            BLOOD_PRESSURE_USER_LABEL
        ).remote_field.on_delete
        self.assertEqual(user_on_delete, d_db_models.CASCADE)

    def test_user_related_name(self):
        """
        Test the `user` field related name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        user_related_name = blood_pressure._meta.get_field(
            BLOOD_PRESSURE_USER_LABEL
        ).remote_field.related_name
        self.assertEqual(user_related_name, BLOOD_PRESSURE_USER_RELATED_NAME)

    def test_user_help_text(self):
        """
        Test the `user` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        user_help_text = blood_pressure._meta.get_field(
            BLOOD_PRESSURE_USER_LABEL
        ).help_text
        self.assertEqual(user_help_text, BLOOD_PRESSURE_USER_HELP_TEXT)

    def test_systolic_field_name(self):
        """
        Test the `systolic` field name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        systolic_field_name = blood_pressure._meta.get_field("systolic").name
        self.assertEqual(systolic_field_name, "systolic")

    def test_systolic_field_verbose_name(self):
        """
        Test the `systolic` field verbose name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        systolic_field_verbose_name = blood_pressure._meta.get_field(
            "systolic"
        ).verbose_name
        self.assertEqual(systolic_field_verbose_name, "Systolic Blood Pressure")

    def test_systolic_field_help_text(self):
        """
        Test the `systolic` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        systolic_field_help_text = blood_pressure._meta.get_field("systolic").help_text
        self.assertEqual(
            systolic_field_help_text, "The systolic blood pressure reading."
        )

    def test_diastolic_field_name(self):
        """
        Test the `diastolic` field name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        diastolic_field_name = blood_pressure._meta.get_field("diastolic").name
        self.assertEqual(diastolic_field_name, "diastolic")

    def test_diastolic_field_verbose_name(self):
        """
        Test the `diastolic` field verbose name.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        diastolic_field_verbose_name = blood_pressure._meta.get_field(
            "diastolic"
        ).verbose_name
        self.assertEqual(diastolic_field_verbose_name, BLOOD_PRESSURE_DIASTOLIC_LABEL)

    def test_diastolic_field_help_text(self):
        """
        Test the `diastolic` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        diastolic_field_help_text = blood_pressure._meta.get_field(
            "diastolic"
        ).help_text
        self.assertEqual(
            diastolic_field_help_text, "The diastolic blood pressure reading."
        )

    def test_pulse_field_verbose_name(self):
        """
        Test the verbose name of the `Pulse` model.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        pulse_field_verbose_name = blood_pressure._meta.get_field("pulse").verbose_name
        self.assertEqual(pulse_field_verbose_name, BLOOD_PRESSURE_PULSE_LABEL)

    def test_pulse_field_help_text(self):
        """
        Test the `pulse` field help text.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        pulse_field_help_text = blood_pressure._meta.get_field("pulse").help_text
        self.assertEqual(pulse_field_help_text, BLOOD_PRESSURE_PULSE_HELP_TEXT)

    def test_verbose_name_plural(self):
        """
        Test the plural verbose name of the `BloodPressure` model.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        self.assertEqual(
            str(blood_pressure._meta.verbose_name_plural),
            BLOOD_PRESSURE_VERBOSE_NAME_PLURAL,
        )

    def test_dunder_string_method(self):
        """
        Test the `__str__` method of the `BloodPressure` model.
        """
        blood_pressure = BloodPressure.objects.get(id=self.blood_pressure_1.pk)
        self.assertEqual(
            str(blood_pressure),
            (
                f"{blood_pressure.user.username} | "
                f"{blood_pressure.systolic} / "
                f"{blood_pressure.diastolic} mmHg | "
                f"{blood_pressure.pulse} bpm"
            ),
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
            bpm=PULSE_1,
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


class TemperatureModelTest(TestCase):
    """
    Test the `Temperature` model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Sets up data for the whole TestCase.
        """
        cls.subject = CustomUser.objects.create_user(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            first_name=TEST_FIRST_NAME,
        )
        cls.temperature = Temperature.objects.create(
            subject=cls.subject,
            measurement=TEMPERATURE_1,
        )

    def test_temperature_subject_uses_correct_user_model(self):
        """
        Test the `subject` field uses the correct user model.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        subject_field = temperature._meta.get_field("subject")
        self.assertEqual(subject_field.related_model, CustomUser)

    def test_temperature_subject_verbose_name(self):
        """
        Test the `subject` field verbose_name.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        subject_label = temperature._meta.get_field("subject").verbose_name
        self.assertEqual(subject_label, TEMPERATURE_SUBJECT_VERBOSE_NAME)

    def test_temperature_subject_on_delete_cascade(self):
        """
        Test the `subject` field on_delete=cascade.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        subject_on_delete = temperature._meta.get_field(
            "subject"
        ).remote_field.on_delete
        self.assertEqual(subject_on_delete, d_db_models.CASCADE)

    def test_temperature_subject_related_name(self):
        """
        Test the `subject` field related name.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        subject_related_name = temperature._meta.get_field(
            "subject"
        ).remote_field.related_name
        self.assertEqual(
            subject_related_name,
            TEMPERATURE_SUBJECT_RELATED_NAME,
        )

    def test_temperature_subject_help_text(self):
        """
        Test the `subject` field help text.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        subject_help_text = temperature._meta.get_field("subject").help_text
        self.assertEqual(subject_help_text, TEMPERATURE_SUBJECT_HELP_TEXT)

    def test_temperature_measurement_field_name(self):
        """
        Test the `measurement` field name.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        measurement_field_name = temperature._meta.get_field("measurement").name
        self.assertEqual(measurement_field_name, "measurement")

    def test_temperature_measurement_field_verbose_name(self):
        """
        Test the `measurement` field verbose name.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        measurement_field_verbose_name = temperature._meta.get_field(
            "measurement"
        ).verbose_name
        self.assertEqual(
            measurement_field_verbose_name,
            TEMPERATURE_MEASUREMENT_VERBOSE_NAME,
        )

    def test_temperature_measurement_field_max_digits(self):
        """
        Test the `measurement` field max_digits.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        measurement_field_max_digits = temperature._meta.get_field(
            "measurement"
        ).max_digits
        self.assertEqual(
            measurement_field_max_digits,
            TEMPERATURE_MEASUREMENT_MAX_DIGITS,
        )

    def test_temperature_measurement_field_decimal_places(self):
        """
        Test the `measurement` field decimal_places.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        measurement_field_decimal_places = temperature._meta.get_field(
            "measurement"
        ).decimal_places
        self.assertEqual(
            measurement_field_decimal_places,
            TEMPERATURE_MEASUREMENT_DECIMAL_PLACES,
        )

    def test_temperature_measurement_field_help_text(self):
        """
        Test the `measurement` field help text.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        measurement_field_help_text = temperature._meta.get_field(
            "measurement"
        ).help_text
        self.assertEqual(
            measurement_field_help_text,
            TEMPERATURE_MEASUREMENT_HELP_TEXT,
        )

    def test_temperature_meta_verbose_name(self):
        """
        Test the verbose name of the `Temperature` model.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        self.assertEqual(
            str(temperature._meta.verbose_name),
            TEMPERATURE_VERBOSE_NAME,
        )

    def test_temperature_meta_verbose_name_plural(self):
        """
        Test the plural verbose name of the `Temperature` model.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        self.assertEqual(
            str(temperature._meta.verbose_name_plural),
            TEMPERATURE_VERBOSE_NAME_PLURAL,
        )

    def test_temperature_dunder_string_method(self):
        """
        Test the `__str__` method of the `Temperature` model.
        """
        temperature = Temperature.objects.get(id=self.temperature.pk)
        self.assertEqual(
            str(temperature),
            f"{temperature.subject.username} | {temperature.measurement}°F",
        )


class BodyWeightModelTest(TestCase):
    """
    Test the `BodyWeight` model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Sets up data for the whole TestCase.
        """
        cls.subject = CustomUser.objects.create_user(
            username="DezziKitten",
            password="MeowMeow42",
            email="DezziKitten@purr.scratch",
        )
        cls.body_weight = BodyWeight.objects.create(
            subject=cls.subject,
            measurement=6.1,
        )

    def test_body_weight_subject_uses_correct_user_model(self):
        """
        Test the `subject` field uses the correct user model.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        subject_field = body_weight._meta.get_field("subject")
        self.assertEqual(subject_field.related_model, CustomUser)

    def test_body_weight_subject_verbose_name(self):
        """
        Test the `subject` field verbose_name.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        subject_label = body_weight._meta.get_field("subject").verbose_name
        self.assertEqual(subject_label, "Subject")

    def test_body_weight_subject_on_delete_cascade(self):
        """
        Test the `subject` field on_delete=cascade.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        subject_on_delete = body_weight._meta.get_field(
            "subject"
        ).remote_field.on_delete
        self.assertEqual(subject_on_delete, d_db_models.CASCADE)

    def test_body_weight_subject_related_name(self):
        """
        Test the `subject` field related name.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        subject_related_name = body_weight._meta.get_field(
            "subject"
        ).remote_field.related_name
        self.assertEqual(subject_related_name, "body_weights")

    def test_body_weight_subject_help_text(self):
        """
        Test the `subject` field help text.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        subject_help_text = body_weight._meta.get_field("subject").help_text
        self.assertEqual(
            subject_help_text,
            "The subject that gets their body weight measured.",
        )

    def test_body_weight_measurement_field_name(self):
        """
        Test the `measurement` field name.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        measurement_field_name = body_weight._meta.get_field("measurement").name
        self.assertEqual(measurement_field_name, "measurement")

    def test_body_weight_measurement_field_verbose_name(self):
        """
        Test the `measurement` field verbose name.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        measurement_field_verbose_name = body_weight._meta.get_field(
            "measurement"
        ).verbose_name
        self.assertEqual(
            measurement_field_verbose_name,
            "Body Weight Measurement",
        )

    def test_body_weight_measurement_field_max_digits(self):
        """
        Test the `measurement` field max_digits.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        measurement_field_max_digits = body_weight._meta.get_field(
            "measurement"
        ).max_digits
        self.assertEqual(
            measurement_field_max_digits,
            5,
        )

    def test_body_weight_measurement_field_decimal_places(self):
        """
        Test the `measurement` field decimal_places.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        measurement_field_decimal_places = body_weight._meta.get_field(
            "measurement"
        ).decimal_places
        self.assertEqual(
            measurement_field_decimal_places,
            2,
        )

    def test_body_weight_measurement_field_help_text(self):
        """
        Test the `measurement` field help text.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        measurement_field_help_text = body_weight._meta.get_field(
            "measurement"
        ).help_text
        self.assertEqual(
            measurement_field_help_text,
            "The body weight measurement in pounds.",
        )

    def test_body_weight_meta_verbose_name(self):
        """
        Test the verbose name of the `BodyWeight` model.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        self.assertEqual(
            str(body_weight._meta.verbose_name),
            "Body Weight Measurement",
        )

    def test_body_weight_meta_verbose_name_plural(self):
        """
        Test the plural verbose name of the `BodyWeight` model.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        self.assertEqual(
            str(body_weight._meta.verbose_name_plural),
            "Body Weight Measurements",
        )

    def test_body_weight_dunder_string_method(self):
        """
        Test the `__str__` method of the `BodyWeight` model.
        """
        body_weight = BodyWeight.objects.get(id=self.body_weight.pk)
        self.assertEqual(
            str(body_weight),
            f"{body_weight.subject.username} | {body_weight.measurement} lbs",
        )
