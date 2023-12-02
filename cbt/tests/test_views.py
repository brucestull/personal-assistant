# Import get_user_model() to get the `User` model.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class HomeViewTest(TestCase):
    """
    Tests for `home` view.
    """

    def test_home_view_url_exists_at_desired_location(self):
        """
        Test that home view exists at desired location.
        """
        response = self.client.get("/cbt/")
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_accessible_by_name(self):
        """
        Test that home view is accessible by name.
        """
        response = self.client.get(reverse("cbt:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """
        Test that home view uses correct template.
        """
        response = self.client.get(reverse("cbt:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cbt/home.html")

    def test_home_view_has_correct_context(self):
        """
        Test that home view has correct context.
        """
        response = self.client.get(reverse("cbt:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")
        self.assertEqual(response.context["page_title"], "Cognitive Behavioral Therapy")


class CognitiveDistortionListViewTest(TestCase):
    """
    Tests for `CognitiveDistortionListView` view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.
        """
        # Create a registration_accepted True user.
        cls.registered_user_dezzi = get_user_model().objects.create_user(
            username="RegisteredDezzi",
            password="MeowMeow42",
            email="RegisteredDezzi@purr.scratch",
            registration_accepted=True,
        )
        # This is probably not necessary:
        # registered_user_dezzi.save()
        cls.unregistered_user_bunbun = get_user_model().objects.create_user(
            username="UnRegisteredBunBun",
            password="MeowMeow42",
            email="UnRegisteredBunBun@purr.scratch",
            registration_accepted=False,
        )

    # TODO: Test that class model is `CognitiveDistortion`

    def test_unauthenticated_user_routed_to_login(self):
        """
        Test that cognitive distortion list view redirects unregistered users.
        """
        response = self.client.get("/cbt/cognitive-distortions/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/cbt/cognitive-distortions/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    # TODO: Unregistered users should be redirected to a page that says their
    # registartion is not yet accepted.

    def test_url_exists_for_registered_user(self):
        """
        Test that cognitive distortion list view exists for registered users.
        """
        self.client.login(username="RegisteredDezzi", password="MeowMeow42")
        response = self.client.get("/cbt/cognitive-distortions/")
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        """
        Test that cognitive distortion list view is accessible by name.
        """
        self.client.login(username="RegisteredDezzi", password="MeowMeow42")
        response = self.client.get(reverse("cbt:cognitive-distortion-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test that cognitive distortion list view uses correct template.
        """
        self.client.login(username="RegisteredDezzi", password="MeowMeow42")
        response = self.client.get(reverse("cbt:cognitive-distortion-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cbt/cognitivedistortion_list.html")

    def test_view_has_correct_context(self):
        """
        Test that cognitive distortion list view has correct context.
        """
        self.client.login(username="RegisteredDezzi", password="MeowMeow42")
        response = self.client.get(reverse("cbt:cognitive-distortion-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")
        self.assertEqual(response.context["page_title"], "Cognitive Distortions")
        self.assertIn("cognitivedistortion_list", response.context)
        self.assertIn("object_list", response.context)


class ThoughtListViewTest(TestCase):
    """
    Tests for `ThoughtListView` view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole TestCase.
        """
        # Create a registration_accepted True user.
        cls.registered_user_dezzi = get_user_model().objects.create_user(
            username="RegisteredDezzi",
            password="MeowMeow42",
            email="RegisteredDezzi@purr.scratch",
            registration_accepted=True,
        )
        # Create a registration_accepted False user.
        cls.unregistered_user_bunbun = get_user_model().objects.create_user(
            username="UnRegisteredBunBun",
            password="MeowMeow42",
            email="UnRegisteredBunBun@purr.scratch",
            registration_accepted=False,
        )

    def test_unauthenticated_user_routed_to_login(self):
        """
        Test that thought list view redirects unregistered users.
        """
        response = self.client.get("/cbt/thoughts/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/cbt/thoughts/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_url_exists_for_registered_user(self):
        """
        Test that thought list view exists for registered users.
        """
        self.client.login(username="RegisteredDezzi", password="MeowMeow42")
        response = self.client.get("/cbt/thoughts/")
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        """
        Test that thought list view is accessible by name.
        """
        self.client.login(username="RegisteredDezzi", password="MeowMeow42")
        response = self.client.get(reverse("cbt:thought-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test that thought list view uses correct template.
        """
        self.client.login(username="RegisteredDezzi", password="MeowMeow42")
        response = self.client.get(reverse("cbt:thought-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cbt/thought_list.html")

    def test_view_has_correct_context(self):
        """
        Test that thought list view has correct context.
        """
        self.client.login(username="RegisteredDezzi", password="MeowMeow42")
        response = self.client.get(reverse("cbt:thought-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")
        self.assertEqual(response.context["page_title"], "Thoughts")
        self.assertIn("thought_list", response.context)
        self.assertIn("object_list", response.context)
