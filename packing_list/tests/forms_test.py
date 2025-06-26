from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model

from packing_list.forms import ActivityForm, ItemForm
from packing_list.models import Activity

User = get_user_model()


class ActivityFormTests(TestCase):
    def test_valid_data(self):
        form = ActivityForm(data={"name": "Jog", "description": "Morning run"})
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        form = ActivityForm(data={"name": "", "description": "No name"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class ItemFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="charlie", password="pw")
        # Two activities for this user + one for another
        self.a1 = Activity.objects.create(name="A1", user=self.user)
        self.a2 = Activity.objects.create(name="A2", user=self.user)
        other = User.objects.create_user(username="other", password="pw")
        Activity.objects.create(name="OtherAct", user=other)

    def test_without_kwargs_shows_all_activities(self):
        form = ItemForm()
        qs = form.fields["activity"].queryset
        # Should include all three
        names = {a.name for a in qs}
        self.assertSetEqual(names, {"A1", "A2", "OtherAct"})

    def test_user_kwargs_limits_queryset(self):
        form = ItemForm(user=self.user)
        qs = form.fields["activity"].queryset
        names = {a.name for a in qs}
        self.assertSetEqual(names, {"A1", "A2"})

    def test_activity_kwargs_initial_and_hidden(self):
        form = ItemForm(activity=self.a1)
        field = form.fields["activity"]
        self.assertEqual(field.initial, self.a1)
        self.assertIsInstance(field.widget, forms.HiddenInput)

    def test_valid_data_with_user_and_activity(self):
        data = {
            "name": "Water Bottle",
            "description": "",
            "quantity": 1,
            "is_packed": False,
            "is_essential": True,
            "activity": self.a1.pk,
        }
        form = ItemForm(data=data, user=self.user, activity=self.a1)
        self.assertTrue(form.is_valid())
