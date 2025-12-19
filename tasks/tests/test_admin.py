# tasks/tests/test_admin.py

from django.test import TestCase
from django.contrib import admin
from tasks.models import Tag, Priority, Task
from tasks.admin import TagAdmin, PriorityAdmin, TaskAdmin


class AdminRegistrationTests(TestCase):
    def test_tag_admin_registered(self):
        self.assertIn(Tag, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Tag], TagAdmin)

    def test_priority_admin_registered(self):
        self.assertIn(Priority, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Priority], PriorityAdmin)

    def test_task_admin_registered(self):
        self.assertIn(Task, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Task], TaskAdmin)


class AdminConfigTests(TestCase):
    def test_tag_admin_config(self):
        ma = TagAdmin(Tag, admin.site)
        self.assertEqual(ma.list_display, ("name", "user", "created", "updated"))
        self.assertEqual(ma.list_filter, ("user",))
        self.assertEqual(ma.search_fields, ("name", "description"))
        self.assertEqual(ma.ordering, ("-created",))

    def test_priority_admin_config(self):
        ma = PriorityAdmin(Priority, admin.site)
        self.assertEqual(
            ma.list_display, ("name", "level", "user", "created", "updated")
        )
        self.assertEqual(ma.list_filter, ("level", "user"))
        self.assertEqual(ma.search_fields, ("name",))
        self.assertEqual(ma.ordering, ("level",))

    def test_task_admin_config(self):
        ma = TaskAdmin(Task, admin.site)
        self.assertEqual(ma.list_display, ("completed", "name", "user", "priority", "display_tags"))
        self.assertEqual(ma.list_filter, ("priority", "tag", "user"))
        self.assertEqual(ma.list_select_related, ("priority", "user"))
        self.assertEqual(ma.filter_horizontal, ("tag",))
        self.assertEqual(ma.search_fields, ("name", "information"))
        self.assertEqual(ma.ordering, ("completed", "priority__level", "-created"))
