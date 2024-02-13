from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from app_tracker.models import OrganizationalConcept


class HomeViewTest(TestCase):
    """
    Test the `home` view.
    """

    def test_home_view_url_exists_at_desired_location(self):
        """
        Test that the `home` view is rendered at "/app-tracker/".
        """
        response = self.client.get("/app-tracker/")
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_accessible_by_name(self):
        """
        Test that the `home` view is rendered at the desired location by
        "app_tracker:home".
        """
        response = self.client.get(reverse("app_tracker:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """
        Test that the `home` view uses the correct template "app_tracker/home.html".
        """
        response = self.client.get(reverse("app_tracker:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_tracker/home.html")

    def test_home_view_uses_correct_context(self):
        """
        Test that the `home` view uses the correct context.

        The context should contain the following:
        - the_site_name
        - page_title
        """
        response = self.client.get(reverse("app_tracker:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")
        self.assertEqual(response.context["page_title"], "App Tracker Home")


class OrganizationalConceptListViewTest(TestCase):
    """
    Tests for the `OrganizationalConceptListView`.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up the test data for the `OrganizationalConceptListView` tests.
        """
        cls.user_registration_accepted_true = CustomUser.objects.create_user(
            username="RegisteredUser",
            password="password",
            registration_accepted=True,
        )

    def test_view_uses_correct_model(self):
        """
        Test that the `OrganizationalConceptListView` uses the correct model.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="password",
        )
        self.assertTrue(login)
        response = self.client.get(reverse("app_tracker:organizational-concepts"))
        self.assertEqual(response.status_code, 200)
        for object in response.context["object_list"]:
            self.assertEqual(object.__class__.__name__, "OrganizationalConcept")
        # Alternative test:
        self.assertEqual(response.context["object_list"].model, OrganizationalConcept)

    def test_view_context_has_the_site_name(self):
        """
        Test that the `OrganizationalConceptListView` context contains the
        `the_site_name` variable.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="password",
        )
        self.assertTrue(login)
        response = self.client.get(reverse("app_tracker:organizational-concepts"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")

    def test_view_context_has_page_title(self):
        """
        Test that the `OrganizationalConceptListView` context contains the
        `page_title` variable.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="password",
        )
        self.assertTrue(login)
        response = self.client.get(reverse("app_tracker:organizational-concepts"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_title"], "Organizational Concepts")

    def test_view_uses_correct_template(self):
        """
        Test that the `OrganizationalConceptListView` uses the correct template.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="password",
        )
        self.assertTrue(login)
        response = self.client.get(reverse("app_tracker:organizational-concepts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_tracker/organizationalconcept_list.html")
