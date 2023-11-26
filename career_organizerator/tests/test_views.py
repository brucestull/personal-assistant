from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from career_organizerator.models import (
    Purpose,
)
from career_organizerator.forms import (
    PurposeForm,
)


class HomeViewTests(TestCase):
    """
    Tests for the `home` view.
    """

    def test_home_view(self):
        """
        Test that the `home` view returns a response with an HTTP status code
        of 200.
        """
        response = self.client.get(reverse_lazy("career_organizerator:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """
        Test that the `home` view uses the correct template.
        """
        response = self.client.get(reverse_lazy("career_organizerator:home"))
        self.assertTemplateUsed(response, "career_organizerator/home.html")

    def test_home_view_context(self):
        """
        Test that the `home` view passes the correct context to the template.
        """
        response = self.client.get(reverse_lazy("career_organizerator:home"))
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")
        self.assertEqual(response.context["page_title"], "Career Organizerator Home")


class PurposeListViewTests(TestCase):
    """
    Tests for the `PurposeListView` view.
    """

    def setUp(self):
        """
        Create a user.
        """
        self.registered_user = get_user_model().objects.create_user(
            username="RegisteredKitten",
            email="RegisteredKitten@purr.scratch",
            password="MeowMeow42",
            registration_accepted=True,
        )
        self.unregistered_user = get_user_model().objects.create_user(
            username="UnRegisteredKitten",
            email="UnRegisteredKitten@purr.scratch",
            password="MeowMeow42",
            registration_accepted=False,
        )
        self.registered_user_purpose = Purpose.objects.create(
            user=self.registered_user,
            text="To create a test purpose.",
        )
        # self.client.login(username="RegisteredKitten", password="MeowMeow42")

    def test_purpose_list_view(self):
        """
        Test that the `PurposeListView` view returns a response with an HTTP
        status code of 200.
        """
        # Login the registered user.
        self.client.login(username="RegisteredKitten", password="MeowMeow42")
        response = self.client.get(reverse_lazy("career_organizerator:purpose-list"))
        self.assertEqual(response.status_code, 200)

    # def test_purpose_list_view_template(self):
    #     """
    #     Test that the `PurposeListView` view uses the correct template.
    #     """
    #     response = self.client.get(reverse_lazy("career_organizerator:purpose-list"))
    #     self.assertTemplateUsed(response, "career_organizerator/purpose_list.html")

    def test_view_for_registered_user(self):
        """
        Test that the `PurposeListView` view returns a response with an HTTP
        status code of 200 for a registered user.
        """
        # Login the registered user.
        self.client.login(username="RegisteredKitten", password="MeowMeow42")
        response = self.client.get(reverse_lazy("career_organizerator:purpose-list"))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the correct context.
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")
        self.assertEqual(response.context["page_title"], "Purposes")
        # Check that the response contains the correct template.
        self.assertTemplateUsed(response, "career_organizerator/purpose_list.html")
        # Check that the response contains the correct `Purpose` objects.
        self.assertQuerysetEqual(
            response.context["object_list"],
            Purpose.objects.filter(user=self.registered_user).order_by("-created"),
            transform=lambda x: x,
        )
        # Check that the response context has one `Purpose` object.
        self.assertEqual(len(response.context["object_list"]), 1)
        # Check that the response context doesn't have more than one `Purpose`
        # object.
        self.assertLessEqual(len(response.context["object_list"]), 1)
        # Check that the response contains the correct form.
        self.assertIsInstance(response.context["form"], PurposeForm)
