from django.test import TestCase, override_settings

from accounts.models import CustomUser
from thing_thought_reminder.models import ReminderSchedule, Thing
from thing_thought_reminder.tasks import process_due_reminders, send_reminder_email


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="no-reply@example.com",
)
class SendReminderEmailTaskTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="tasktestuser",
            password="testpass123",
            email="tasktestuser@example.com",
            registration_accepted=True,
        )
        cls.thing = Thing.objects.create(
            user=cls.user,
            name="Task Thing",
            content="Some important content.",
            type="reminder",
        )

    def _make_schedule(self, **kwargs):
        defaults = {
            "user": self.user,
            "thing": self.thing,
            "frequency": ReminderSchedule.FREQUENCY_DAILY,
        }
        defaults.update(kwargs)
        return ReminderSchedule.objects.create(**defaults)

    def test_send_reminder_email_returns_ok_for_valid_schedule(self):
        schedule = self._make_schedule()
        result = send_reminder_email(schedule.pk)
        self.assertTrue(result["ok"])
        self.assertEqual(result["schedule_id"], schedule.pk)

    def test_send_reminder_email_updates_last_sent(self):
        schedule = self._make_schedule()
        self.assertIsNone(schedule.last_sent)
        send_reminder_email(schedule.pk)
        schedule.refresh_from_db()
        self.assertIsNotNone(schedule.last_sent)

    def test_send_reminder_email_updates_next_send(self):
        schedule = self._make_schedule()
        self.assertIsNone(schedule.next_send)
        send_reminder_email(schedule.pk)
        schedule.refresh_from_db()
        self.assertIsNotNone(schedule.next_send)

    def test_send_reminder_email_missing_schedule(self):
        result = send_reminder_email(99999)
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "schedule_not_found")

    def test_send_reminder_email_sends_email(self):
        from django.core import mail

        schedule = self._make_schedule()
        send_reminder_email(schedule.pk)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Task Thing", mail.outbox[0].body)

    def test_send_reminder_email_no_email_on_user(self):
        user_no_email = CustomUser.objects.create_user(
            username="noemailuser",
            password="testpass123",
            email="",
            registration_accepted=True,
        )
        thing = Thing.objects.create(
            user=user_no_email,
            name="No Email Thing",
            content="content",
            type="type",
        )
        schedule = ReminderSchedule.objects.create(
            user=user_no_email,
            thing=thing,
            frequency=ReminderSchedule.FREQUENCY_DAILY,
        )
        result = send_reminder_email(schedule.pk)
        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "no_user_email")


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPAGATES=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="no-reply@example.com",
)
class ProcessDueRemindersTaskTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="duereminduser",
            password="testpass123",
            email="duereminduser@example.com",
            registration_accepted=True,
        )
        cls.thing = Thing.objects.create(
            user=cls.user,
            name="Due Thing",
            content="Due content.",
            type="due-type",
        )

    def test_process_due_reminders_dispatches_due_schedules(self):
        from datetime import timedelta
        from unittest.mock import patch

        from django.utils import timezone

        past = timezone.now() - timedelta(hours=1)
        schedule = ReminderSchedule.objects.create(
            user=self.user,
            thing=self.thing,
            frequency=ReminderSchedule.FREQUENCY_DAILY,
            is_active=True,
            next_send=past,
        )
        with patch(
            "thing_thought_reminder.tasks.send_reminder_email.delay"
        ) as mock_delay:
            result = process_due_reminders()
        self.assertGreaterEqual(result["dispatched"], 1)
        mock_delay.assert_called_once_with(schedule.pk)

    def test_process_due_reminders_skips_future_schedules(self):
        from django.utils import timezone
        from datetime import timedelta

        future = timezone.now() + timedelta(hours=1)
        ReminderSchedule.objects.create(
            user=self.user,
            thing=self.thing,
            frequency=ReminderSchedule.FREQUENCY_DAILY,
            is_active=True,
            next_send=future,
        )
        result = process_due_reminders()
        self.assertEqual(result["dispatched"], 0)

    def test_process_due_reminders_skips_inactive_schedules(self):
        from django.utils import timezone
        from datetime import timedelta

        past = timezone.now() - timedelta(hours=1)
        ReminderSchedule.objects.create(
            user=self.user,
            thing=self.thing,
            frequency=ReminderSchedule.FREQUENCY_DAILY,
            is_active=False,
            next_send=past,
        )
        result = process_due_reminders()
        self.assertEqual(result["dispatched"], 0)
