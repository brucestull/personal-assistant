from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from kanban_cabinet.models import Location, StockItem


class LocationModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="item_owner", password="testpass123"
        )

    def test_str_uses_name(self):
        location = Location.objects.create(
            owner=self.user,
            name="Bathroom Cabinet - Top Shelf",
            description="For shampoo and soap",
        )
        self.assertEqual(str(location), "Bathroom Cabinet - Top Shelf")

    def test_unique_together_owner_name(self):
        # First location is fine
        Location.objects.create(
            owner=self.user,
            name="Garage Shelf",
        )

        # Second with same (owner, name) must fail, but we wrap in atomic()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Location.objects.create(
                    owner=self.user,
                    name="Garage Shelf",
                )

        # Same name but different owner is allowed
        other_user = get_user_model().objects.create_user(
            username="other_user", password="x"
        )
        loc_other = Location.objects.create(
            owner=other_user,
            name="Garage Shelf",
        )
        self.assertEqual(loc_other.name, "Garage Shelf")


class StockItemModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="item_owner", password="testpass123"
        )
        self.location = Location.objects.create(
            owner=self.user,
            name="Kitchen - Drawer 1",
        )

    def test_str_includes_location_when_present(self):
        item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Teaspoon",
            quantity_on_hand=5,
            target_quantity=10,
        )
        self.assertIn("Teaspoon", str(item))
        self.assertIn("Kitchen - Drawer 1", str(item))

    def test_str_without_location(self):
        item = StockItem.objects.create(
            owner=self.user,
            location=None,
            name="Spare License",
            quantity_on_hand=1,
            target_quantity=3,
        )
        self.assertEqual(str(item), "Spare License")

    def test_quantity_to_restock_when_target_greater_than_on_hand(self):
        item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Paper Towels",
            quantity_on_hand=2,
            target_quantity=8,
        )
        self.assertEqual(item.quantity_to_restock, 6)
        self.assertTrue(item.needs_restock)

    def test_quantity_to_restock_when_equal(self):
        item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Toothpaste",
            quantity_on_hand=5,
            target_quantity=5,
        )
        self.assertEqual(item.quantity_to_restock, 0)
        self.assertFalse(item.needs_restock)

    def test_quantity_to_restock_when_on_hand_exceeds_target(self):
        item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Spare Screws",
            quantity_on_hand=20,
            target_quantity=10,
        )
        self.assertEqual(item.quantity_to_restock, 0)
        self.assertFalse(item.needs_restock)

    def test_unique_together_owner_name_location(self):
        StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Bandages",
            quantity_on_hand=2,
            target_quantity=10,
        )

        # Second with same (owner, name, location) must fail; wrap in atomic()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                StockItem.objects.create(
                    owner=self.user,
                    location=self.location,
                    name="Bandages",
                    quantity_on_hand=3,
                    target_quantity=12,
                )

        # Same name in different location is allowed
        other_location = Location.objects.create(
            owner=self.user,
            name="Bathroom Cabinet",
        )
        other_item = StockItem.objects.create(
            owner=self.user,
            location=other_location,
            name="Bandages",
            quantity_on_hand=1,
            target_quantity=5,
        )
        self.assertEqual(other_item.name, "Bandages")

    def test_slug_auto_generated_on_create(self):
        item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Test Item",
            quantity_on_hand=5,
            target_quantity=10,
        )
        self.assertEqual(item.slug, "test-item")

    def test_slug_collision_handling(self):
        # Create first item
        item1 = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Duplicate Name",
            quantity_on_hand=1,
            target_quantity=5,
        )
        self.assertEqual(item1.slug, "duplicate-name")

        # Create second item with same name in different location
        other_location = Location.objects.create(
            owner=self.user,
            name="Other Location",
        )
        item2 = StockItem.objects.create(
            owner=self.user,
            location=other_location,
            name="Duplicate Name",
            quantity_on_hand=2,
            target_quantity=6,
        )
        self.assertEqual(item2.slug, "duplicate-name-2")

        # Create third item with same name
        item3 = StockItem.objects.create(
            owner=self.user,
            location=None,
            name="Duplicate Name",
            quantity_on_hand=3,
            target_quantity=7,
        )
        self.assertEqual(item3.slug, "duplicate-name-3")

    def test_slug_stability_on_update(self):
        # Create item
        item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Original Name",
            quantity_on_hand=5,
            target_quantity=10,
        )
        original_slug = item.slug
        self.assertEqual(original_slug, "original-name")

        # Update item but not name - slug should remain stable
        item.quantity_on_hand = 7
        item.save()
        item.refresh_from_db()
        self.assertEqual(item.slug, original_slug)

        # Update item name - slug should still remain stable (not regenerate)
        item.name = "Updated Name"
        item.save()
        item.refresh_from_db()
        self.assertEqual(item.slug, original_slug)

    def test_slug_unique_constraint(self):
        # Create first item
        item1 = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Item One",
            quantity_on_hand=1,
            target_quantity=5,
        )
        
        # Manually try to create item with duplicate slug (should fail)
        item2 = StockItem(
            owner=self.user,
            location=self.location,
            name="Item Two",
            quantity_on_hand=2,
            target_quantity=6,
        )
        item2.slug = item1.slug  # Force duplicate slug
        
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                item2.save()
