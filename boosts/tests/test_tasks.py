# tests/test_tasks.py
from __future__ import annotations

import smtplib
from unittest import mock

from celery.exceptions import Retry
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings

from boosts.models import Inspirational
from boosts.tasks import send_inspirational_to_beastie, send_random_inspirational_email


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


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="no-reply@example.com",
    THE_SITE_NAME="Test Site",
)
class SendRandomInspirationalEmailTest(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        self.inspirational = Inspirational.objects.create(
            body="Keep going!",
            author=self.user,
        )

    def test_uses_user_email_as_from_address(self):
        """
        send_random_inspirational_email should use the user's own email as the
        'from' address, not the DEFAULT_FROM_EMAIL.
        """
        result = send_random_inspirational_email.delay(self.user.id)

        self.assertEqual(result.result["ok"], True)
        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.from_email, self.user.email)
        self.assertEqual(sent_email.to, [self.user.email])
        self.assertIn("Daily Boost", sent_email.subject)
