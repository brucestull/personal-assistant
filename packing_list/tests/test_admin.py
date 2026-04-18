# packing_list/tests/test_admin.py

from __future__ import annotations

from unittest.mock import MagicMock

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase

from packing_list.admin import ActivityAdmin, ItemAdmin, TaskAdmin
from packing_list.models import Activity, Item, Task

User = get_user_model()


class AdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = User.objects.create_user(username="dan", password="pw")
        self.other_user = User.objects.create_user(username="other", password="pw")

        self.activity = Activity.objects.create(
            name="Run", user=self.user, description="Morning run"
        )
        self.activity2 = Activity.objects.create(name="Trip", user=self.user)

        self.item = Item.objects.create(
            name="Shoes",
            activity=self.activity,
            user=self.user,
            quantity=1,
            is_packed=False,
            is_essential=True,
        )
        self.item2 = Item.objects.create(
            name="Socks",
            activity=self.activity,
            user=self.user,
            quantity=2,
            is_packed=True,
            is_essential=False,
        )
        self.task = Task.objects.create(
            name="Book flight",
            activity=self.activity,
            user=self.user,
            is_completed=False,
        )
        self.task2 = Task.objects.create(
            name="Charge watch",
            activity=self.activity,
            user=self.user,
            is_completed=True,
        )

        self.act_admin = ActivityAdmin(Activity, self.site)
        self.it_admin = ItemAdmin(Item, self.site)
        self.task_admin = TaskAdmin(Task, self.site)

    def test_activity_admin_configuration(self):
        self.assertIn("item_count", self.act_admin.list_display)
        self.assertIn("packed_item_count", self.act_admin.list_display)
        self.assertIn("packed_percent", self.act_admin.list_display)
        self.assertIn("task_count", self.act_admin.list_display)
        self.assertIn("completed_task_count", self.act_admin.list_display)

        self.assertIn("name", self.act_admin.search_fields)
        self.assertIn("description", self.act_admin.search_fields)
        self.assertIn("user__username", self.act_admin.search_fields)

        self.assertEqual(self.act_admin.list_filter, ("user",))
        self.assertEqual(self.act_admin.ordering, ("name",))

        # inlines
        inline_models = [inline.model for inline in self.act_admin.inlines]
        self.assertIn(Item, inline_models)
        self.assertIn(Task, inline_models)

    def test_activity_admin_get_queryset_has_expected_annotations(self):
        qs = self.act_admin.get_queryset(MagicMock())
        self.assertIsInstance(qs, models.QuerySet)

        annotations = qs.query.annotations
        for key in (
            "_item_count",
            "_packed_item_count",
            "_task_count",
            "_completed_task_count",
        ):
            self.assertIn(key, annotations)

    def test_activity_admin_summary_methods(self):
        # fetch annotated instance
        obj = self.act_admin.get_queryset(MagicMock()).get(pk=self.activity.pk)

        self.assertEqual(self.act_admin.item_count(obj), 2)
        self.assertEqual(self.act_admin.packed_item_count(obj), 1)
        self.assertEqual(self.act_admin.packed_percent(obj), "50%")

        self.assertEqual(self.act_admin.task_count(obj), 2)
        self.assertEqual(self.act_admin.completed_task_count(obj), 1)

    def test_activity_admin_packed_percent_when_no_items(self):
        obj = self.act_admin.get_queryset(MagicMock()).get(pk=self.activity2.pk)
        self.assertEqual(self.act_admin.item_count(obj), 0)
        self.assertEqual(self.act_admin.packed_item_count(obj), 0)
        self.assertEqual(self.act_admin.packed_percent(obj), "—")

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
        self.assertIn("name", self.it_admin.search_fields)
        self.assertIn("description", self.it_admin.search_fields)
        self.assertEqual(
            self.it_admin.list_filter, ("activity", "is_packed", "is_essential")
        )
        self.assertEqual(self.it_admin.ordering, ("activity", "name"))
        self.assertEqual(
            self.it_admin.list_editable, ("is_packed", "is_essential", "quantity")
        )
        self.assertEqual(
            self.it_admin.list_select_related, ("activity", "user", "activity__user")
        )

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
        self.assertIn("name", self.task_admin.search_fields)
        self.assertIn("description", self.task_admin.search_fields)
        self.assertEqual(self.task_admin.list_filter, ("activity", "is_completed"))
        self.assertEqual(self.task_admin.ordering, ("activity", "name"))
        self.assertEqual(self.task_admin.list_editable, ("is_completed",))
        self.assertEqual(
            self.task_admin.list_select_related, ("activity", "user", "activity__user")
        )

    def test_activity_user_method_item_and_task(self):
        self.assertEqual(self.it_admin.activity_user(self.item), "dan")
        self.assertEqual(self.task_admin.activity_user(self.task), "dan")

        class Fake:
            activity = None

        fake = Fake()
        self.assertEqual(self.it_admin.activity_user(fake), "N/A")
        self.assertEqual(self.task_admin.activity_user(fake), "N/A")

    def test_item_admin_save_model_sets_user_when_missing(self):
        obj = Item(
            name="Backpack",
            activity=self.activity,
            user=None,  # intentionally missing
            quantity=1,
        )
        request = MagicMock()
        form = MagicMock()

        self.it_admin.save_model(request, obj, form, change=False)
        self.assertEqual(obj.user, self.activity.user)

    def test_task_admin_save_model_sets_user_when_missing(self):
        obj = Task(
            name="Make list",
            activity=self.activity,
            user=None,
            is_completed=False,
        )
        request = MagicMock()
        form = MagicMock()

        self.task_admin.save_model(request, obj, form, change=False)
        self.assertEqual(obj.user, self.activity.user)

    def test_activity_admin_save_formset_sets_inline_users(self):
        """
        Ensures ActivityAdmin.save_formset sets Item/Task.user to Activity.user.
        """
        request = MagicMock()

        # "form.instance" is the Activity being edited
        form = MagicMock()
        form.instance = self.activity

        # inline instances with user unset (what we want to fix)
        new_item = Item(name="Hat", activity=self.activity, user=None, quantity=1)
        new_task = Task(
            name="Check weather", activity=self.activity, user=None, is_completed=False
        )

        formset = MagicMock()
        formset.save.return_value = [new_item, new_task]
        formset.save_m2m = MagicMock()

        self.act_admin.save_formset(request, form, formset, change=True)

        self.assertEqual(new_item.user, self.activity.user)
        self.assertEqual(new_task.user, self.activity.user)
        self.assertTrue(formset.save_m2m.called)
