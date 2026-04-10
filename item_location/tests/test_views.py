from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from item_location.models import Item, StorageLocation


class StorageLocationViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="locviewuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.other_user = CustomUser.objects.create_user(
            username="otherlocuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.location = StorageLocation.objects.create(
            user=cls.user,
            name="Garage Shelf",
            type="shelf",
        )

    def setUp(self):
        self.client.login(username="locviewuser", password="testpass123")

    def test_dashboard_status_200(self):
        response = self.client.get(reverse("item_location:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_location_list_status_200(self):
        response = self.client.get(reverse("item_location:location-list"))
        self.assertEqual(response.status_code, 200)

    def test_location_list_only_own(self):
        StorageLocation.objects.create(
            user=self.other_user, name="Other Shelf", type="shelf"
        )
        response = self.client.get(reverse("item_location:location-list"))
        self.assertContains(response, "Garage Shelf")
        self.assertNotContains(response, "Other Shelf")

    def test_location_detail_status_200(self):
        response = self.client.get(
            reverse("item_location:location-detail", args=[self.location.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_location_detail_denied_for_other_user(self):
        other_loc = StorageLocation.objects.create(
            user=self.other_user, name="Other Shelf", type="shelf"
        )
        response = self.client.get(
            reverse("item_location:location-detail", args=[other_loc.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_location_create_get(self):
        response = self.client.get(reverse("item_location:location-create"))
        self.assertEqual(response.status_code, 200)

    def test_location_create_post(self):
        response = self.client.post(
            reverse("item_location:location-create"),
            {"name": "New Cabinet", "type": "cabinet"},
        )
        self.assertRedirects(response, reverse("item_location:location-list"))
        self.assertTrue(
            StorageLocation.objects.filter(name="New Cabinet", user=self.user).exists()
        )

    def test_location_update_get(self):
        response = self.client.get(
            reverse("item_location:location-update", args=[self.location.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_location_update_post(self):
        response = self.client.post(
            reverse("item_location:location-update", args=[self.location.pk]),
            {"name": "Updated Shelf", "type": "shelf"},
        )
        self.assertRedirects(response, reverse("item_location:location-list"))
        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Updated Shelf")

    def test_location_delete_get(self):
        response = self.client.get(
            reverse("item_location:location-delete", args=[self.location.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_location_delete_post(self):
        loc_to_delete = StorageLocation.objects.create(
            user=self.user, name="ToDelete", type="box"
        )
        response = self.client.post(
            reverse("item_location:location-delete", args=[loc_to_delete.pk])
        )
        self.assertRedirects(response, reverse("item_location:location-list"))
        self.assertFalse(
            StorageLocation.objects.filter(pk=loc_to_delete.pk).exists()
        )

    def test_location_update_forbidden_for_other_user(self):
        other_loc = StorageLocation.objects.create(
            user=self.other_user, name="Other Loc", type="shelf"
        )
        response = self.client.post(
            reverse("item_location:location-update", args=[other_loc.pk]),
            {"name": "Hacked", "type": "shelf"},
        )
        self.assertEqual(response.status_code, 403)

    def test_spa_view_status_200(self):
        response = self.client.get(reverse("item_location:spa"))
        self.assertEqual(response.status_code, 200)


class ItemViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="itemviewuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.other_user = CustomUser.objects.create_user(
            username="otheritemuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.location = StorageLocation.objects.create(
            user=cls.user, name="Shelf A", type="shelf"
        )
        cls.item = Item.objects.create(
            user=cls.user, name="Hammer", type="tool", location=cls.location
        )

    def setUp(self):
        self.client.login(username="itemviewuser", password="testpass123")

    def test_item_list_status_200(self):
        response = self.client.get(reverse("item_location:item-list"))
        self.assertEqual(response.status_code, 200)

    def test_item_list_only_own(self):
        other_loc = StorageLocation.objects.create(
            user=self.other_user, name="Other Shelf", type="shelf"
        )
        Item.objects.create(
            user=self.other_user, name="Other Item", type="tool", location=other_loc
        )
        response = self.client.get(reverse("item_location:item-list"))
        self.assertContains(response, "Hammer")
        self.assertNotContains(response, "Other Item")

    def test_item_detail_status_200(self):
        response = self.client.get(
            reverse("item_location:item-detail", args=[self.item.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_item_detail_denied_for_other_user(self):
        other_loc = StorageLocation.objects.create(
            user=self.other_user, name="Other Shelf", type="shelf"
        )
        other_item = Item.objects.create(
            user=self.other_user, name="Other Item", type="tool", location=other_loc
        )
        response = self.client.get(
            reverse("item_location:item-detail", args=[other_item.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_item_create_get(self):
        response = self.client.get(reverse("item_location:item-create"))
        self.assertEqual(response.status_code, 200)

    def test_item_create_post(self):
        response = self.client.post(
            reverse("item_location:item-create"),
            {"name": "Screwdriver", "type": "tool", "location": self.location.pk},
        )
        self.assertRedirects(response, reverse("item_location:item-list"))
        self.assertTrue(
            Item.objects.filter(name="Screwdriver", user=self.user).exists()
        )

    def test_item_update_get(self):
        response = self.client.get(
            reverse("item_location:item-update", args=[self.item.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_item_update_post(self):
        response = self.client.post(
            reverse("item_location:item-update", args=[self.item.pk]),
            {"name": "Big Hammer", "type": "tool", "location": self.location.pk},
        )
        self.assertRedirects(response, reverse("item_location:item-list"))
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Big Hammer")

    def test_item_delete_get(self):
        response = self.client.get(
            reverse("item_location:item-delete", args=[self.item.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_item_delete_post(self):
        item_to_delete = Item.objects.create(
            user=self.user, name="ToDelete", type="other"
        )
        response = self.client.post(
            reverse("item_location:item-delete", args=[item_to_delete.pk])
        )
        self.assertRedirects(response, reverse("item_location:item-list"))
        self.assertFalse(Item.objects.filter(pk=item_to_delete.pk).exists())

    def test_item_update_forbidden_for_other_user(self):
        other_loc = StorageLocation.objects.create(
            user=self.other_user, name="Other Shelf", type="shelf"
        )
        other_item = Item.objects.create(
            user=self.other_user, name="Other Item", type="tool", location=other_loc
        )
        response = self.client.post(
            reverse("item_location:item-update", args=[other_item.pk]),
            {"name": "Hacked", "type": "tool"},
        )
        self.assertEqual(response.status_code, 403)
