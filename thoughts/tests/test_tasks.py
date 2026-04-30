# thoughts/tests/test_tasks.py

from __future__ import annotations

import smtplib
from unittest import mock

from celery.exceptions import Retry
from django.core import mail
from django.test import TestCase, override_settings

from thoughts.tasks import send_thoughts_dashboard_email
from thoughts.tests.factories import CustomUserFactory


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="no-reply@example.com",
    SITE_URL="https://example.com",
)
class SendThoughtsDashboardEmailTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory()

    def test_sends_email_with_dashboard_url(self):
        """Email is sent and contains a link to the Thoughts dashboard."""
        send_thoughts_dashboard_email.delay(self.user.pk)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn(self.user.username, email.body)
        self.assertIn("/thoughts/", email.body)
        self.assertEqual(email.to, [self.user.email])

    def test_subject_contains_site_name(self):
        """Email subject includes the site name."""
        send_thoughts_dashboard_email.delay(self.user.pk)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Review Your Thoughts", mail.outbox[0].subject)

    def test_returns_ok_true_on_success(self):
        """Task returns ok=True dict when email is sent successfully."""
        result = send_thoughts_dashboard_email.delay(self.user.pk)

        self.assertTrue(result.get()["ok"])
        self.assertEqual(result.get()["user_id"], self.user.pk)

    def test_user_not_found_returns_ok_false(self):
        """Task returns ok=False when the user PK does not exist."""
        result = send_thoughts_dashboard_email.delay(user_id=99999)

        self.assertEqual(result.get(), {"ok": False, "reason": "user_not_found"})
        self.assertEqual(len(mail.outbox), 0)

    def test_user_without_email_returns_ok_false(self):
        """Task returns ok=False when the user has no email address."""
        self.user.email = ""
        self.user.save(update_fields=["email"])

        result = send_thoughts_dashboard_email.delay(self.user.pk)

        self.assertEqual(result.get(), {"ok": False, "reason": "no_user_email"})
        self.assertEqual(len(mail.outbox), 0)

    @mock.patch(
        "thoughts.tasks.EmailMultiAlternatives.send",
        side_effect=smtplib.SMTPException("smtp failure"),
    )
    def test_autoretry_on_smtp_error(self, _mock_send):
        """Task is configured to retry on SMTP errors."""
        with self.assertRaises(Retry):
            send_thoughts_dashboard_email.delay(self.user.pk)

        self.assertEqual(len(mail.outbox), 0)
