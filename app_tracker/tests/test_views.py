from django.test import TestCase
from django.urls import reverse


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
