# kanban_cabinet/tests/test_views.py

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from kanban_cabinet.models import Location, StockItem
from kanban_cabinet import views as kc_views  # noqa: F401 - ensures module is imported


class BaseViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="owner", password="testpass123")
        self.other_user = User.objects.create_user(
            username="other", password="othertest123"
        )

        self.client = Client()
        self.client.login(username="owner", password="testpass123")

        self.location = Location.objects.create(
            owner=self.user,
            name="Main Cabinet",
        )
        self.other_location = Location.objects.create(
            owner=self.other_user,
            name="Other Cabinet",
        )

        self.item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Shampoo",
            unit_name="bottle",
            quantity_on_hand=1,
            target_quantity=3,
        )
        self.other_item = StockItem.objects.create(
            owner=self.other_user,
            location=self.other_location,
            name="Other Shampoo",
            unit_name="bottle",
            quantity_on_hand=10,
            target_quantity=3,
        )


class AuthRequiredTests(BaseViewTests):
    def test_dashboard_requires_login(self):
        client = Client()
        url = reverse("kanban_cabinet:dashboard")
        response = client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    def test_stockitem_list_requires_login(self):
        client = Client()
        url = reverse("kanban_cabinet:stockitem_list")
        response = client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_location_list_requires_login(self):
        client = Client()
        url = reverse("kanban_cabinet:location_list")
        response = client.get(url)
        self.assertEqual(response.status_code, 302)


class StockItemListAndDetailViewTests(BaseViewTests):
    def test_stockitem_list_shows_only_owner_items(self):
        url = reverse("kanban_cabinet:stockitem_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        object_list = list(response.context["object_list"])
        self.assertIn(self.item, object_list)
        self.assertNotIn(self.other_item, object_list)

    def test_stockitem_detail_for_owner(self):
        url = reverse(
            "kanban_cabinet:stockitem_detail", kwargs={"slug": self.item.slug}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.item)

    def test_stockitem_detail_404_for_non_owner(self):
        url = reverse(
            "kanban_cabinet:stockitem_detail",
            kwargs={"slug": self.other_item.slug},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_stockitem_detail_by_slug(self):
        """Test that detail view resolves by slug and returns 200."""
        url = reverse(
            "kanban_cabinet:stockitem_detail", kwargs={"slug": self.item.slug}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)

    def test_stockitem_old_pk_url_redirects_to_slug_url(self):
        """Test that old pk-based URLs redirect to slug-based URLs."""
        old_url = reverse(
            "kanban_cabinet:stockitem_redirect", kwargs={"pk": self.item.pk}
        )
        response = self.client.get(old_url)
        self.assertEqual(response.status_code, 301)  # Permanent redirect
        expected_url = reverse(
            "kanban_cabinet:stockitem_detail", kwargs={"slug": self.item.slug}
        )
        self.assertRedirects(
            response, expected_url, status_code=301, fetch_redirect_response=False
        )


class StockItemCreateUpdateDeleteViewTests(BaseViewTests):
    def test_create_stockitem_sets_owner_via_mixin(self):
        url = reverse("kanban_cabinet:stockitem_create")
        data = {
            "name": "New Soap",
            "location": self.location.pk,
            "description": "Nice soap",
            "is_physical": True,
            "unit_name": "bar",
            "quantity_on_hand": 0,
            "target_quantity": 4,
            "is_active": True,
        }
        response = self.client.post(url, data)
        # Should redirect to detail page
        self.assertEqual(response.status_code, 302)

        item = StockItem.objects.get(name="New Soap")
        self.assertEqual(item.owner, self.user)
        self.assertEqual(item.location, self.location)
        self.assertEqual(item.target_quantity, 4)

    def test_update_stockitem_uses_owner_mixin_but_does_not_change_owner(self):
        url = reverse(
            "kanban_cabinet:stockitem_update", kwargs={"slug": self.item.slug}
        )
        data = {
            "name": "Shampoo (Updated)",
            "location": self.location.pk,
            "description": "Updated desc",
            "is_physical": True,
            "unit_name": "bottle",
            "quantity_on_hand": 2,
            "target_quantity": 5,
            "is_active": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Shampoo (Updated)")
        self.assertEqual(self.item.quantity_on_hand, 2)
        # Owner should still be the same
        self.assertEqual(self.item.owner, self.user)

    def test_delete_stockitem(self):
        url = reverse(
            "kanban_cabinet:stockitem_delete", kwargs={"slug": self.item.slug}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(StockItem.objects.filter(pk=self.item.pk).exists())

    def test_delete_stockitem_of_other_user_404(self):
        url = reverse(
            "kanban_cabinet:stockitem_delete",
            kwargs={"slug": self.other_item.slug},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class LocationListDetailCrudTests(BaseViewTests):
    def test_location_list_shows_only_owner_locations(self):
        url = reverse("kanban_cabinet:location_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        object_list = list(response.context["object_list"])
        self.assertIn(self.location, object_list)
        self.assertNotIn(self.other_location, object_list)

    def test_location_detail_for_owner(self):
        url = reverse("kanban_cabinet:location_detail", args=[self.location.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.location)

    def test_location_detail_404_for_non_owner(self):
        url = reverse("kanban_cabinet:location_detail", args=[self.other_location.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_location_sets_owner(self):
        url = reverse("kanban_cabinet:location_create")
        data = {
            "name": "New Location",
            "description": "For random stuff",
            "is_active": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        location = Location.objects.get(name="New Location")
        self.assertEqual(location.owner, self.user)

    def test_update_location(self):
        url = reverse("kanban_cabinet:location_update", args=[self.location.pk])
        data = {
            "name": "Main Cabinet (Updated)",
            "description": "Updated",
            "is_active": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Main Cabinet (Updated)")
        self.assertFalse(self.location.is_active)

    def test_delete_location(self):
        # Use a location that has NO items, so PROTECT does not trigger
        empty_location = Location.objects.create(
            owner=self.user,
            name="Empty Cabinet",
        )
        url = reverse("kanban_cabinet:location_delete", args=[empty_location.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Location.objects.filter(pk=empty_location.pk).exists())


class DashboardViewTests(BaseViewTests):
    def test_dashboard_shows_correct_summary_and_item_ordering(self):
        # Create a couple more items to exercise annotate/aggregation
        # Item needing restock by 5
        item2 = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Toilet Paper",
            unit_name="roll",
            quantity_on_hand=3,
            target_quantity=8,
        )
        # Item fully stocked (no restock needed)
        item3 = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Soap",
            unit_name="bar",
            quantity_on_hand=10,
            target_quantity=5,
        )

        url = reverse("kanban_cabinet:dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        items = list(response.context["items"])
        items_needing_restock = list(response.context["items_needing_restock"])
        summary = response.context["summary"]

        # Only this user's items are considered (BaseViewTests set those up)
        # We have: self.item (needs restock by 2), item2 (needs restock by 5), item3 (none)  # noqa: E501
        self.assertEqual(summary["total_items"], 3)
        self.assertEqual(summary["total_needing_restock"], 2)
        self.assertEqual(summary["total_units_to_order"], 7)

        # items_needing_restock should contain only the two that need restock
        self.assertIn(self.item, items_needing_restock)
        self.assertIn(item2, items_needing_restock)
        self.assertNotIn(item3, items_needing_restock)

        # Items should be ordered by descending quantity_to_restock_annotated, then name
        # So item2 (5) should come before self.item (2)
        needing_sorted_by_view = [i.name for i in items if i.quantity_to_restock > 0]
        self.assertLess(
            needing_sorted_by_view.index("Toilet Paper"),
            needing_sorted_by_view.index("Shampoo"),
        )
