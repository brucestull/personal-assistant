from django.test import TestCase

from accounts.models import CustomUser
from bus_drive.models import Thought


class ThoughtAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="busapiuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.other_user = CustomUser.objects.create_user(
            username="busapiother",
            password="testpass123",
            registration_accepted=True,
        )

    def setUp(self):
        self.client.login(username="busapiuser", password="testpass123")

    def test_list_only_own_thoughts(self):
        mine = Thought.objects.create(user=self.user, text="Mine")
        Thought.objects.create(user=self.other_user, text="Not mine")

        response = self.client.get("/bus-drive/api/thoughts/")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["id"], mine.id)

    def test_create_assigns_current_user(self):
        response = self.client.post(
            "/bus-drive/api/thoughts/",
            data='{"text":"Created via API"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        created = Thought.objects.get(pk=response.json()["id"])
        self.assertEqual(created.user, self.user)

    def test_cannot_access_other_user_detail(self):
        other_thought = Thought.objects.create(user=self.other_user, text="Private")
        response = self.client.get(f"/bus-drive/api/thoughts/{other_thought.pk}/")
        self.assertEqual(response.status_code, 404)
