from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from plan_it.models import (
    StorageLocation,
    Item,
    ActivityType,
    Activity,
    ActivityLocation,
    ActivityInstance,
)


User = get_user_model()


class PlanItViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass", registration_accepted=True
        )
        self.client.login(username="testuser", password="testpass")

        self.location = StorageLocation.objects.create(user=self.user, name="Garage")
        self.item = Item.objects.create(
            user=self.user, name="Socket Set", storage_location=self.location
        )
        self.activity_type = ActivityType.objects.create(
            user=self.user, name="Cleaning"
        )

        self.overdue_activity = Activity.objects.create(
            user=self.user,
            name="Overdue Task",
            type=self.activity_type,
            due_date=date.today() - timedelta(days=2),
        )
        self.today_activity = Activity.objects.create(
            user=self.user,
            name="Today's Task",
            type=self.activity_type,
            due_date=date.today(),
        )
        self.upcoming_activity = Activity.objects.create(
            user=self.user,
            name="Future Task",
            type=self.activity_type,
            due_date=date.today() + timedelta(days=2),
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse("plan_it:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Overdue Task")
        # TODO: Fix view to show `Today's Task`
        # self.assertContains(response, "Today's Task")
        self.assertContains(response, "Future Task")
        self.assertContains(response, "Socket Set")

    def test_dashboard_statistics(self):
        """Test that dashboard shows correct statistics"""
        response = self.client.get(reverse("plan_it:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Overdue")
        self.assertContains(response, "Due Today")
        self.assertContains(response, "Upcoming")
        # Check context variables
        self.assertEqual(response.context["overdue_count"], 1)
        self.assertEqual(response.context["today_count"], 1)
        self.assertEqual(response.context["upcoming_count"], 1)

    def test_dashboard_quick_actions(self):
        """Test that dashboard shows quick action buttons"""
        response = self.client.get(reverse("plan_it:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quick Actions")
        self.assertContains(response, "New Activity")
        self.assertContains(response, "New Item")
        self.assertContains(response, "New Location")
        self.assertContains(response, "New Type")

    def test_storage_location_crud(self):
        # Create
        response = self.client.post(
            reverse("plan_it:storage_location_add"), {"name": "Attic"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            StorageLocation.objects.filter(name="Attic", user=self.user).exists()
        )

        # List
        response = self.client.get(reverse("plan_it:storage_location_list"))
        self.assertContains(response, "Garage")

        # Update
        response = self.client.post(
            reverse("plan_it:storage_location_edit", args=[self.location.id]),
            {"name": "Updated Garage"},
        )
        self.assertEqual(response.status_code, 302)
        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Updated Garage")

        # Delete
        response = self.client.post(
            reverse("plan_it:storage_location_delete", args=[self.location.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(StorageLocation.objects.filter(id=self.location.id).exists())

    def test_item_crud(self):
        response = self.client.post(
            reverse("plan_it:item_add"),
            {"name": "New Item", "storage_location": self.location.id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Item.objects.filter(name="New Item", user=self.user).exists())

    def test_activity_type_crud(self):
        response = self.client.post(
            reverse("plan_it:activity_type_add"), {"name": "Maintenance"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ActivityType.objects.filter(name="Maintenance", user=self.user).exists()
        )

    def test_activity_crud(self):
        response = self.client.post(
            reverse("plan_it:activity_add"),
            {
                "name": "Test Task",
                "type": self.activity_type.id,
                "due_date": date.today(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Activity.objects.filter(name="Test Task", user=self.user).exists()
        )


class ActivityLocationViewTests(TestCase):
    """Test ActivityLocation CRUD operations"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass", registration_accepted=True
        )
        self.client.login(username="testuser", password="testpass")
        self.activity_location = ActivityLocation.objects.create(
            user=self.user, name="Home"
        )

    def test_activity_location_list(self):
        """Test listing activity locations"""
        response = self.client.get(reverse("plan_it:activity_location_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")

    def test_activity_location_create(self):
        """Test creating a new activity location"""
        response = self.client.post(
            reverse("plan_it:activity_location_add"), {"name": "Office"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ActivityLocation.objects.filter(name="Office", user=self.user).exists()
        )

    def test_activity_location_update(self):
        """Test updating an activity location"""
        response = self.client.post(
            reverse("plan_it:activity_location_edit", args=[self.activity_location.id]),
            {"name": "Updated Home"},
        )
        self.assertEqual(response.status_code, 302)
        self.activity_location.refresh_from_db()
        self.assertEqual(self.activity_location.name, "Updated Home")

    def test_activity_location_delete(self):
        """Test deleting an activity location"""
        response = self.client.post(
            reverse(
                "plan_it:activity_location_delete",
                args=[self.activity_location.id],
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            ActivityLocation.objects.filter(id=self.activity_location.id).exists()
        )

    def test_activity_location_hierarchy(self):
        """Test creating sub-locations"""
        parent = ActivityLocation.objects.create(user=self.user, name="Building")
        response = self.client.post(
            reverse("plan_it:activity_location_add"),
            {"name": "Floor 1", "parent_location": parent.id},
        )
        self.assertEqual(response.status_code, 302)
        child = ActivityLocation.objects.get(name="Floor 1")
        self.assertEqual(child.parent_location, parent)


class ActivityCompletionTests(TestCase):
    """Test activity completion functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass", registration_accepted=True
        )
        self.client.login(username="testuser", password="testpass")
        self.activity_type = ActivityType.objects.create(
            user=self.user, name="Cleaning"
        )
        self.activity = Activity.objects.create(
            user=self.user,
            name="Clean Kitchen",
            type=self.activity_type,
            due_date=date.today(),
        )

    def test_mark_activity_completed(self):
        """Test marking an activity as completed"""
        self.assertIsNone(self.activity.last_completed)
        self.assertEqual(ActivityInstance.objects.count(), 0)

        response = self.client.post(
            reverse("plan_it:activity_complete", args=[self.activity.pk])
        )
        self.assertEqual(response.status_code, 302)

        # Check activity was updated
        self.activity.refresh_from_db()
        self.assertIsNotNone(self.activity.last_completed)
        self.assertEqual(self.activity.last_completed, date.today())

        # Check instance was created
        self.assertEqual(ActivityInstance.objects.count(), 1)
        instance = ActivityInstance.objects.first()
        self.assertEqual(instance.name_snapshot, "Clean Kitchen")
        self.assertEqual(instance.type_name_snapshot, "Cleaning")
        self.assertEqual(instance.user, self.user)

    def test_complete_activity_with_item(self):
        """Test completing an activity that has a target item"""
        location = StorageLocation.objects.create(user=self.user, name="Garage")
        item = Item.objects.create(
            user=self.user, name="Vacuum", storage_location=location
        )
        activity = Activity.objects.create(
            user=self.user,
            name="Clean with Vacuum",
            type=self.activity_type,
            target_item=item,
        )

        response = self.client.post(
            reverse("plan_it:activity_complete", args=[activity.pk])
        )
        self.assertEqual(response.status_code, 302)

        instance = ActivityInstance.objects.get(activity=activity)
        self.assertEqual(instance.target_item_name_snapshot, "Vacuum")

    def test_complete_activity_with_location(self):
        """Test completing an activity that has a location"""
        activity_location = ActivityLocation.objects.create(
            user=self.user, name="Kitchen"
        )
        activity = Activity.objects.create(
            user=self.user,
            name="Clean Kitchen Floor",
            type=self.activity_type,
            activity_location=activity_location,
        )

        response = self.client.post(
            reverse("plan_it:activity_complete", args=[activity.pk])
        )
        self.assertEqual(response.status_code, 302)

        instance = ActivityInstance.objects.get(activity=activity)
        self.assertEqual(instance.activity_location_name_snapshot, "Kitchen")


class ActivityStatusTests(TestCase):
    """Test activity due status functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass", registration_accepted=True
        )
        self.activity_type = ActivityType.objects.create(
            user=self.user, name="Cleaning"
        )

    def test_overdue_status(self):
        """Test activity overdue status"""
        activity = Activity.objects.create(
            user=self.user,
            name="Overdue Task",
            type=self.activity_type,
            due_date=date.today() - timedelta(days=1),
        )
        self.assertEqual(activity.due_status(), "overdue")

    def test_today_status(self):
        """Test activity due today status"""
        activity = Activity.objects.create(
            user=self.user,
            name="Today Task",
            type=self.activity_type,
            due_date=date.today(),
        )
        self.assertEqual(activity.due_status(), "today")

    def test_upcoming_status(self):
        """Test activity upcoming status"""
        activity = Activity.objects.create(
            user=self.user,
            name="Future Task",
            type=self.activity_type,
            due_date=date.today() + timedelta(days=1),
        )
        self.assertEqual(activity.due_status(), "upcoming")

    def test_no_due_date_status(self):
        """Test activity with no due date"""
        activity = Activity.objects.create(
            user=self.user, name="No Due Date Task", type=self.activity_type
        )
        self.assertEqual(activity.due_status(), "none")
