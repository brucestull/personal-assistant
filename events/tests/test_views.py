# events/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser
from events.models import CalendarEvent


class TodayEventsViewTest(TestCase):
    """Tests for the today_events view."""

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(username="viewuser")
        cls.today = timezone.localdate()
        now = timezone.now()
        cls.event = CalendarEvent.objects.create(
            user=cls.user,
            summary="Morning sync",
            start_datetime=now,
            end_datetime=now + timezone.timedelta(hours=1),
        )

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(reverse("events:today"))
        self.assertNotEqual(response.status_code, 200)

    def test_logged_in_user_sees_today_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("events:today"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Today")

    def test_today_event_shown(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("events:today"))
        self.assertContains(response, "Morning sync")

    def test_add_event_via_post(self):
        self.client.force_login(self.user)
        start = timezone.now().replace(second=0, microsecond=0)
        end = start + timezone.timedelta(hours=1)
        response = self.client.post(
            reverse("events:today"),
            {
                "summary": "New test event",
                "start_datetime": start.strftime("%Y-%m-%dT%H:%M"),
                "end_datetime": end.strftime("%Y-%m-%dT%H:%M"),
            },
        )
        self.assertRedirects(response, reverse("events:today"))
        self.assertTrue(
            CalendarEvent.objects.filter(
                user=self.user,
                summary="New test event",
            ).exists()
        )

    def test_form_visible_on_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("events:today"))
        self.assertContains(response, "id_summary")

    def test_sync_requires_post(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("events:sync"))
        self.assertEqual(response.status_code, 405)
