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

    def test_slug_is_created_on_save(self):
        """Test that slug is auto-generated from name when item is created."""
        item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Letter A",
            quantity_on_hand=5,
            target_quantity=10,
        )
        self.assertEqual(item.slug, "letter-a")

    def test_slug_handles_special_characters(self):
        """Test that slug properly handles special characters."""
        item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Item with Spaces & Special!",
            quantity_on_hand=1,
            target_quantity=2,
        )
        self.assertEqual(item.slug, "item-with-spaces-special")

    def test_slug_collision_handling(self):
        """Test that slug collisions are handled by appending -2, -3, etc."""
        # Create first item with a name
        item1 = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Letter A",
            quantity_on_hand=5,
            target_quantity=10,
        )
        self.assertEqual(item1.slug, "letter-a")

        # Create second item with same name but different location
        location2 = Location.objects.create(
            owner=self.user,
            name="Kitchen - Drawer 2",
        )
        item2 = StockItem.objects.create(
            owner=self.user,
            location=location2,
            name="Letter A",
            quantity_on_hand=3,
            target_quantity=5,
        )
        self.assertEqual(item2.slug, "letter-a-2")

        # Create third item with same name
        item3 = StockItem.objects.create(
            owner=self.user,
            location=None,
            name="Letter A",
            quantity_on_hand=1,
            target_quantity=2,
        )
        self.assertEqual(item3.slug, "letter-a-3")

    def test_slug_uniqueness(self):
        """Test that slugs must be unique."""
        item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Test Item",
            quantity_on_hand=1,
            target_quantity=2,
        )

        # Try to create another item with the same slug manually
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                item2 = StockItem(
                    owner=self.user,
                    location=self.location,
                    name="Different Name",
                    slug=item.slug,  # Use same slug
                    quantity_on_hand=1,
                    target_quantity=2,
                )
                item2.save()

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
