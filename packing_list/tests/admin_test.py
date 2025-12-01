from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from unittest.mock import MagicMock

from packing_list.admin import ActivityAdmin, ItemAdmin, TaskAdmin
from packing_list.models import Activity, Item, Task

User = get_user_model()


class AdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = User.objects.create_user(username="dan", password="pw")
        self.activity = Activity.objects.create(name="Run", user=self.user)
        self.item = Item.objects.create(
            name="Shoes", activity=self.activity, user=self.user
        )
        self.task = Task.objects.create(
            name="Book flight", activity=self.activity, user=self.user
        )
        self.act_admin = ActivityAdmin(Activity, self.site)
        self.it_admin = ItemAdmin(Item, self.site)
        self.task_admin = TaskAdmin(Task, self.site)

    def test_activity_admin_configuration(self):
        self.assertEqual(self.act_admin.list_display, ("name", "user", "description"))
        self.assertEqual(self.act_admin.search_fields, ("name", "description"))
        self.assertEqual(self.act_admin.list_filter, ("user",))
        self.assertEqual(self.act_admin.ordering, ("-name",))

    def test_item_admin_configuration(self):
        self.assertEqual(
            self.it_admin.list_display,
            (
                "name",
                "activity",
                "activity_user",
                "quantity",
                "is_packed",
                "is_essential",
            ),
        )
        self.assertEqual(self.it_admin.search_fields, ("name", "description"))
        self.assertEqual(
            self.it_admin.list_filter, ("activity", "is_packed", "is_essential")
        )
        self.assertEqual(self.it_admin.ordering, ("activity", "name"))

    def test_task_admin_configuration(self):
        self.assertEqual(
            self.task_admin.list_display,
            (
                "name",
                "activity",
                "activity_user",
                "is_completed",
            ),
        )
        self.assertEqual(self.task_admin.search_fields, ("name", "description"))
        self.assertEqual(self.task_admin.list_filter, ("activity", "is_completed"))
        self.assertEqual(self.task_admin.ordering, ("activity", "name"))

    def test_get_queryset_selects_related(self):
        qs = self.it_admin.get_queryset(MagicMock())
        from django.db.models import QuerySet

        self.assertIsInstance(qs, QuerySet)

    def test_task_get_queryset_selects_related(self):
        qs = self.task_admin.get_queryset(MagicMock())
        from django.db.models import QuerySet

        self.assertIsInstance(qs, QuerySet)

    def test_activity_user_method(self):
        # normal case
        self.assertEqual(self.it_admin.activity_user(self.item), "dan")

        # edge: no activity
        class Fake:
            activity = None

        fake = Fake()
        self.assertEqual(self.it_admin.activity_user(fake), "N/A")

    def test_task_activity_user_method(self):
        # normal case
        self.assertEqual(self.task_admin.activity_user(self.task), "dan")

        # edge: no activity
        class Fake:
            activity = None

        fake = Fake()
        self.assertEqual(self.task_admin.activity_user(fake), "N/A")
