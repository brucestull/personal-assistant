# tests/test_tasks.py
from __future__ import annotations

import smtplib
from unittest import mock

from celery.exceptions import Retry
from django.core import mail
from django.db.models import Max
from django.test import TestCase, override_settings

from accounts.models import CustomUser
from boosts.models import Inspirational
from boosts.tasks import send_daily_boost_and_note, send_inspirational_to_beastie
from unimportant_notes.models import UnimportantNote


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
)
class SendDailyBoostAndNoteTest(TestCase):
    def setUp(self) -> None:
        # Create test user
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        # Create test inspirational
        self.inspirational = Inspirational.objects.create(
            body="Test inspirational message",
            author=self.user,
        )
        # Create test unimportant note
        self.unimportant_note = UnimportantNote.objects.create(
            title="Test Note Title",
            content="Test note content",
            url="https://example.com",
            author=self.user,
        )

    def test_sends_email_with_both_items(self):
        """
        Test that the task sends an email with both inspirational and note.
        """
        # Act
        send_daily_boost_and_note.delay(self.user.id)

        # Assert
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Your Daily Boost and Note")
        self.assertIn("Your Daily Inspirational Quote", email.body)
        self.assertIn("Test inspirational message", email.body)
        self.assertIn("Your Daily Unimportant Note", email.body)
        self.assertIn("Test Note Title", email.body)
        self.assertIn("Test note content", email.body)
        self.assertIn("https://example.com", email.body)
        self.assertEqual(email.to, [self.user.email])

    def test_handles_missing_user(self):
        """
        Test that the task handles a non-existent user gracefully.
        """
        # Get a user ID that doesn't exist
        max_id = CustomUser.objects.aggregate(Max("id"))["id__max"] or 0
        non_existent_id = max_id + 1

        # Act
        send_daily_boost_and_note.delay(non_existent_id)

        # Assert - no email should be sent
        self.assertEqual(len(mail.outbox), 0)

    def test_handles_user_without_email(self):
        """
        Test that the task skips users without email addresses.
        """
        # Create user without email
        user_no_email = CustomUser.objects.create_user(
            username="noemail",
            password="testpass123",
        )

        # Act
        send_daily_boost_and_note.delay(user_no_email.id)

        # Assert - no email should be sent
        self.assertEqual(len(mail.outbox), 0)

    def test_handles_missing_inspirational(self):
        """
        Test that the task sends note even if no inspirational exists.
        """
        # Delete all inspirationals
        Inspirational.objects.all().delete()

        # Act
        send_daily_boost_and_note.delay(self.user.id)

        # Assert
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertNotIn("Your Daily Inspirational Quote", email.body)
        self.assertIn("Your Daily Unimportant Note", email.body)
        self.assertIn("Test Note Title", email.body)

    def test_handles_missing_unimportant_note(self):
        """
        Test that the task sends inspirational even if no note exists.
        """
        # Delete all unimportant notes
        UnimportantNote.objects.all().delete()

        # Act
        send_daily_boost_and_note.delay(self.user.id)

        # Assert
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("Your Daily Inspirational Quote", email.body)
        self.assertIn("Test inspirational message", email.body)
        self.assertNotIn("Your Daily Unimportant Note", email.body)

    def test_handles_no_content(self):
        """
        Test that the task handles when neither inspirational nor note exist.
        """
        # Delete all
        Inspirational.objects.all().delete()
        UnimportantNote.objects.all().delete()

        # Act
        send_daily_boost_and_note.delay(self.user.id)

        # Assert - no email should be sent
        self.assertEqual(len(mail.outbox), 0)

    @mock.patch(
        "boosts.tasks.EmailMultiAlternatives.send",
        side_effect=smtplib.SMTPException("boom"),
    )
    def test_autoretry_on_smtp_errors(self, _mock_send):
        """
        If the underlying SMTP send fails, the task is configured to autoretry.
        """
        with self.assertRaises(Retry):
            send_daily_boost_and_note.delay(self.user.id)
        # Nothing should have been left in the outbox because send failed.
        self.assertEqual(len(mail.outbox), 0)

    @mock.patch("boosts.tasks.DEFAULT_FROM_EMAIL", None)
    def test_handles_missing_default_from_email(self):
        """
        Test that the task handles missing DEFAULT_FROM_EMAIL configuration.
        """
        # Act
        send_daily_boost_and_note.delay(self.user.id)

        # Assert - no email should be sent
        self.assertEqual(len(mail.outbox), 0)
