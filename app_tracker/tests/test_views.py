from django.test import TestCase
from django.urls import reverse


THE_SITE_NAME = "Personal Assistant"

HOME_URL = "/app-tracker/"
HOME_VIEW_NAME = "app_tracker:home"
HOME_TEMPLATE = "app_tracker/home.html"
HOME_PAGE_TITLE = "App Tracker Home"

class HomeViewTest(TestCase):
    """
    Test the `home` view.
    """

    def test_home_view_url_exists_at_desired_location(self):
        """
        Test that the `home` view is rendered at the desired location.
        """
        response = self.client.get(HOME_URL)
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_accessible_by_name(self):
        """
        Test that the `home` view is rendered at the desired location by name.
        """
        response = self.client.get(reverse(HOME_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """
        Test that the `home` view uses the correct template.
        """
        response = self.client.get(reverse(HOME_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, HOME_TEMPLATE)

    def test_home_view_uses_correct_context(self):
        """
        Test that the `home` view uses the correct context.
        """
        response = self.client.get(reverse(HOME_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)
        self.assertEqual(response.context["page_title"], HOME_PAGE_TITLE)



