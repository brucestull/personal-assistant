from django.contrib import admin
from django.test import TestCase
from django.test.client import RequestFactory

from accounts.models import CustomUser

from cbt.admin import CognativeDistortionAdmin, ThoughtAdmin

from cbt.models import CognitiveDistortion, Thought


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
        self.cognitive_distortion = CognitiveDistortion.objects.create(
            name="Test Cognative Distortion Name",
            description="Test Cognative Distortion Description",
        )
        self.cognitive_distortion_admin = CognativeDistortionAdmin(
            CognitiveDistortion, admin.site
        )

    def test_list_display(self):
        """
        Test that the list display is correct
        """
        self.assertEqual(
            self.cognitive_distortion_admin.list_display,
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
            self.cognitive_distortion_admin.list_filter,
            [
                "name",
            ],
        )

    def test_search_fields(self):
        """
        Test that the search fields are correct
        """
        self.assertEqual(
            self.cognitive_distortion_admin.search_fields,
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
            self.cognitive_distortion_admin.readonly_fields,
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
            self.cognitive_distortion_admin.fieldsets,
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
            self.cognitive_distortion_admin.ordering,
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
            self.cognitive_distortion_admin.truncated_description(
                self.cognitive_distortion
            ),
            self.cognitive_distortion.description[:57] + "..."
            if len(self.cognitive_distortion.description) > 57
            else self.cognitive_distortion.description,
        )

    # TODO: Test the `truncated_description()` method by using a hard-coded
    # string to compare against the method's output


class ThoughtAdminTest(TestCase):
    """
    Tests for the ThoughtAdmin class
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="DezziKitten",
            email="DezziKitten@purr.scratch",
            password="MeowMeow42",
        )
        self.thought = Thought.objects.create(
            user=self.user,
            name="Test Thought Name",
            description="Test Thought Description",
        )
        self.thought_admin = ThoughtAdmin(Thought, admin.site)

    def test_list_display(self):
        """
        Test that the list display is correct
        """
        self.assertEqual(
            ThoughtAdmin.list_display,
            [
                "user",
                "name",
                "truncated_description",
            ],
        )

    def test_list_filter(self):
        """
        Test that the list filter is correct
        """
        self.assertEqual(
            ThoughtAdmin.list_filter,
            [
                "user",
                "name",
            ],
        )

    def test_search_fields(self):
        """
        Test that the search fields are correct
        """
        self.assertEqual(
            ThoughtAdmin.search_fields,
            [
                "user",
                "name",
                "description",
            ],
        )

    def test_readonly_fields(self):
        """
        Test that the readonly fields are correct
        """
        self.assertEqual(
            ThoughtAdmin.readonly_fields,
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
            ThoughtAdmin.fieldsets,
            (
                (
                    "Thought",
                    {
                        "fields": (
                            "user",
                            "name",
                            "cognitive_distortion",
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
            ThoughtAdmin.ordering,
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
            self.thought_admin.truncated_description(self.thought),
            self.thought.description[:57] + "..."
            if len(self.thought.description) > 57
            else self.thought.description,
        )

    def test_truncated_description_short_description(self):
        """
        Test that the truncated description short description is correct
        """
        self.assertEqual(
            ThoughtAdmin.truncated_description.short_description,
            "Description",
        )
