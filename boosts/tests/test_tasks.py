# test_tasks.py
from unittest import mock
from django.test import TestCase, override_settings
from boosts.tasks import send_inspirational_to_beastie


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
class SendInspirationalToBeastieTest(TestCase):
    @mock.patch("boosts.tasks.send_mail")
    def test_send_inspirational_to_beastie(self, mock_send_mail):
        # Arrange
        user_username = "user123"
        user_email = "user@example.com"
        user_beastie_email = "beastie@example.com"
        user_beastie_username = "beastie123"
        message = "Keep pushing forward!"

        # Act
        send_inspirational_to_beastie(
            user_username,
            user_email,
            user_beastie_email,
            user_beastie_username,
            message,
        )

        # Assert
        self.assertEqual(mock_send_mail.call_count, 2)
        first_call_args, first_call_kwargs = mock_send_mail.call_args_list[0]
        second_call_args, second_call_kwargs = mock_send_mail.call_args_list[1]

        # Check first email (to beastie)
        self.assertEqual(
            first_call_args[0],
            f"Inspirational Quote from your Beastie: {user_username}",
        )
        self.assertEqual(first_call_args[1], message)
        self.assertEqual(first_call_args[2], user_email)
        self.assertEqual(first_call_args[3], [user_beastie_email])

        # Check second email (to user)
        self.assertEqual(
            second_call_args[0],
            f"You Sent an Inspirational Quote to your Beastie: {user_beastie_username}",
        )
        self.assertEqual(second_call_args[1], message)
        self.assertEqual(second_call_args[2], user_email)
        self.assertEqual(second_call_args[3], [user_email])
