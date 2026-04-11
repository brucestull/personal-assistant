from django.test import TestCase

from accounts.models import CustomUser
from item_location.models import Item, StorageLocation


class StorageLocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="locuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.location = StorageLocation.objects.create(
            user=cls.user,
            name="Garage Shelf",
            type="shelf",
        )

    def test_str(self):
        self.assertEqual(str(self.location), "Garage Shelf (Shelf)")

    def test_name_field_max_length(self):
        field = self.location._meta.get_field("name")
        self.assertEqual(field.max_length, 255)

    def test_type_field_choices(self):
        field = self.location._meta.get_field("type")
        choice_values = [c[0] for c in field.choices]
        self.assertIn("shelf", choice_values)

    def test_user_fk(self):
        self.assertEqual(self.location.user, self.user)

    def test_get_absolute_url(self):
        url = self.location.get_absolute_url()
        self.assertIn(str(self.location.pk), url)

    def test_ordering(self):
        self.assertEqual(StorageLocation._meta.ordering, ("name",))


class ItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="itemuser",
            password="testpass123",
            registration_accepted=True,
        )
        cls.location = StorageLocation.objects.create(
            user=cls.user,
            name="Kitchen Cabinet",
            type="cabinet",
        )
        cls.item = Item.objects.create(
            user=cls.user,
            name="Cordless Drill",
            type="tool",
            location=cls.location,
        )
        cls.item_no_location = Item.objects.create(
            user=cls.user,
            name="Loose Screw",
            type="tool",
        )

    def test_str_with_location(self):
        self.assertEqual(
            str(self.item), "Cordless Drill (Tool) @ Kitchen Cabinet"
        )

    def test_str_without_location(self):
        self.assertEqual(str(self.item_no_location), "Loose Screw (Tool)")

    def test_name_field_max_length(self):
        field = self.item._meta.get_field("name")
        self.assertEqual(field.max_length, 255)

    def test_type_field_choices(self):
        field = self.item._meta.get_field("type")
        choice_values = [c[0] for c in field.choices]
        self.assertIn("tool", choice_values)

    def test_location_fk_nullable(self):
        field = self.item._meta.get_field("location")
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_user_fk(self):
        self.assertEqual(self.item.user, self.user)

    def test_get_absolute_url(self):
        url = self.item.get_absolute_url()
        self.assertIn(str(self.item.pk), url)

    def test_ordering(self):
        self.assertEqual(Item._meta.ordering, ("name",))

    def test_location_set_null_on_delete(self):
        temp_location = StorageLocation.objects.create(
            user=self.user, name="Temp", type="box"
        )
        item = Item.objects.create(
            user=self.user, name="TempItem", type="other", location=temp_location
        )
        temp_location.delete()
        item.refresh_from_db()
        self.assertIsNone(item.location)
