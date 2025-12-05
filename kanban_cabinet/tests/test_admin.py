# kanban_cabinet/tests/test_admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase

from kanban_cabinet.admin import LocationAdmin, StockItemAdmin, StockItemInline
from kanban_cabinet.models import Location, StockItem


class AdminRegistrationTests(TestCase):
    def test_location_admin_is_registered(self):
        self.assertIn(Location, admin.site._registry)
        self.assertIsInstance(admin.site._registry[Location], LocationAdmin)

    def test_stockitem_admin_is_registered(self):
        self.assertIn(StockItem, admin.site._registry)
        self.assertIsInstance(admin.site._registry[StockItem], StockItemAdmin)


class StockItemInlineAndAdminMethodTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="owner", password="testpass123")
        self.location = Location.objects.create(
            owner=self.user,
            name="Test Location",
        )
        self.item = StockItem.objects.create(
            owner=self.user,
            location=self.location,
            name="Test Item",
            quantity_on_hand=2,
            target_quantity=5,
        )

    def test_stockitem_inline_quantity_to_restock_display(self):
        inline = StockItemInline(Location, admin.site)
        value = inline.quantity_to_restock_display(self.item)
        self.assertEqual(value, 3)

    def test_stockitem_admin_quantity_to_restock_display(self):
        model_admin = StockItemAdmin(StockItem, admin.site)
        value = model_admin.quantity_to_restock_display(self.item)
        self.assertEqual(value, 3)

    def test_stockitem_admin_configuration(self):
        model_admin = StockItemAdmin(StockItem, admin.site)

        # Sanity-check key config (list_display, readonly_fields, etc.)
        self.assertIn("name", model_admin.list_display)
        self.assertIn("quantity_to_restock_display", model_admin.list_display)
        self.assertIn("quantity_to_restock_display", model_admin.readonly_fields)

    def test_location_admin_uses_inline(self):
        model_admin = LocationAdmin(Location, admin.site)
        inline_classes = model_admin.inlines
        self.assertIn(StockItemInline, inline_classes)
