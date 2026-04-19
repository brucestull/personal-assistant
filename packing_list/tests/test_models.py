# packing_list/tests/test_models.py

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from packing_list.models import Activity, Item, Task

User = get_user_model()


class ActivityModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pw")
        self.activity = Activity.objects.create(
            name="Hike", description="Mountain trail", user=self.user
        )

    def test_str_returns_name(self):
        self.assertEqual(str(self.activity), "Hike")

    def test_get_absolute_url(self):
        expected = reverse(
            "packing_list:activity_detail", kwargs={"pk": self.activity.pk}
        )
        self.assertEqual(self.activity.get_absolute_url(), expected)

    def test_meta_verbose_names(self):
        self.assertEqual(Activity._meta.verbose_name, "Activity")
        self.assertEqual(Activity._meta.verbose_name_plural, "Activities")


class ItemModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="pw")
        self.activity = Activity.objects.create(name="Camp", user=self.user)
        self.item = Item.objects.create(
            name="Tent",
            description="2-person",
            quantity=2,
            is_packed=True,
            is_essential=False,
            activity=self.activity,
            user=self.user,
        )

    def test_str_returns_name(self):
        self.assertEqual(str(self.item), "Tent")

    def test_get_absolute_url(self):
        expected = reverse("packing_list:item_detail", kwargs={"pk": self.item.pk})
        self.assertEqual(self.item.get_absolute_url(), expected)

    def test_defaults(self):
        item = Item.objects.create(name="Water", activity=self.activity, user=self.user)
        self.assertEqual(item.quantity, 1)
        self.assertFalse(item.is_packed)
        self.assertFalse(item.is_essential)

    def test_meta_verbose_names_and_ordering(self):
        self.assertEqual(Item._meta.verbose_name, "Item")
        self.assertEqual(Item._meta.verbose_name_plural, "Items")
        # inherited ordering from ActivityEntry.Meta
        self.assertEqual(list(Item._meta.ordering), ["activity", "name"])


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="carol", password="pw")
        self.activity = Activity.objects.create(name="Trip", user=self.user)
        self.task = Task.objects.create(
            name="Book flight",
            description="Round trip to destination",
            is_completed=False,
            activity=self.activity,
            user=self.user,
        )

    def test_str_returns_name(self):
        self.assertEqual(str(self.task), "Book flight")

    def test_get_absolute_url(self):
        expected = reverse("packing_list:task_detail", kwargs={"pk": self.task.pk})
        self.assertEqual(self.task.get_absolute_url(), expected)

    def test_default_is_completed_false(self):
        task = Task.objects.create(
            name="Another task", activity=self.activity, user=self.user
        )
        self.assertFalse(task.is_completed)

    def test_meta_verbose_names_and_ordering(self):
        self.assertEqual(Task._meta.verbose_name, "Task")
        self.assertEqual(Task._meta.verbose_name_plural, "Tasks")
        self.assertEqual(list(Task._meta.ordering), ["activity", "name"])
