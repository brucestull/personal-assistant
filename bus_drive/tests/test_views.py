from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from bus_drive.models import Thought


class ThoughtViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="busviewuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.other_user = CustomUser.objects.create_user(
            username="busotheruser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.thought = Thought.objects.create(user=cls.user, text="My bus drive thought")

    def setUp(self):
        self.client.login(username="busviewuser", password="testpass123")

    def test_dashboard_status_200(self):
        response = self.client.get(reverse("bus_drive:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_spa_status_200(self):
        response = self.client.get(reverse("bus_drive:spa"))
        self.assertEqual(response.status_code, 200)

    def test_list_only_own(self):
        Thought.objects.create(user=self.other_user, text="Private thought")
        response = self.client.get(reverse("bus_drive:thought-list"))
        self.assertContains(response, "My bus drive thought")
        self.assertNotContains(response, "Private thought")

    def test_detail_own_status_200(self):
        response = self.client.get(
            reverse("bus_drive:thought-detail", args=[self.thought.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_other_status_404(self):
        other_thought = Thought.objects.create(
            user=self.other_user, text="Other detail"
        )  # noqa: E501
        response = self.client.get(
            reverse("bus_drive:thought-detail", args=[other_thought.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_create_post(self):
        response = self.client.post(
            reverse("bus_drive:thought-create"),
            {"text": "Created thought"},
        )
        self.assertRedirects(response, reverse("bus_drive:thought-list"))
        self.assertTrue(
            Thought.objects.filter(user=self.user, text="Created thought").exists()
        )  # noqa: E501

    def test_update_owner_post(self):
        response = self.client.post(
            reverse("bus_drive:thought-update", args=[self.thought.pk]),
            {"text": "Updated thought"},
        )
        self.assertRedirects(response, reverse("bus_drive:thought-list"))
        self.thought.refresh_from_db()
        self.assertEqual(self.thought.text, "Updated thought")

    def test_update_other_forbidden(self):
        other_thought = Thought.objects.create(
            user=self.other_user, text="Other update"
        )  # noqa: E501
        response = self.client.post(
            reverse("bus_drive:thought-update", args=[other_thought.pk]),
            {"text": "Hacked"},
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_owner(self):
        response = self.client.post(
            reverse("bus_drive:thought-delete", args=[self.thought.pk])
        )
        self.assertRedirects(response, reverse("bus_drive:thought-list"))
        self.assertFalse(Thought.objects.filter(pk=self.thought.pk).exists())
