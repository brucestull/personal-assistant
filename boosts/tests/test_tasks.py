# tests/test_tasks.py
from __future__ import annotations

import smtplib
from unittest import mock

from celery.exceptions import Retry
from django.core import mail
from django.test import TestCase, override_settings

from boosts.tasks import send_inspirational_to_beastie


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="no-reply@example.com",
)
class SendInspirationalToBeastieTest(TestCase):
    def setUp(self) -> None:
        # Common fixtures
        self.user_username = "user123"
        self.user_email = "user@example.com"
        self.user_beastie_email = "beastie@example.com"
        self.user_beastie_username = "beastie123"
        self.message = "Keep pushing forward!"

    def test_sends_two_emails_with_expected_contents(self):
        """
        In eager mode, calling .delay() should send two emails and they should
        have the expected subjects, bodies, recipients, and from_email.
        """
        # Act
        send_inspirational_to_beastie.delay(
            self.user_username,
            self.user_email,
            self.user_beastie_email,
            self.user_beastie_username,
            self.message,
        )

        # Assert
        self.assertEqual(len(mail.outbox), 2)

        # First email goes to Beastie
        first = mail.outbox[0]
        self.assertEqual(
            first.subject,
            f"Inspirational Quote from your Beastie: {self.user_username}",
        )
        self.assertEqual(first.body, self.message)
        self.assertEqual(
            first.from_email, self.user_email
        )  # task uses user's email if provided
        self.assertEqual(first.to, [self.user_beastie_email])

        # Second email goes to the user as a CC/copy
        second = mail.outbox[1]
        self.assertEqual(
            second.subject,
            f"You Sent an Inspirational Quote to your Beastie: {self.user_beastie_username}",  # noqa: E501
        )
        self.assertEqual(second.body, self.message)
        self.assertEqual(second.from_email, self.user_email)
        self.assertEqual(second.to, [self.user_email])

    @mock.patch(
        "boosts.tasks.EmailMultiAlternatives.send",
        side_effect=smtplib.SMTPException("boom"),
    )
    def test_autoretry_on_smtp_errors(self, _mock_send):
        """
        If the underlying SMTP send fails, the task is configured to autoretry.
        In eager/propagate mode that surfaces as a celery.exceptions.Retry.
        """
        with self.assertRaises(Retry):
            send_inspirational_to_beastie.delay(
                self.user_username,
                self.user_email,
                self.user_beastie_email,
                self.user_beastie_username,
                self.message,
            )
        # Nothing should have been left in the outbox because the first send failed.
        self.assertEqual(len(mail.outbox), 0)
