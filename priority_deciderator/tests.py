from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from .models import Reminder, ReminderSchedule

User = get_user_model()


class ReminderModelTest(TestCase):
    """Tests for Reminder model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        # Set registration_accepted if required
        if hasattr(self.user, "registration_accepted"):
            self.user.registration_accepted = True
            self.user.save()

    def test_create_reminder(self):
        """Test creating a reminder."""
        reminder = Reminder.objects.create(
            name="Test Reminder",
            description="Test description",
            user=self.user,
        )
        self.assertEqual(reminder.name, "Test Reminder")
        self.assertEqual(reminder.description, "Test description")
        self.assertEqual(reminder.user, self.user)
        self.assertTrue(reminder.is_active)

    def test_reminder_str(self):
        """Test reminder string representation."""
        reminder = Reminder.objects.create(
            name="Test Reminder",
            user=self.user,
        )
        expected_str = f"Test Reminder - {self.user.username}"
        self.assertEqual(str(reminder), expected_str)

    def test_reminder_get_absolute_url(self):
        """Test reminder get_absolute_url."""
        reminder = Reminder.objects.create(
            name="Test Reminder",
            user=self.user,
        )
        expected_url = reverse("priority_deciderator:reminder_detail", kwargs={"pk": reminder.pk})
        self.assertEqual(reminder.get_absolute_url(), expected_url)


class ReminderScheduleModelTest(TestCase):
    """Tests for ReminderSchedule model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        if hasattr(self.user, "registration_accepted"):
            self.user.registration_accepted = True
            self.user.save()

        self.reminder = Reminder.objects.create(
            name="Test Reminder",
            description="Test description",
            user=self.user,
        )

    def test_create_daily_schedule(self):
        """Test creating a daily schedule."""
        schedule = ReminderSchedule.objects.create(
            reminder=self.reminder,
            frequency="daily",
            time=timezone.now().time(),
        )
        self.assertEqual(schedule.reminder, self.reminder)
        self.assertEqual(schedule.frequency, "daily")
        self.assertTrue(schedule.is_active)

    def test_create_weekly_schedule(self):
        """Test creating a weekly schedule."""
        schedule = ReminderSchedule.objects.create(
            reminder=self.reminder,
            frequency="weekly",
            time=timezone.now().time(),
            day_of_week=1,  # Tuesday
        )
        self.assertEqual(schedule.frequency, "weekly")
        self.assertEqual(schedule.day_of_week, 1)

    def test_create_monthly_schedule(self):
        """Test creating a monthly schedule."""
        schedule = ReminderSchedule.objects.create(
            reminder=self.reminder,
            frequency="monthly",
            time=timezone.now().time(),
            day_of_month=15,
        )
        self.assertEqual(schedule.frequency, "monthly")
        self.assertEqual(schedule.day_of_month, 15)

    def test_schedule_creates_periodic_task(self):
        """Test that creating a schedule creates a periodic task."""
        schedule = ReminderSchedule.objects.create(
            reminder=self.reminder,
            frequency="daily",
            time=timezone.now().time(),
        )
        self.assertIsNotNone(schedule.periodic_task)
        self.assertIsInstance(schedule.periodic_task, PeriodicTask)
        self.assertTrue(schedule.periodic_task.enabled)

    def test_schedule_str(self):
        """Test schedule string representation."""
        schedule = ReminderSchedule.objects.create(
            reminder=self.reminder,
            frequency="daily",
            time=timezone.now().time(),
        )
        expected_str = f"{self.reminder.name} - Daily at {schedule.time}"
        self.assertEqual(str(schedule), expected_str)

    def test_delete_schedule_deletes_periodic_task(self):
        """Test that deleting a schedule deletes the periodic task."""
        schedule = ReminderSchedule.objects.create(
            reminder=self.reminder,
            frequency="daily",
            time=timezone.now().time(),
        )
        periodic_task_id = schedule.periodic_task.id
        schedule.delete()
        
        # Check that periodic task is also deleted
        with self.assertRaises(PeriodicTask.DoesNotExist):
            PeriodicTask.objects.get(id=periodic_task_id)


