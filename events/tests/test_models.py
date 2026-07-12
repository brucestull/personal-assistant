# events/tests/test_models.py

from django.test import TestCase
from django.utils import timezone

from accounts.models import CustomUser
from events.models import CalendarEvent, GoogleCalendarCredentials


class CalendarEventModelTest(TestCase):
    """Tests for the CalendarEvent model."""

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(username="testuser")
        cls.now = timezone.now()
        cls.event = CalendarEvent.objects.create(
            user=cls.user,
            summary="Team standup",
            start_datetime=cls.now,
            end_datetime=cls.now + timezone.timedelta(hours=1),
        )

    def test_str_includes_summary(self):
        self.assertIn("Team standup", str(self.event))

    def test_summary_help_text(self):
        help_text = self.event._meta.get_field("summary").help_text
        self.assertIn("Google Calendar", help_text)

    def test_google_event_id_defaults_blank(self):
        self.assertEqual(self.event.google_event_id, "")

    def test_description_defaults_blank(self):
        self.assertEqual(self.event.description, "")

    def test_ordering_by_start_datetime(self):
        ordering = CalendarEvent._meta.ordering
        self.assertEqual(ordering, ["start_datetime"])

    def test_verbose_name(self):
        self.assertEqual(CalendarEvent._meta.verbose_name, "Calendar Event")

    def test_verbose_name_plural(self):
        self.assertEqual(CalendarEvent._meta.verbose_name_plural, "Calendar Events")

    def test_user_foreign_key(self):
        user_model = self.event._meta.get_field("user").remote_field.model
        self.assertIs(user_model, CustomUser)


class GoogleCalendarCredentialsModelTest(TestCase):
    """Tests for the GoogleCalendarCredentials model."""

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(username="gcaluser")
        cls.creds = GoogleCalendarCredentials.objects.create(
            user=cls.user,
            token="acc_token",
            refresh_token="ref_token",
        )

    def test_str_includes_username(self):
        self.assertIn("gcaluser", str(self.creds))

    def test_one_to_one_relationship(self):
        retrieved = GoogleCalendarCredentials.objects.get(user=self.user)
        self.assertEqual(retrieved.token, "acc_token")

    def test_verbose_name(self):
        self.assertEqual(
            GoogleCalendarCredentials._meta.verbose_name,
            "Google Calendar Credentials",
        )
