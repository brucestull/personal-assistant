from django.test import TestCase
from django.db import models as d_db_models

from pharma_tracker.models import (
    Pharmaceutical,
)
from accounts.models import CustomUser


class PharmaceuticalModelTests(TestCase):
    """
    Tests for `pharma_tracker.models.Pharmaceutical` model.
    """

    def test_user_field_uses_custom_user_model(self):
        """
        'user' field should use `accounts.CustomUser` model.
        """
        user_field = Pharmaceutical._meta.get_field("user")
        self.assertEqual(user_field.related_model, CustomUser)

    def test_user_verbose_name(self):
        """
        'user' field should have verbose name of 'User'.
        """
        user_field = Pharmaceutical._meta.get_field("user")
        self.assertEqual(user_field.verbose_name, "User")

    def test_user_help_text(self):
        """
        'user' field should have help text of 'Select the user that the
        pharmaceutical belongs to.'.
        """
        user_field = Pharmaceutical._meta.get_field("user")
        self.assertEqual(
            user_field.help_text,
            "Select the user that the pharmaceutical belongs to."
        )

    def test_user_on_delete_cascade(self):
        """
        'user' field should have on_delete of models.CASCADE.
        """
        user_field = Pharmaceutical._meta.get_field("user")
        self.assertEqual(user_field.remote_field.on_delete,
                         d_db_models.CASCADE)

    def test_name_verbose_name(self):
        """
        'name' field should have verbose name of 'Pharmaceutical Name'.
        """
        name_field = Pharmaceutical._meta.get_field("name")
        self.assertEqual(name_field.verbose_name, "Pharmaceutical Name")

    def test_name_help_text(self):
        """
        'name' field should have help text of 'Enter the name of the
        pharmaceutical.'.
        """
        name_field = Pharmaceutical._meta.get_field("name")
        self.assertEqual(
            name_field.help_text, "Enter the name of the pharmaceutical."
        )

    def test_name_max_length(self):
        """
        'name' field should have max length of 200.
        """
        name_field = Pharmaceutical._meta.get_field("name")
        self.assertEqual(name_field.max_length, 200)

    def test_description_verbose_name(self):
        """
        'description' field should have verbose name of 'Description'.
        """
        description_field = Pharmaceutical._meta.get_field("description")
        self.assertEqual(description_field.verbose_name, "Description")

    def test_description_help_text(self):
        """
        'description' field should have help text of 'Enter a description of
        the pharmaceutical.'.
        """
        description_field = Pharmaceutical._meta.get_field("description")
        self.assertEqual(
            description_field.help_text,
            "Enter a description of the pharmaceutical."
        )

    def test_description_blank_true(self):
        """
        'description' field option 'blank' should be 'True'.
        """
        description_field = Pharmaceutical._meta.get_field("description")
        self.assertTrue(description_field.blank)

    def test_description_null_true(self):
        """
        'description' field option 'null' should be 'True'.
        """
        description_field = Pharmaceutical._meta.get_field("description")
        self.assertTrue(description_field.null)

    def test_is_active_verbose_name(self):
        """
        'is_active' field should have verbose name of 'Is Active?'.
        """
        is_active_field = Pharmaceutical._meta.get_field("is_active")
        self.assertEqual(is_active_field.verbose_name, "Is Active?")

    def test_is_active_help_text(self):
        """
        'is_active' field should have help text of 'Designates if this
        pharmaceutical is currently active.'.
        """
        is_active_field = Pharmaceutical._meta.get_field("is_active")
        self.assertEqual(
            is_active_field.help_text,
            "Designates if this pharmaceutical is currently active."
        )

    def test_is_active_default_true(self):
        """
        'is_active' field option 'default' should be 'True'.
        """
        is_active_field = Pharmaceutical._meta.get_field("is_active")
        self.assertTrue(is_active_field.default)

    def test_prescription_required_verbose_name(self):
        """
        'prescription_required' field should have verbose name of
        'Prescription Required?'.
        """
        prescription_required_field = Pharmaceutical._meta.get_field(
            "prescription_required"
        )
        self.assertEqual(
            prescription_required_field.verbose_name, "Prescription Required?"
        )

    def test_prescription_required_help_text(self):
        """
        'prescription_required' field should have help text of 'Designates if
        this pharmaceutical requires a prescription.'.
        """
        prescription_required_field = Pharmaceutical._meta.get_field(
            "prescription_required"
        )
        self.assertEqual(
            prescription_required_field.help_text,
            "Designates if this pharmaceutical requires a prescription."
        )

    def test_prescription_required_default_true(self):
        """
        'prescription_required' field option 'default' should be 'True'.
        """
        prescription_required_field = Pharmaceutical._meta.get_field(
            "prescription_required"
        )
        self.assertTrue(prescription_required_field.default)

    def test_dunder_string_method(self):
        """
        `__str__` method should return 'name' field.
        """
        self.test_user = CustomUser.objects.create_user(
            username="DezziKitten",
            email="DezziKitten@purr.scratch",
            password="MeowMeow42",
        )
        self.test_pharmaceutical = Pharmaceutical.objects.create(
            user=self.test_user,
            name="Test Pharmaceutical",
        )
        self.assertEqual(str(self.test_pharmaceutical), "Test Pharmaceutical")

    def test_meta_verbose_name(self):
        """
        `Meta` class should have verbose name of 'Pharmaceutical'.
        """
        self.assertEqual(Pharmaceutical._meta.verbose_name, "Pharmaceutical")

    def test_meta_verbose_name_plural(self):
        """
        `Meta` class should have verbose name plural of 'Pharmaceuticals'.
        """
        self.assertEqual(
            Pharmaceutical._meta.verbose_name_plural, "Pharmaceuticals"
        )
