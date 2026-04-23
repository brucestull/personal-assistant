from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from packing_list.models import Activity, Item, Task

User = get_user_model()


class RegistrationDecoratorTests(TestCase):
    def setUp(self):
        self.url = reverse("packing_list:activity_list")

    def test_unauthenticated_forbidden(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 403)
        self.assertTemplateUsed(res, "403.html")
        self.assertIn("You must be logged in", res.context["error"])

    def test_unaccepted_forbidden(self):
        u = User.objects.create_user(  # noqa F841
            username="ua", password="pw", registration_accepted=False
        )
        self.client.login(username="ua", password="pw")
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 403)
        self.assertIn("not been accepted", res.context["error"])

    def test_accepted_allowed(self):
        u = User.objects.create_user(  # noqa F841
            username="ub", password="pw", registration_accepted=True
        )
        self.client.login(username="ub", password="pw")
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "packing_list/activity_list.html")


class ActivityViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="act", password="pw", registration_accepted=True
        )
        self.client.login(username="act", password="pw")
        self.act = Activity.objects.create(name="A", description="d", user=self.user)

    def test_list_only_user_activities(self):
        other = User.objects.create_user(
            username="o", password="pw", registration_accepted=True
        )
        Activity.objects.create(name="X", user=other)
        res = self.client.get(reverse("packing_list:activity_list"))
        self.assertEqual(list(res.context["activities"]), [self.act])

    def test_detail_valid_and_404(self):
        res = self.client.get(
            reverse("packing_list:activity_detail", kwargs={"pk": self.act.pk})
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["activity"], self.act)

        res404 = self.client.get(
            reverse("packing_list:activity_detail", kwargs={"pk": 999})
        )
        self.assertEqual(res404.status_code, 404)

    def test_create_get_and_post(self):
        # GET
        r1 = self.client.get(reverse("packing_list:activity_create"))
        self.assertEqual(r1.status_code, 200)
        self.assertIn("form", r1.context)

        # POST invalid
        r2 = self.client.post(reverse("packing_list:activity_create"), {"name": ""})
        self.assertEqual(r2.status_code, 200)
        self.assertFormError(r2.context["form"], "name", "This field is required.")

        # POST valid
        r3 = self.client.post(
            reverse("packing_list:activity_create"),
            {"name": "New", "description": "Desc"},
        )
        new_activity = Activity.objects.get(name="New", user=self.user)
        self.assertRedirects(
            r3, reverse("packing_list:activity_detail", kwargs={"pk": new_activity.pk})
        )
        self.assertTrue(Activity.objects.filter(name="New", user=self.user).exists())

    def test_update_get_and_post(self):
        url = reverse("packing_list:activity_update", kwargs={"pk": self.act.pk})

        # GET
        r1 = self.client.get(url)
        self.assertEqual(r1.status_code, 200)

        # POST invalid
        r2 = self.client.post(url, {"name": ""})
        self.assertEqual(r2.status_code, 200)
        self.assertFormError(r2.context["form"], "name", "This field is required.")

        # POST valid
        r3 = self.client.post(url, {"name": "Upd", "description": "d"})
        self.assertRedirects(r3, reverse("packing_list:activity_list"))
        self.act.refresh_from_db()
        self.assertEqual(self.act.name, "Upd")

    def test_delete_get_and_post(self):
        url = reverse("packing_list:activity_delete", kwargs={"pk": self.act.pk})

        # GET
        r1 = self.client.get(url)
        self.assertEqual(r1.status_code, 200)
        self.assertContains(r1, f"Delete {self.act.name}")

        # POST
        r2 = self.client.post(url)
        self.assertRedirects(r2, reverse("packing_list:activity_list"))
        self.assertFalse(Activity.objects.filter(pk=self.act.pk).exists())

    def test_pdf_various_fonts(self):
        # add an item
        Item.objects.create(
            name="I", quantity=1, description="d", activity=self.act, user=self.user
        )
        base = reverse("packing_list:activity_pdf", kwargs={"pk": self.act.pk})

        # default
        r0 = self.client.get(base)
        self.assertEqual(r0.status_code, 200)
        self.assertEqual(r0["Content-Type"], "application/pdf")
        expected_filename = (
            f'{slugify(self.act.name)}_{timezone.localdate():%Y-%m-%d}.pdf'
        )
        self.assertIn(expected_filename, r0["Content-Disposition"])

        # too small
        r1 = self.client.get(base + "?font_size=5")
        self.assertEqual(r1.status_code, 200)

        # too large
        r2 = self.client.get(base + "?font_size=999")
        self.assertEqual(r2.status_code, 200)

        # invalid
        r3 = self.client.get(base + "?font_size=foo")
        self.assertEqual(r3.status_code, 200)


class ItemViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="it", password="pw", registration_accepted=True
        )
        self.client.login(username="it", password="pw")
        self.act = Activity.objects.create(name="Act", user=self.user)
        self.item = Item.objects.create(
            name="X",
            description="d",
            quantity=1,
            is_packed=False,
            is_essential=True,
            activity=self.act,
            user=self.user,
        )

    def test_list_and_detail(self):
        r1 = self.client.get(reverse("packing_list:item_list"))
        self.assertEqual(r1.status_code, 200)
        self.assertIn(self.item, r1.context["items"])

        r2 = self.client.get(
            reverse("packing_list:item_detail", kwargs={"pk": self.item.pk})
        )
        self.assertEqual(r2.status_code, 200)

        r404 = self.client.get(reverse("packing_list:item_detail", kwargs={"pk": 999}))
        self.assertEqual(r404.status_code, 404)

    def test_create_get_and_post(self):
        # The activity query parameter is optional by design; the form still renders.
        r0 = self.client.get(reverse("packing_list:item_create"))
        self.assertEqual(r0.status_code, 200)
        self.assertIsNone(r0.context["form"].fields["activity"].initial)

        url = reverse("packing_list:item_create") + f"?activity={self.act.pk}"
        r1 = self.client.get(url)
        self.assertEqual(r1.status_code, 200)
        self.assertIn("form", r1.context)

        # POST invalid
        r2 = self.client.post(url, {"name": ""})
        self.assertEqual(r2.status_code, 200)
        self.assertFormError(r2.context["form"], "name", "This field is required.")

        # POST valid
        data = {
            "name": "NewI",
            "description": "",
            "quantity": 2,
            "is_packed": True,
            "is_essential": False,
            "activity": self.act.pk,
        }
        r3 = self.client.post(url, data)
        self.assertRedirects(
            r3, reverse("packing_list:activity_detail", kwargs={"pk": self.act.pk})
        )
        self.assertTrue(Item.objects.filter(name="NewI").exists())

    def test_update_get_and_post(self):
        url = reverse("packing_list:item_update", kwargs={"pk": self.item.pk})

        r1 = self.client.get(url)
        self.assertEqual(r1.status_code, 200)

        r2 = self.client.post(
            url,
            {
                "name": "X2",
                "description": "",
                "quantity": 5,
                "is_packed": False,
                "is_essential": True,
                "activity": self.act.pk,
            },
        )
        self.assertRedirects(r2, reverse("packing_list:item_list"))
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "X2")

        r3 = self.client.post(url, {"name": ""})
        self.assertFormError(r3.context["form"], "name", "This field is required.")

    def test_delete_get_and_post(self):
        url = reverse("packing_list:item_delete", kwargs={"pk": self.item.pk})

        r1 = self.client.get(url)
        self.assertEqual(r1.status_code, 200)
        self.assertContains(r1, f"Delete {self.item.name}")

        r2 = self.client.post(url)
        self.assertRedirects(r2, reverse("packing_list:item_list"))
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())


class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="task_user", password="pw", registration_accepted=True
        )
        self.client.login(username="task_user", password="pw")
        self.act = Activity.objects.create(name="Act", user=self.user)
        self.task = Task.objects.create(
            name="TaskX",
            description="d",
            is_completed=False,
            activity=self.act,
            user=self.user,
        )

    def test_list_and_detail(self):
        r1 = self.client.get(reverse("packing_list:task_list"))
        self.assertEqual(r1.status_code, 200)
        self.assertIn(self.task, r1.context["tasks"])

        r2 = self.client.get(
            reverse("packing_list:task_detail", kwargs={"pk": self.task.pk})
        )
        self.assertEqual(r2.status_code, 200)

        r404 = self.client.get(reverse("packing_list:task_detail", kwargs={"pk": 999}))
        self.assertEqual(r404.status_code, 404)

    def test_create_with_activity(self):
        url = reverse("packing_list:task_create") + f"?activity={self.act.pk}"
        r1 = self.client.get(url)
        self.assertEqual(r1.status_code, 200)
        self.assertIn("form", r1.context)

        # POST valid
        data = {
            "name": "NewTask",
            "description": "Task desc",
            "is_completed": False,
            "activity": self.act.pk,
        }
        r2 = self.client.post(url, data)
        # Should redirect to activity detail
        self.assertRedirects(
            r2, reverse("packing_list:activity_detail", kwargs={"pk": self.act.pk})
        )
        self.assertTrue(Task.objects.filter(name="NewTask").exists())

    def test_update_get_and_post(self):
        url = reverse("packing_list:task_update", kwargs={"pk": self.task.pk})

        r1 = self.client.get(url)
        self.assertEqual(r1.status_code, 200)

        r2 = self.client.post(
            url,
            {
                "name": "TaskX2",
                "description": "updated",
                "is_completed": True,
                "activity": self.act.pk,
            },
        )
        self.assertRedirects(r2, reverse("packing_list:task_list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "TaskX2")
        self.assertTrue(self.task.is_completed)

    def test_delete_get_and_post(self):
        url = reverse("packing_list:task_delete", kwargs={"pk": self.task.pk})

        r1 = self.client.get(url)
        self.assertEqual(r1.status_code, 200)
        self.assertContains(r1, f"Delete {self.task.name}")

        r2 = self.client.post(url)
        self.assertRedirects(r2, reverse("packing_list:task_list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
