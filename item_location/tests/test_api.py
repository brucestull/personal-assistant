from django.test import TestCase

from accounts.models import CustomUser
from item_location.models import StorageLocation


class ItemLocationAPITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.accepted_user = CustomUser.objects.create_user(
            username="itemapiaccepted",
            password="testpass123",
            registration_accepted=True,
        )
        cls.unaccepted_user = CustomUser.objects.create_user(
            username="itemapiunaccepted",
            password="testpass123",
            registration_accepted=False,
        )
        StorageLocation.objects.create(
            user=cls.accepted_user,
            name="Garage Shelf",
            type="shelf",
        )

    def test_accepted_user_can_access_api(self):
        self.client.login(username="itemapiaccepted", password="testpass123")
        response = self.client.get("/item-location/api/locations/")
        self.assertEqual(response.status_code, 200)

    def test_unaccepted_user_gets_403(self):
        self.client.login(username="itemapiunaccepted", password="testpass123")
        response = self.client.get("/item-location/api/locations/")
        self.assertEqual(response.status_code, 403)
