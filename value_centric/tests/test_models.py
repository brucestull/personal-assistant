from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase

from value_centric.models import PersonalValue


class PersonalValueTestCase(TestCase):
    """Test the PersonalValue model."""

    def test_name_verbose_name(self):
        """Test the verbose name of the name field."""
        self.assertEqual(
            PersonalValue._meta.get_field("name").verbose_name,
            "Identifier for the Personal Value",
        )

    def test_name_max_length(self):
        """Test the max length of the name field."""
        self.assertEqual(PersonalValue._meta.get_field("name").max_length, 100)

    def test_description_verbose_name(self):
        """Test the verbose name of the description field."""
        self.assertEqual(
            PersonalValue._meta.get_field("description").verbose_name,
            "Description of the Personal Value",
        )

    def test_user_verbose_name(self):
        """Test the verbose name of the user field."""
        self.assertEqual(PersonalValue._meta.get_field("user").verbose_name, "user")

    def test_user_on_delete_cascade(self):
        """Test the on_delete behavior of the user field."""
        self.assertEqual(
            PersonalValue._meta.get_field("user").remote_field.on_delete, models.CASCADE
        )

    def test_dunder_string_method(self):
        """Test the __str__ method of the PersonalValue model."""
        user = get_user_model().objects.create_user(
            username="Dezzi", email="Dezzi@purr.scratch"
        )
        value = PersonalValue.objects.create(
            name="Control", description="Controlling all the humans!", user=user
        )
        self.assertEqual(str(value), f"{user.username}'s Value: {value.name}")

    def test_meta_verbose_name(self):
        """Test the verbose_name of the PersonalValue model."""
        self.assertEqual(PersonalValue._meta.verbose_name, "Personal Value")

    def test_meta_verbose_name_plural(self):
        """Test the verbose_name_plural of the PersonalValue model."""
        self.assertEqual(PersonalValue._meta.verbose_name_plural, "Personal Values")
