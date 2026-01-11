"""Tests for successes app admin configuration."""

from django.contrib import admin
from django.test import TestCase

from successes.admin import SuccessAdmin, WhatWentWellAdmin
from successes.models import Success, WhatWentWell


class AdminRegistrationTests(TestCase):
    """Test that models are properly registered in admin."""

    def test_success_admin_registered(self):
        """Test Success model is registered with admin."""
        self.assertIn(Success, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Success], SuccessAdmin)

    def test_what_went_well_admin_registered(self):
        """Test WhatWentWell model is registered with admin."""
        self.assertIn(WhatWentWell, admin.site._registry)
        self.assertIsInstance(admin.site._registry[WhatWentWell], WhatWentWellAdmin)


class SuccessAdminConfigTests(TestCase):
    """Test SuccessAdmin configuration."""

    def setUp(self):
        self.admin = SuccessAdmin(Success, admin.site)

    def test_list_display(self):
        """Test list_display configuration."""
        expected = ("display_text", "user", "created", "updated")
        self.assertEqual(self.admin.list_display, expected)

    def test_list_filter(self):
        """Test list_filter configuration."""
        expected = ("user", "created")
        self.assertEqual(self.admin.list_filter, expected)

    def test_search_fields(self):
        """Test search_fields configuration."""
        expected = ("text", "user__username")
        self.assertEqual(self.admin.search_fields, expected)

    def test_ordering(self):
        """Test ordering configuration."""
        expected = ("-created",)
        self.assertEqual(self.admin.ordering, expected)

    def test_readonly_fields(self):
        """Test readonly_fields configuration."""
        expected = ("created", "updated")
        self.assertEqual(self.admin.readonly_fields, expected)

    def test_fieldsets(self):
        """Test fieldsets configuration."""
        self.assertEqual(len(self.admin.fieldsets), 2)
        # Check main fieldset
        self.assertEqual(self.admin.fieldsets[0][0], None)
        self.assertIn("user", self.admin.fieldsets[0][1]["fields"])
        self.assertIn("text", self.admin.fieldsets[0][1]["fields"])
        # Check timestamps fieldset
        self.assertEqual(self.admin.fieldsets[1][0], "Timestamps")
        self.assertIn("collapse", self.admin.fieldsets[1][1]["classes"])


class WhatWentWellAdminConfigTests(TestCase):
    """Test WhatWentWellAdmin configuration."""

    def setUp(self):
        self.admin = WhatWentWellAdmin(WhatWentWell, admin.site)

    def test_list_display(self):
        """Test list_display configuration."""
        expected = ("display_what_went_well", "user", "created", "updated")
        self.assertEqual(self.admin.list_display, expected)

    def test_list_filter(self):
        """Test list_filter configuration."""
        expected = ("user", "created")
        self.assertEqual(self.admin.list_filter, expected)

    def test_search_fields(self):
        """Test search_fields configuration."""
        expected = ("what_went_well", "how_i_made_it_happen", "user__username")
        self.assertEqual(self.admin.search_fields, expected)

    def test_ordering(self):
        """Test ordering configuration."""
        expected = ("-created",)
        self.assertEqual(self.admin.ordering, expected)

    def test_readonly_fields(self):
        """Test readonly_fields configuration."""
        expected = ("created", "updated")
        self.assertEqual(self.admin.readonly_fields, expected)

    def test_fieldsets(self):
        """Test fieldsets configuration."""
        self.assertEqual(len(self.admin.fieldsets), 2)
        # Check main fieldset
        self.assertEqual(self.admin.fieldsets[0][0], None)
        self.assertIn("user", self.admin.fieldsets[0][1]["fields"])
        self.assertIn("what_went_well", self.admin.fieldsets[0][1]["fields"])
        self.assertIn("how_i_made_it_happen", self.admin.fieldsets[0][1]["fields"])
        # Check timestamps fieldset
        self.assertEqual(self.admin.fieldsets[1][0], "Timestamps")
        self.assertIn("collapse", self.admin.fieldsets[1][1]["classes"])
