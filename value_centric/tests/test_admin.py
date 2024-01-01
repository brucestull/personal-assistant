from django.test import TestCase

from value_centric.admin import PersonalValueAdmin


class PersonalValueAdminTestCase(TestCase):
    """Test the PersonalValueAdmin."""

    def test_list_display(self):
        """Test the list_display attribute."""
        self.assertEqual(PersonalValueAdmin.list_display, ("name", "user"))

    def test_list_filter(self):
        """Test the list_filter attribute."""
        self.assertEqual(PersonalValueAdmin.list_filter, ("user",))

    def test_search_fields(self):
        """Test the search_fields attribute."""
        self.assertEqual(PersonalValueAdmin.search_fields, ("name", "description"))
