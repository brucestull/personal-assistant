from django.test import TestCase
from django.contrib.auth import get_user_model


class PharmaceuticalListViewTest(TestCase):
    """
    Test the `PharmaceuticalListView` view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create a user.
        """

        # Create a user.
        cls.user_01 = get_user_model().objects.create_user(
            username="DezziKitten01",
            email="DezziKitten01@purr.scratch",
            password="MeowMeow42",
            registration_accepted=True,
        )
        cls.user_02 = get_user_model().objects.create_user(
            username="DezziKitten02",
            email="DezziKitten02@purr.scratch",
            password="MeowMeow42",
            registration_accepted=True,
        )
        cls.user_ra_false = get_user_model().objects.create_user(
            username="RegistrationAcceptedFalse",
            email="RegistrationAcceptedFalse@purr.scratch",
            password="MeowMeow42",
            registration_accepted=False,
        )
        # Create a pharmaceutical.
        cls.pharmaceutical_01 = cls.user_01.pharmaceutical_set.create(
            name="Test Pharmaceutical",
            description="This is a test pharmaceutical.",
            is_active=True,
            prescription_required=True,
        )
        cls.pharmaceutical_02 = cls.user_02.pharmaceutical_set.create(
            name="Test Pharmaceutical 2",
            description="This is a test pharmaceutical.",
            is_active=True,
            prescription_required=True,
        )

    def test_pharmaceutical_list_view_url_with_authenticated_user(self):
        """
        Test that the `PharmaceuticalListView` view is rendered at
        "/pharma-tracker/" for a user who is authenticated and has
        "registration_accepted" set to "True".
        """
        login = self.client.login(
            username=self.user_01.username,
            password="MeowMeow42",
        )
        self.assertTrue(login)
        response = self.client.get("/pharma-tracker/")
        self.assertEqual(response.status_code, 200)

    def test_pharmaceutical_list_view_url_with_unauthenticated_user(self):
        """
        Test that a request to "/pharma-tracker/" for a user who is not
        authenticated redirects to login.
        """
        response = self.client.get("/pharma-tracker/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/pharma-tracker/",
        )
