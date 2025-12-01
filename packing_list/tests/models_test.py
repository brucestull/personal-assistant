from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

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
            name="Another task",
            activity=self.activity,
            user=self.user,
        )
        self.assertFalse(task.is_completed)
