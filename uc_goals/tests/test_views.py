from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from uc_goals.models import Goal


class GoalDetailViewTest(TestCase):
    def setUp(self):
        # Create two users
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="password123", registration_accepted=True)
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="password123", registration_accepted=True)

        # Create goals for both users
        self.goal1 = Goal.objects.create(user=self.user1, name="Goal User 1")
        self.goal2 = Goal.objects.create(user=self.user2, name="Goal User 2")

    def test_goal_detail_view_authenticated_user(self):
        """Test that the view only returns goals owned by the authenticated user"""
        self.client.login(username="user1", password="password123")
        response = self.client.get(
            reverse("uc_goals:goal_detail", kwargs={"pk": self.goal1.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["goal"].name, "Goal User 1")
        self.assertEqual(response.context["page_title"], "Goal User 1")
        self.assertIn("the_site_name", response.context)

    def test_goal_detail_view_forbidden_for_other_user(self):
        """Test that a user cannot access another user's goal"""
        self.client.login(username="user1", password="password123")
        response = self.client.get(
            reverse("uc_goals:goal_detail", kwargs={"pk": self.goal2.pk}))

        self.assertEqual(response.status_code, 404)

    def test_goal_detail_view_requires_authentication(self):
        """Test that unauthenticated users are redirected"""
        response = self.client.get(
            reverse("uc_goals:goal_detail", kwargs={"pk": self.goal1.pk}))

        self.assertNotEqual(response.status_code, 200)  # Should redirect or deny access
        self.assertIn(response.status_code, [302, 403])
