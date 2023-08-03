from django.test import TestCase, RequestFactory
from django.urls import reverse
from app_tracker.views import home


class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_home_view(self):
        request = self.factory.get(reverse("home"))
        response = home(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_tracker/home.html")
        self.assertContains(response, "App Tracker Home")
        self.assertContains(response, "Welcome to the App Tracker")
