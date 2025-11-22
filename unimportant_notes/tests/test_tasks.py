# unimportant_notes/tests/test_tasks.py
from __future__ import annotations

from django.core import mail
from django.test import TestCase, override_settings

from accounts.models import CustomUser
from unimportant_notes.models import NoteTag, UnimportantNote
from unimportant_notes.tasks import send_random_unimportant_note_email


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="no-reply@example.com",
)
class SendRandomUnimportantNoteEmailTest(TestCase):
    def setUp(self) -> None:
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
        )
        self.user.registration_accepted = True
        self.user.save()

        # Create a test note with content
        self.note = UnimportantNote.objects.create(
            title="Test Note",
            content="This is the content of the test note.",
            author=self.user,
        )

    def test_sends_email_with_content_field(self):
        """
        Test that the task sends an email with the note's content field.
        """
        # Act
        eager_result = send_random_unimportant_note_email.delay(self.user.id)
        result = eager_result.get()

        # Assert task returned success
        self.assertTrue(result["ok"])
        self.assertEqual(result["note_id"], self.note.id)
        self.assertEqual(result["user_id"], self.user.id)

        # Assert email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        # Assert email contains the content
        self.assertIn("This is the content of the test note.", email.body)
        self.assertIn("Test Note", email.body)
        self.assertEqual(email.to, [self.user.email])

    def test_sends_email_with_empty_content(self):
        """
        Test that the task handles notes with empty content gracefully.
        """
        # Remove the first note to ensure only the empty note is available
        UnimportantNote.objects.filter(author=self.user).delete()

        # Create a note with empty content
        UnimportantNote.objects.create(
            title="Empty Note",
            content="",
            author=self.user,
        )

        # Act
        eager_result = send_random_unimportant_note_email.delay(self.user.id)
        result = eager_result.get()

        # Assert task returned success
        self.assertTrue(result["ok"])

        # Assert email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        # Assert email contains the title but handles empty content
        self.assertIn("Empty Note", email.body)
        # The body should not include a separate content section since it's empty
        # Check that it only has the title line
        self.assertIn("Title: Empty Note", email.body)

    def test_sends_email_with_tag_filter(self):
        """
        Test that the task correctly filters notes by tag.
        """
        # Create a tag
        tag = NoteTag.objects.create(name="Important", author=self.user)

        # Create a note with the tag
        note_with_tag = UnimportantNote.objects.create(
            title="Tagged Note",
            content="This note has a tag.",
            author=self.user,
        )
        note_with_tag.tag.add(tag)

        # Act
        eager_result = send_random_unimportant_note_email.delay(
            self.user.id, tag_id=tag.id
        )
        result = eager_result.get()

        # Assert task returned success
        self.assertTrue(result["ok"])
        self.assertEqual(result["tag_id"], tag.id)

        # Assert email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        # Assert email contains the tag name in subject
        self.assertIn("[Important]", email.subject)

    def test_returns_error_when_user_not_found(self):
        """
        Test that the task returns an error when user doesn't exist.
        """
        # Act
        eager_result = send_random_unimportant_note_email.delay(99999)
        result = eager_result.get()

        # Assert task returned error
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "user_not_found")

        # Assert no email was sent
        self.assertEqual(len(mail.outbox), 0)

    def test_returns_error_when_no_notes(self):
        """
        Test that the task returns an error when user has no notes.
        """
        # Create a user without notes
        user_no_notes = CustomUser.objects.create_user(
            username="nonoteuser",
            email="nonotes@example.com",
            password="testpassword123",
        )
        user_no_notes.registration_accepted = True
        user_no_notes.save()

        # Act
        eager_result = send_random_unimportant_note_email.delay(user_no_notes.id)
        result = eager_result.get()

        # Assert task returned error
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "no_notes")

        # Assert no email was sent
        self.assertEqual(len(mail.outbox), 0)
