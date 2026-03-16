from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from accounts.models import CustomUser
from thing_thought_reminder.models import ReminderSchedule, Thing, Thought


class ThingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="thinguser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.thing = Thing.objects.create(
            user=cls.user,
            name="Test Thing",
            content="This is some content.",
            type="test-type",
        )

    def test_str(self):
        self.assertEqual(str(self.thing), "Test Thing (test-type)")

    def test_name_field(self):
        field = self.thing._meta.get_field("name")
        self.assertEqual(field.max_length, 255)

    def test_content_field_is_textfield(self):
        from django.db.models import TextField

        field = self.thing._meta.get_field("content")
        self.assertIsInstance(field, TextField)

    def test_type_field(self):
        field = self.thing._meta.get_field("type")
        self.assertEqual(field.max_length, 100)

    def test_user_fk(self):
        self.assertEqual(self.thing.user, self.user)

    def test_get_absolute_url(self):
        url = self.thing.get_absolute_url()
        self.assertIn(str(self.thing.pk), url)

    def test_ordering(self):
        meta_ordering = Thing._meta.ordering
        self.assertEqual(meta_ordering, ("-created",))


class ThoughtModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="thoughtuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.thought = Thought.objects.create(
            user=cls.user,
            name="Test Thought",
            content="Some thought content.",
            realm="philosophy",
        )

    def test_str(self):
        self.assertEqual(str(self.thought), "Test Thought (philosophy)")

    def test_name_field(self):
        field = self.thought._meta.get_field("name")
        self.assertEqual(field.max_length, 255)

    def test_content_field_is_textfield(self):
        from django.db.models import TextField

        field = self.thought._meta.get_field("content")
        self.assertIsInstance(field, TextField)

    def test_realm_field(self):
        field = self.thought._meta.get_field("realm")
        self.assertEqual(field.max_length, 100)

    def test_user_fk(self):
        self.assertEqual(self.thought.user, self.user)

    def test_get_absolute_url(self):
        url = self.thought.get_absolute_url()
        self.assertIn(str(self.thought.pk), url)

    def test_ordering(self):
        meta_ordering = Thought._meta.ordering
        self.assertEqual(meta_ordering, ("-created",))


class ReminderScheduleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="scheduser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.thing = Thing.objects.create(
            user=cls.user,
            name="My Thing",
            content="Content.",
            type="idea",
        )
        cls.thought = Thought.objects.create(
            user=cls.user,
            name="My Thought",
            content="Content.",
            realm="work",
        )

    def _make_schedule(self, **kwargs):
        defaults = {
            "user": self.user,
            "thing": self.thing,
            "frequency": ReminderSchedule.FREQUENCY_DAILY,
        }
        defaults.update(kwargs)
        return ReminderSchedule(**defaults)

    def test_str_with_thing(self):
        schedule = self._make_schedule()
        schedule.save()
        self.assertIn("Daily", str(schedule))
        self.assertIn("My Thing", str(schedule))

    def test_str_with_thought(self):
        schedule = self._make_schedule(thing=None, thought=self.thought)
        schedule.save()
        self.assertIn("My Thought", str(schedule))

    def test_clean_requires_thing_or_thought(self):
        schedule = self._make_schedule(thing=None, thought=None)
        with self.assertRaises(ValidationError):
            schedule.full_clean()

    def test_clean_rejects_both_thing_and_thought(self):
        schedule = self._make_schedule(thing=self.thing, thought=self.thought)
        with self.assertRaises(ValidationError):
            schedule.full_clean()

    def test_frequency_choices(self):
        choices_keys = [k for k, _ in ReminderSchedule.FREQUENCY_CHOICES]
        self.assertIn("daily", choices_keys)
        self.assertIn("weekly", choices_keys)
        self.assertIn("monthly", choices_keys)

    def test_compute_next_send_daily(self):
        schedule = self._make_schedule(frequency=ReminderSchedule.FREQUENCY_DAILY)
        before = timezone.now()
        result = schedule.compute_next_send()
        self.assertGreater(result, before)
        # Should be roughly 1 day ahead
        from datetime import timedelta

        self.assertAlmostEqual(
            (result - before).total_seconds(), 86400, delta=10
        )

    def test_compute_next_send_weekly(self):
        schedule = self._make_schedule(frequency=ReminderSchedule.FREQUENCY_WEEKLY)
        before = timezone.now()
        result = schedule.compute_next_send()
        from datetime import timedelta

        self.assertAlmostEqual(
            (result - before).total_seconds(), 7 * 86400, delta=10
        )

    def test_compute_next_send_monthly(self):
        schedule = self._make_schedule(frequency=ReminderSchedule.FREQUENCY_MONTHLY)
        before = timezone.now()
        result = schedule.compute_next_send()
        from datetime import timedelta

        self.assertAlmostEqual(
            (result - before).total_seconds(), 30 * 86400, delta=10
        )

    def test_get_subject_for_thing(self):
        schedule = self._make_schedule()
        subject = schedule.get_subject()
        self.assertIn("My Thing", subject)

    def test_get_subject_for_thought(self):
        schedule = self._make_schedule(thing=None, thought=self.thought)
        subject = schedule.get_subject()
        self.assertIn("My Thought", subject)

    def test_get_content_for_thing(self):
        schedule = self._make_schedule()
        content = schedule.get_content()
        self.assertIn("My Thing", content)
        self.assertIn("idea", content)

    def test_get_content_for_thought(self):
        schedule = self._make_schedule(thing=None, thought=self.thought)
        content = schedule.get_content()
        self.assertIn("My Thought", content)
        self.assertIn("work", content)

    def test_get_absolute_url(self):
        schedule = self._make_schedule()
        schedule.save()
        url = schedule.get_absolute_url()
        self.assertIn(str(schedule.pk), url)
