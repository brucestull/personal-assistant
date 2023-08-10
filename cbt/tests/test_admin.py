from django.contrib import admin
from django.test import TestCase
from django.test.client import RequestFactory

from accounts.models import CustomUser

from cbt.admin import CognativeDistortionAdmin
from cbt.admin import ThoughtAdmin

from cbt.models import CognativeDistortion
from cbt.models import Thought


class CognativeDistortionAdminTest(TestCase):
    """
    Tests for the CognativeDistortionAdmin class
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test.email@app.com",
            password="testpassword",
        )
        self.cognative_distortion = CognativeDistortion.objects.create(
            name="Test Cognative Distortion Name",
            description="Test Cognative Distortion Description",
        )
        self.cognative_distortion_admin = CognativeDistortionAdmin(
            CognativeDistortion, admin.site
        )

    def test_list_display(self):
        """
        Test that the list display is correct
        """
        self.assertEqual(
            self.cognative_distortion_admin.list_display,
            [
                "name",
                "truncated_description",
            ],
        )

    def test_list_filter(self):
        """
        Test that the list filter is correct
        """
        self.assertEqual(
            self.cognative_distortion_admin.list_filter,
            [
                "name",
            ],
        )

    def test_search_fields(self):
        """
        Test that the search fields are correct
        """
        self.assertEqual(
            self.cognative_distortion_admin.search_fields,
            [
                "name",
                "description",
            ],
        )

    def test_readonly_fields(self):
        """
        Test that the readonly fields are correct
        """
        self.assertEqual(
            self.cognative_distortion_admin.readonly_fields,
            [
                "created",
                "updated",
            ],
        )

    def test_fieldsets(self):
        """
        Test that the fieldsets are correct
        """
        self.assertEqual(
            self.cognative_distortion_admin.fieldsets,
            (
                (
                    "Cognative Distortion",
                    {
                        "fields": (
                            "name",
                            "description",
                        )
                    },
                ),
                (
                    "Dates/Metadata",
                    {
                        "fields": (
                            "created",
                            "updated",
                        )
                    },
                ),
            ),
        )

    def test_ordering(self):
        """
        Test that the ordering is correct
        """
        self.assertEqual(
            self.cognative_distortion_admin.ordering,
            [
                "name",
                "description",
            ],
        )

    def test_truncated_description_method(self):
        """
        Test that the truncated description is correct
        """
        self.assertEqual(
            self.cognative_distortion_admin.truncated_description(
                self.cognative_distortion
            ),
            self.cognative_distortion.description[:57] + "..."
            if len(self.cognative_distortion.description) > 57
            else self.cognative_distortion.description,
        )

