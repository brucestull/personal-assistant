from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from packing_list.models import Activity, Item

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
