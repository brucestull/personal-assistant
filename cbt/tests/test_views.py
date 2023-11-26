from django.test import TestCase
from django.urls import reverse


THE_SITE_NAME = "Personal Assistant"

HOME_URL = "/cbt/"
HOME_VIEW_NAME = "cbt:home"
HOME_TEMPLATE = "cbt/home.html"
HOME_PAGE_TITLE = "Cognitive Behavioral Therapy"


class HomeViewTest(TestCase):
    """
    Tests for `home` view.
    """

    def test_home_view_url_exists_at_desired_location(self):
        """
        Test that home view exists at desired location.
        """
        response = self.client.get(HOME_URL)
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_accessible_by_name(self):
        """
        Test that home view is accessible by name.
        """
        response = self.client.get(reverse(HOME_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """
        Test that home view uses correct template.
        """
        response = self.client.get(reverse(HOME_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, HOME_TEMPLATE)

    def test_home_view_has_correct_context(self):
        """
        Test that home view has correct context.
        """
        response = self.client.get(reverse(HOME_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)
        self.assertEqual(response.context["page_title"], HOME_PAGE_TITLE)
