from django.test import TestCase

from accounts.models import CustomUser
from bus_drive.models import Thought


class ThoughtModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="busmodeluser",
            password="testpass123",
            registration_accepted=True,
        )

    def test_str_truncates_to_50_chars(self):
        thought = Thought.objects.create(user=self.user, text="A" * 60)
        self.assertEqual(str(thought), "A" * 50)

    def test_user_cascade_delete(self):
        Thought.objects.create(user=self.user, text="test")
        self.assertEqual(Thought.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Thought.objects.count(), 0)
