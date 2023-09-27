from django.test import TestCase

from pharma_tracker.admin import PharmaceuticalAdmin


class PharmaceuticalAdminTest(TestCase):
    """
    Test 'PharmaceuticalAdmin' class.
    """

    def test_list_display(self):
        """
        Test 'list_display' attribute.
        """
        expected = (
            "name",
            "user",
            "is_active",
            "prescription_required",
        )
        self.assertEqual(PharmaceuticalAdmin.list_display, expected)

    def test_list_filter(self):
        """
        Test 'list_filter' attribute.
        """
        expected = (
            "user",
            "name",
            "is_active",
            "prescription_required",
        )
        self.assertEqual(PharmaceuticalAdmin.list_filter, expected)

    def test_search_fields(self):
        """
        Test 'search_fields' attribute.
        """
        expected = (
            "user",
            "name",
        )
        self.assertEqual(PharmaceuticalAdmin.search_fields, expected)