class ReminderViewTest(TestCase):
    """Tests for Reminder views."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        if hasattr(self.user, "registration_accepted"):
            self.user.registration_accepted = True
            self.user.save()

        self.client.login(username="testuser", password="testpass123")

    def test_dashboard_view(self):
        """Test dashboard view."""
        url = reverse("priority_deciderator:dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "priority_deciderator/dashboard.html")

    def test_reminder_list_view(self):
        """Test reminder list view."""
        url = reverse("priority_deciderator:reminder_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "priority_deciderator/reminder_list.html")

    def test_reminder_create_view(self):
        """Test reminder create view."""
        url = reverse("priority_deciderator:reminder_create")
        data = {
            "name": "New Reminder",
            "description": "Test description",
            "is_active": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check reminder was created
        reminder = Reminder.objects.get(name="New Reminder")
        self.assertEqual(reminder.user, self.user)
        self.assertEqual(reminder.description, "Test description")

    def test_reminder_detail_view(self):
        """Test reminder detail view."""
        reminder = Reminder.objects.create(
            name="Test Reminder",
            user=self.user,
        )
        url = reverse("priority_deciderator:reminder_detail", kwargs={"pk": reminder.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "priority_deciderator/reminder_detail.html")
        self.assertContains(response, "Test Reminder")

    def test_reminder_update_view(self):
        """Test reminder update view."""
        reminder = Reminder.objects.create(
            name="Test Reminder",
            user=self.user,
        )
        url = reverse("priority_deciderator:reminder_update", kwargs={"pk": reminder.pk})
        data = {
            "name": "Updated Reminder",
            "description": "Updated description",
            "is_active": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        # Check reminder was updated
        reminder.refresh_from_db()
        self.assertEqual(reminder.name, "Updated Reminder")
        self.assertEqual(reminder.description, "Updated description")

    def test_reminder_delete_view(self):
        """Test reminder delete view."""
        reminder = Reminder.objects.create(
            name="Test Reminder",
            user=self.user,
        )
        url = reverse("priority_deciderator:reminder_delete", kwargs={"pk": reminder.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        
        # Check reminder was deleted
        with self.assertRaises(Reminder.DoesNotExist):
            Reminder.objects.get(pk=reminder.pk)

    def test_user_can_only_see_own_reminders(self):
        """Test that users can only see their own reminders."""
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )
        if hasattr(other_user, "registration_accepted"):
            other_user.registration_accepted = True
            other_user.save()

        other_reminder = Reminder.objects.create(
            name="Other's Reminder",
            user=other_user,
        )
        
        # Try to access other user's reminder
        url = reverse("priority_deciderator:reminder_detail", kwargs={"pk": other_reminder.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ScheduleViewTest(TestCase):
    """Tests for Schedule views."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        if hasattr(self.user, "registration_accepted"):
            self.user.registration_accepted = True
            self.user.save()

        self.client.login(username="testuser", password="testpass123")

        self.reminder = Reminder.objects.create(
            name="Test Reminder",
            user=self.user,
        )

    def test_schedule_create_view(self):
        """Test schedule create view."""
        url = reverse("priority_deciderator:schedule_create", kwargs={"reminder_pk": self.reminder.pk})
        data = {
            "frequency": "daily",
            "time": "09:00:00",
            "is_active": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        # Check schedule was created
        schedule = ReminderSchedule.objects.get(reminder=self.reminder)
        self.assertEqual(schedule.frequency, "daily")

    def test_schedule_update_view(self):
        """Test schedule update view."""
        from datetime import time
        schedule = ReminderSchedule.objects.create(
            reminder=self.reminder,
            frequency="daily",
            time=time(9, 0),
        )
        url = reverse("priority_deciderator:schedule_update", kwargs={"pk": schedule.pk})
        data = {
            "frequency": "weekly",
            "time": "10:00:00",
            "day_of_week": 1,
            "is_active": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        # Check schedule was updated
        schedule.refresh_from_db()
        self.assertEqual(schedule.frequency, "weekly")
        self.assertEqual(schedule.day_of_week, 1)

    def test_schedule_delete_view(self):
        """Test schedule delete view."""
        from datetime import time
        schedule = ReminderSchedule.objects.create(
            reminder=self.reminder,
            frequency="daily",
            time=time(9, 0),
        )
        url = reverse("priority_deciderator:schedule_delete", kwargs={"pk": schedule.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        
        # Check schedule was deleted
        with self.assertRaises(ReminderSchedule.DoesNotExist):
            ReminderSchedule.objects.get(pk=schedule.pk)

