from django.test import TestCase

from accounts.models import CustomUser
from accounts.admin import CustomUserAdmin
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm


class MockRequest:
    pass


class TestCustomUserAdmin(TestCase):
    """
    Tests for `CustomUserAdmin`.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods.

        This specific function name `setUpTestData` is required by Django.
        """
        cls.user = CustomUser.objects.create_user(
            username="DezziKitten",
            password="MeowMeow42",
        )

    def test_uses_correct_add_form(self):
        """
        `CustomUserAdmin` `add_form` should be `CustomUserCreationForm`.
        """
        custom_user_admin = CustomUserAdmin(CustomUser, None)
        self.assertEqual(custom_user_admin.add_form, CustomUserCreationForm)

    def test_uses_correct_change_form(self):
        """
        `CustomUserAdmin` `form` should be `CustomUserChangeForm`.
        """
        custom_user_admin = CustomUserAdmin(CustomUser, None)
        self.assertEqual(custom_user_admin.form, CustomUserChangeForm)

    def test_uses_correct_model(self):
        """
        `CustomUserAdmin` `model` should be `CustomUser`.
        """
        custom_user_admin = CustomUserAdmin(CustomUser, None)
        self.assertEqual(custom_user_admin.model, CustomUser)

    def test_list_display(self):
        """
        This tests that the `list_display` contains the proper fields and that they are
        in the proper order.
        """
        self.assertEqual(
            CustomUserAdmin.list_display,
            (
                "username",
                "beastie",
                "registration_accepted",
                "is_staff",
                "is_superuser",
            ),
        )

    def test_list_display_includes_proper_fields(self):
        """
        `CustomUserAdmin` `list_display` should include `username`,
        `beastie`, `registration_accepted`, `is_staff`, and
        `is_superuser`.

        This tests that the `list_display` contains the proper fields, but not
        necessarily in the proper order.
        """
        custom_user_admin = CustomUserAdmin(CustomUser, None)
        self.assertIn("username", custom_user_admin.list_display)
        self.assertIn("beastie", custom_user_admin.list_display)
        self.assertIn("registration_accepted", custom_user_admin.list_display)
        self.assertIn("is_staff", custom_user_admin.list_display)
        self.assertIn("is_superuser", custom_user_admin.list_display)

    def test_fieldsets(self):
        """
        Test the fieldsets to ensure the custom fields are included.
        """
        admin = CustomUserAdmin(CustomUser, None)
        request = MockRequest()
        fieldsets = admin.get_fieldsets(request)
        # This line does the following:
        # 1. Iterate over the `fieldsets` list.
        # 2. For each tuple in the `fieldsets` list, get the second item in the
        #    tuple.
        # 3. For each item in the second item in the tuple, get the value of
        #    the "fields" key.
        # 4. Flatten the list of lists into a single list.
        field_names = [field for _, opts in fieldsets for field in opts["fields"]]
        self.assertIn("registration_accepted", field_names)
        self.assertIn("beastie", field_names)

    def test_get_fieldsets_method(self):
        pass
