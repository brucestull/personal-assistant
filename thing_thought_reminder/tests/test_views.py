from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from thing_thought_reminder.models import ReminderSchedule, Thing, Thought


class ThingViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="thingviewuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.other_user = CustomUser.objects.create_user(
            username="otheruser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.thing = Thing.objects.create(
            user=cls.user,
            name="Test Thing",
            content="Some content.",
            type="concept",
        )

    def setUp(self):
        self.client.login(username="thingviewuser", password="testpass123")

    def test_thing_list_view_status_200(self):
        response = self.client.get(reverse("thing_thought_reminder:thing-list"))
        self.assertEqual(response.status_code, 200)

    def test_thing_list_only_shows_own_things(self):
        Thing.objects.create(
            user=self.other_user,
            name="Other Thing",
            content="content",
            type="type",
        )
        response = self.client.get(reverse("thing_thought_reminder:thing-list"))
        self.assertContains(response, "Test Thing")
        self.assertNotContains(response, "Other Thing")

    def test_thing_detail_view_status_200(self):
        response = self.client.get(
            reverse("thing_thought_reminder:thing-detail", args=[self.thing.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_thing_detail_denied_for_other_user(self):
        other_thing = Thing.objects.create(
            user=self.other_user,
            name="Other Thing",
            content="content",
            type="type",
        )
        response = self.client.get(
            reverse("thing_thought_reminder:thing-detail", args=[other_thing.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_thing_create_view_get(self):
        response = self.client.get(reverse("thing_thought_reminder:thing-create"))
        self.assertEqual(response.status_code, 200)

    def test_thing_create_view_post(self):
        response = self.client.post(
            reverse("thing_thought_reminder:thing-create"),
            {"name": "New Thing", "content": "New content.", "type": "new-type"},
        )
        self.assertRedirects(response, reverse("thing_thought_reminder:thing-list"))
        self.assertTrue(Thing.objects.filter(name="New Thing", user=self.user).exists())

    def test_thing_update_view_get(self):
        response = self.client.get(
            reverse("thing_thought_reminder:thing-update", args=[self.thing.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_thing_update_view_post(self):
        response = self.client.post(
            reverse("thing_thought_reminder:thing-update", args=[self.thing.pk]),
            {"name": "Updated Thing", "content": "Updated content.", "type": "updated"},
        )
        self.assertRedirects(response, reverse("thing_thought_reminder:thing-list"))
        self.thing.refresh_from_db()
        self.assertEqual(self.thing.name, "Updated Thing")

    def test_thing_delete_view_get(self):
        response = self.client.get(
            reverse("thing_thought_reminder:thing-delete", args=[self.thing.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_thing_delete_view_post(self):
        thing_to_delete = Thing.objects.create(
            user=self.user,
            name="Delete Me",
            content="content",
            type="type",
        )
        response = self.client.post(
            reverse("thing_thought_reminder:thing-delete", args=[thing_to_delete.pk])
        )
        self.assertRedirects(response, reverse("thing_thought_reminder:thing-list"))
        self.assertFalse(Thing.objects.filter(pk=thing_to_delete.pk).exists())

    def test_thing_update_denied_for_other_user(self):
        other_thing = Thing.objects.create(
            user=self.other_user,
            name="Other Thing",
            content="content",
            type="type",
        )
        response = self.client.post(
            reverse("thing_thought_reminder:thing-update", args=[other_thing.pk]),
            {"name": "Hacked", "content": "content", "type": "type"},
        )
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_redirects_to_login(self):
        self.client.logout()
        response = self.client.get(reverse("thing_thought_reminder:thing-list"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('thing_thought_reminder:thing-list')}",
        )


class ThoughtViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="thoughtviewuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.thought = Thought.objects.create(
            user=cls.user,
            name="Test Thought",
            content="Some content.",
            realm="philosophy",
        )

    def setUp(self):
        self.client.login(username="thoughtviewuser", password="testpass123")

    def test_thought_list_view_status_200(self):
        response = self.client.get(reverse("thing_thought_reminder:thought-list"))
        self.assertEqual(response.status_code, 200)

    def test_thought_detail_view_status_200(self):
        response = self.client.get(
            reverse("thing_thought_reminder:thought-detail", args=[self.thought.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_thought_create_view_post(self):
        response = self.client.post(
            reverse("thing_thought_reminder:thought-create"),
            {
                "name": "New Thought",
                "content": "New content.",
                "realm": "creativity",
            },
        )
        self.assertRedirects(
            response, reverse("thing_thought_reminder:thought-list")
        )
        self.assertTrue(
            Thought.objects.filter(name="New Thought", user=self.user).exists()
        )

    def test_thought_update_view_post(self):
        response = self.client.post(
            reverse(
                "thing_thought_reminder:thought-update", args=[self.thought.pk]
            ),
            {
                "name": "Updated Thought",
                "content": "Updated.",
                "realm": "updated-realm",
            },
        )
        self.assertRedirects(
            response, reverse("thing_thought_reminder:thought-list")
        )
        self.thought.refresh_from_db()
        self.assertEqual(self.thought.name, "Updated Thought")

    def test_thought_delete_view_post(self):
        thought_to_delete = Thought.objects.create(
            user=self.user,
            name="Delete Me",
            content="content",
            realm="realm",
        )
        response = self.client.post(
            reverse(
                "thing_thought_reminder:thought-delete", args=[thought_to_delete.pk]
            )
        )
        self.assertRedirects(
            response, reverse("thing_thought_reminder:thought-list")
        )
        self.assertFalse(Thought.objects.filter(pk=thought_to_delete.pk).exists())


class ReminderScheduleViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="remindviewuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.thing = Thing.objects.create(
            user=cls.user,
            name="My Thing",
            content="content",
            type="idea",
        )
        cls.schedule = ReminderSchedule.objects.create(
            user=cls.user,
            thing=cls.thing,
            frequency=ReminderSchedule.FREQUENCY_DAILY,
        )

    def setUp(self):
        self.client.login(username="remindviewuser", password="testpass123")

    def test_reminder_list_view_status_200(self):
        response = self.client.get(reverse("thing_thought_reminder:reminder-list"))
        self.assertEqual(response.status_code, 200)

    def test_reminder_detail_view_status_200(self):
        response = self.client.get(
            reverse(
                "thing_thought_reminder:reminder-detail", args=[self.schedule.pk]
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_reminder_create_view_post(self):
        response = self.client.post(
            reverse("thing_thought_reminder:reminder-create"),
            {
                "thing": self.thing.pk,
                "thought": "",
                "frequency": ReminderSchedule.FREQUENCY_WEEKLY,
                "is_active": True,
            },
        )
        self.assertRedirects(
            response, reverse("thing_thought_reminder:reminder-list")
        )
        self.assertTrue(
            ReminderSchedule.objects.filter(
                user=self.user,
                thing=self.thing,
                frequency=ReminderSchedule.FREQUENCY_WEEKLY,
            ).exists()
        )

    def test_reminder_create_requires_thing_or_thought(self):
        response = self.client.post(
            reverse("thing_thought_reminder:reminder-create"),
            {
                "thing": "",
                "thought": "",
                "frequency": ReminderSchedule.FREQUENCY_DAILY,
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, 200)
        # The form should be invalid and show an error about missing thing/thought
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        non_field_errors = form.non_field_errors()
        self.assertTrue(
            any("Thing" in e or "Thought" in e for e in non_field_errors),
            f"Expected an error about Thing/Thought, got: {non_field_errors}",
        )

    def test_reminder_delete_view_post(self):
        schedule_to_delete = ReminderSchedule.objects.create(
            user=self.user,
            thing=self.thing,
            frequency=ReminderSchedule.FREQUENCY_MONTHLY,
        )
        response = self.client.post(
            reverse(
                "thing_thought_reminder:reminder-delete",
                args=[schedule_to_delete.pk],
            )
        )
        self.assertRedirects(
            response, reverse("thing_thought_reminder:reminder-list")
        )
        self.assertFalse(
            ReminderSchedule.objects.filter(pk=schedule_to_delete.pk).exists()
        )

    def test_dashboard_view_status_200(self):
        response = self.client.get(reverse("thing_thought_reminder:dashboard"))
        self.assertEqual(response.status_code, 200)
