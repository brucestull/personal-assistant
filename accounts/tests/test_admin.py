from django.test import TestCase

from accounts.models import CustomUser
from accounts.admin import CustomUserAdmin


A_TEST_USERNAME = 'ACustomUser'
A_TEST_PASSWORD = 'a_test_password'
A_TEST_FIRST_NAME = 'A'

ANOTHER_TEST_USERNAME = 'AnotherCustomUser'
ANOTHER_TEST_PASSWORD = 'another_test_password'
ANOTHER_TEST_FIRST_NAME = 'Another'

class TestCustomUserAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.

        This specific function name `setUpTestData` is required by Django.
        """
        cls.user = CustomUser.objects.create(
            username=A_TEST_USERNAME,
            first_name=A_TEST_FIRST_NAME,
        )

    def test_list_display_includes_username(self):
        """
        `CustomUserAdmin` `list_display` should include `username`.
        """
        custom_user_admin = CustomUserAdmin(CustomUser, None)
        self.assertIn("username", custom_user_admin.list_display)

    def test_list_display_includes_email(self):
        """
        `CustomUserAdmin` `list_display` should include `email`.
        """
        custom_user_admin = CustomUserAdmin(CustomUser, None)
        self.assertIn("email", custom_user_admin.list_display)

    def test_list_display_includes_registration_accepted(self):
        """
        `CustomUserAdmin` `list_display` should include `registration_accepted`.
        """
        custom_user_admin = CustomUserAdmin(CustomUser, None)
        self.assertIn("registration_accepted", custom_user_admin.list_display)

    def test_list_display_includes_is_staff(self):
        """
        `CustomUserAdmin` `list_display` should include `is_staff`.
        """
        custom_user_admin = CustomUserAdmin(CustomUser, None)
        self.assertIn("is_staff", custom_user_admin.list_display)

    def test_get_fieldsets_is_list_of_tuples(self):
        """
        `CustomUserAdmin` `get_fieldsets()` method should return a list of tuples.
        """
        custom_user_admin = CustomUserAdmin(CustomUser, None)
        fieldsets = custom_user_admin.get_fieldsets(request=None, obj=None)
        self.assertIsInstance(fieldsets, list)
        self.assertIsInstance(fieldsets[0], tuple)

    def test_get_fieldsets_has_moderator_permissions_in_second_element(self):
        """
        `CustomUserAdmin` `get_fieldsets()` method should return a list of tuples that includes `Moderator Permissions`.
        """
        custom_user_admin = CustomUserAdmin(CustomUser, None)
        fieldsets = custom_user_admin.get_fieldsets(request=None, obj=None)
        fieldsets_as_list = list(fieldsets)
        self.assertIn("Moderator Permissions", fieldsets_as_list[1])

