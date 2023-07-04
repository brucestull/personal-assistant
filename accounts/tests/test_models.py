from django.test import TestCase
from django.db import models

from accounts.models import CustomUser

A_TEST_USERNAME = "ACustomUser"

CUSTOM_USER_REGISTRATION_ACCEPTED_HELP_TEXT = (
    "Designates whether this user's registration has been accepted."
)


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
        user = CustomUser.objects.create(
            username=A_TEST_USERNAME,
        )

    def test_new_user_has_registration_accepted_false(self):
        """
        A newly created `CustomUser` should have `registration_accepted`
        `False`.

        This tests the actual `default` value of the `registration_accepted`
        field of a newly created user.

        This test may be redundant with `test_registration_accepted_default_attribute_false`,
        since Django makes sure to use the `registration_accepted` default
        value we specify in the model, which is tested in
        `test_registration_accepted_default_attribute_false`.
        """
        user = CustomUser.objects.get(id=1)
        self.assertFalse(user.registration_accepted)

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

    def test_dunder_string_method(self):
        """
        `CustomUser` model `__str__` method should return `username`.
        """
        user = CustomUser.objects.get(id=1)
        self.assertEqual(user.__str__(), user.username)
