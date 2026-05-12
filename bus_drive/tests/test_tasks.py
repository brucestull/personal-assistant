from unittest.mock import patch

from django.test import TestCase

from accounts.models import CustomUser
from bus_drive.models import Thought
from bus_drive.tasks import send_thought_email


class SendThoughtEmailTest(TestCase):
    def test_returns_ok_and_sends_email(self):
        user = CustomUser.objects.create_user(
            username="busmailuser",
            password="testpass123",
            email="busmail@example.com",
            registration_accepted=True,
        )
        thought = Thought.objects.create(user=user, text="Email this thought")

        with patch("bus_drive.tasks._send_email") as mock_send:
            result = send_thought_email(user.id, thought.id)

        self.assertTrue(result["ok"])
        self.assertEqual(result["thought_id"], thought.id)
        self.assertEqual(result["user_id"], user.id)
        mock_send.assert_called_once()
        self.assertIn("Email this thought", mock_send.call_args[0][0])
        self.assertIn("Email this thought", mock_send.call_args[0][1])
        self.assertEqual(mock_send.call_args[0][2], [user.email])

    def test_returns_error_when_user_not_found(self):
        result = send_thought_email(99999, 1)
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "user_not_found")

    def test_returns_error_when_user_has_no_email(self):
        user = CustomUser.objects.create_user(
            username="nobusmail",
            password="testpass123",
            registration_accepted=True,
        )
        thought = Thought.objects.create(user=user, text="No email")

        result = send_thought_email(user.id, thought.id)

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "no_user_email")

    def test_returns_error_when_thought_not_found_for_user(self):
        user = CustomUser.objects.create_user(
            username="busowner",
            password="testpass123",
            email="busowner@example.com",
            registration_accepted=True,
        )
        other = CustomUser.objects.create_user(
            username="busother",
            password="testpass123",
            email="busother@example.com",
            registration_accepted=True,
        )
        thought = Thought.objects.create(user=other, text="Other thought")

        result = send_thought_email(user.id, thought.id)

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "thought_not_found_for_user")
