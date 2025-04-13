from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse

from accounts.models import CustomUser
from boosts.forms import InspirationalForm
from boosts.models import Inspirational
from boosts.views import InspirationalListView


class InspirationalListViewTest(TestCase):
    """
    Test the InspirationalListView.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create `CustomUser`s and `Inspirational`s for testing.
        """
        cls.factory = RequestFactory()
        # Create users for testing.
        cls.user_registration_accepted_true = CustomUser.objects.create_user(
            username="RegisteredUser",
            password="a_test_password",
            registration_accepted=True,
        )
        cls.user_registration_accepted_false = CustomUser.objects.create_user(
            username="UnregisteredUser",
            password="a_test_password",
            registration_accepted=False,
        )
        # Create inspirationals for testing.
        for inspirational_id in range(13):
            Inspirational.objects.create(
                author=cls.user_registration_accepted_true,
                body=f"Body for inspirational {inspirational_id}",
            )

    def test_view_redirects_to_login_if_user_is_not_authenticated(self):
        """
        View should redirect user to login view if user is not authenticated.
        """
        response = self.client.get("/boosts/inspirationals/")
        self.assertRedirects(
            response, f"{'/accounts/login/'}?next={'/boosts/inspirationals/'}"
        )

    def test_view_url_returns_200_if_user_is_authenticated(self):
        """
        View should return 200 if user is authenticated.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        response = self.client.get("/boosts/inspirationals/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(login)

    def test_view_accessible_by_name(self):
        """
        View should be accessible by name.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get(reverse("boosts:inspirational-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        View should use the correct template.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/inspirationals/")
        self.assertTemplateUsed(response, "boosts/inspirational_list.html")

    def test_view_pagination_is_ten(self):
        """
        View should paginate the list of `Inspirational`s by `10` (10).
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/inspirationals/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["object_list"]) == 10)

    def test_view_returns_inspirational_objects(self):
        """
        View should return `Inspirational` objects.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/inspirationals/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("object_list" in response.context)
        self.assertTrue(len(response.context["object_list"]) == 10)
        for object in response.context["object_list"]:
            self.assertIsInstance(object, Inspirational)

    def test_view_returns_all_inspirationals(self):
        """
        View should return all `Inspirational`s.

        Page one should show 10 `Inspirational`s.
        Page two should show the 3 remaining `Inspirational`s.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response_page_one = self.client.get("/boosts/inspirationals/")
        self.assertEqual(response_page_one.status_code, 200)
        self.assertTrue("is_paginated" in response_page_one.context)
        self.assertTrue(response_page_one.context["is_paginated"])
        self.assertTrue(len(response_page_one.context["object_list"]) == 10)
        response_page_two = self.client.get("/boosts/inspirationals/" + "?page=2")
        self.assertEqual(response_page_two.status_code, 200)
        self.assertTrue("is_paginated" in response_page_two.context)
        self.assertTrue(response_page_two.context["is_paginated"])
        self.assertTrue(len(response_page_two.context["object_list"]) == 3)

    def test_view_for_authenticated_registration_accepted_false_user(self):
        """
        View should return 403 if user is authenticated and registration_accepted is
        False.
        """
        login = self.client.login(
            username="UnregisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/inspirationals/")
        self.assertEqual(response.status_code, 403)

    def test_view_for_authenticated_registration_accepted_true_user(self):
        """
        View should return 200 if user is authenticated and registration_accepted is
        True.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/inspirationals/")
        self.assertEqual(response.status_code, 200)

    def test_view_for_unauthenticated_user(self):
        """
        View should return 302 if user is not authenticated.
        """
        response = self.client.get("/boosts/inspirationals/")
        self.assertEqual(response.status_code, 302)

    def test_view_get_queryset_method_when_user_unauthenticated(self):
        """
        View `get_queryset` should return `Inspirational.objects.none()` if user is not
        authenticated.
        """
        # Create an instance of a GET request for testing the `get_queryset` method:
        request = self.factory.get("/boosts/inspirationals/")

        # Simulate an unauthenticated user
        request.user = AnonymousUser()

        # Instantiate the view with the mock request
        view = InspirationalListView()
        view.setup(request)

        # Call get_queryset directly
        queryset = view.get_queryset()

        # Perform your test assertions
        self.assertEqual(queryset.count(), 0)


class InspirationalCreateViewTest(TestCase):
    """
    Test `InspirationalCreateView`.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create test data.
        """
        # Create users for testing.
        cls.user_registration_accepted_true = CustomUser.objects.create_user(
            username="RegisteredUser",
            password="a_test_password",
            registration_accepted=True,
        )
        cls.user_registration_accepted_false = CustomUser.objects.create_user(
            username="UnregisteredUser",
            password="a_test_password",
            registration_accepted=False,
        )

    def test_view_uses_proper_form_class(self):
        """
        View should use the proper form class.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/create/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertIsInstance(response.context["form"], InspirationalForm)

    def test_view_uses_proper_template(self):
        """
        View should use the proper template.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/create/")
        self.assertTemplateUsed(response, "boosts/inspirational_form.html")

    def test_view_routes_to_proper_success_url(self):
        """
        View should route to the proper success URL.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.post(
            "/boosts/create/",
            data={
                "body": "This is a test inspirational body.",
                "author": "Test author",
            },
        )
        self.assertRedirects(response, "/boosts/inspirationals/")

    def test_view_redirects_if_user_not_logged_in(self):
        """
        View should redirect if user is not logged in.
        """
        response = self.client.get("/boosts/create/")
        self.assertTrue(response.status_code, 302)
        self.assertRedirects(response, f"{'/accounts/login/'}?next={'/boosts/create/'}")

    def test_view_returns_403_if_user_registration_accepted_false(self):
        """
        View should return 403 if user registration_accepted False.
        """
        login = self.client.login(
            username="UnregisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/create/")
        self.assertEqual(response.status_code, 403)

    def test_view_returns_200_if_user_registration_accepted_true(self):
        """
        View should return 200 if user registration_accepted True.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/create/")
        self.assertEqual(response.status_code, 200)

    def test_view_context_contains_page_title(self):
        """
        View context should contain page title.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/create/")
        # Test that `page_title` is in `response.context`
        self.assertTrue("page_title" in response.context)
        # Test that `page_title` is equal to "Create an Inspirational"
        self.assertEqual(response.context["page_title"], "Create an Inspirational")

    def test_view_context_contains_the_site_name(self):
        """
        View context should contain the site name.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/create/")
        self.assertTrue("the_site_name" in response.context)
        self.assertEqual(response.context["the_site_name"], "Personal Assistant")

    def test_view_context_contains_hide_inspirational_create_link(self):
        """
        View context should contain hide_inspirational_create_link.
        """
        login = self.client.login(
            username="RegisteredUser",
            password="a_test_password",
        )
        self.assertTrue(login)
        response = self.client.get("/boosts/create/")
        self.assertTrue("hide_inspirational_create_link" in response.context)
        self.assertEqual(response.context["hide_inspirational_create_link"], True)


class SendInspirationalViewTest(TestCase):
    """
    Test `send_inspirational` view.
    """

    pass
    # @classmethod
    # def setUpTestData(cls):
    #     """
    #     Create test data.
    #     """
    #     # Create users for testing.
    #     cls.user_registration_accepted_true = CustomUser.objects.create_user(
    #         username="RegisteredUser",
    #         password="a_test_password",
    #         registration_accepted=True,
    #     )
    #     cls.user_registration_accepted_false = CustomUser.objects.create_user(
    #         username="UnregisteredUser",
    #         password="a_test_password",
    #         registration_accepted=False,
    #     )
    #     cls.user_beastie = CustomUser.objects.create_user(
    #         username="Beastie",
    #         password="a_test_password",
    #         registration_accepted=True,
    #     )
    #     # Create inspirationals for testing.
    #     for inspirational_id in range(13):
    #         Inspirational.objects.create(
    #             author=cls.user_registration_accepted_true,
    #             body=f"Body for inspirational {inspirational_id}",
    #         )

    # def test_view_redirects_to_login_if_user_is_not_authenticated(self):
    #     """
    #     View should redirect user to login view if user is not authenticated.
    #     """
    #     response = self.client.get("/boosts/send_inspirational/1/")
    #     self.assertRedirects(
    #         response,
    #         f"{'/accounts/login/'}?next={'/boosts/send_inspirational/1/'}",
    #     )

    # def test_view_returns_403_if_user_registration_accepted_false(self):
    #     """
    #     View should return 403 if user registration_accepted False.
    #     """
    #     login = self.client.login(
    #         username="UnregisteredUser",
    #         password="a_test_password",
    #     )
    #     self.assertTrue(login)
    #     response = self.client.get("/boosts/send_inspirational/1/")
    #     self.assertEqual(response.status_code, 403)

    # def test_view_returns_200_if_user_registration_accepted_true(self):
    #     """
    #     View should return 200 if user registration_accepted True.
    #     """
    #     login = self.client.login(
    #         username="RegisteredUser",
    #         password="a_test_password",
    #     )
    #     self.assertTrue(login)
    #     response = self.client.get("/boosts/send_inspirational/1/")
    #     self.assertEqual(response.status_code, 200)

    # def test_view_returns_404_if_inspirational_does_not_exist(self):
    #     """
    #     View should return 404 if `Inspirational` does not exist.
    #     """
    #     login = self.client.login(
    #         username="RegisteredUser",
    #         password="a_test_password",
    #     )
    #     self.assertTrue(login)
    #     # Test with an `Inspirational` that does not exist.
    #     response = self.client.get("/boosts/send_inspirational/999/")
    #     self.assertEqual(response.status_code, 404)

    # def test_view_returns_404_if_inspirational_exists_but_user_is_not_author(self):
    #     """
    #     View should return 404 if `Inspirational` exists but user is not author.
    #     """
    #     login = self.client.login(
    #         username="Beastie",
    #         password="a_test_password",
    #     )
    #     self.assertTrue(login)
    #     # Test with an `Inspirational` that exists but the user is not the author.
    #     response = self.client.get("/boosts/send_inspirational/1/")
    #     self.assertEqual(response.status_code, 404)

    # def test_view_returns_200_if_inspirational_exists_and_user_is_author(self):
    #     """
    #     View should return 200 if `Inspirational` exists and user is author.
    #     """
    #     login = self.client.login(
    #         username="RegisteredUser",
    #         password="a_test_password",
    #     )
    #     self.assertTrue(login)
    #     # Test with an `Inspirational` that exists and the user is the author.
    #     response = self.client.get("/boosts/send_inspirational/1/")
    #     self.assertEqual(response.status_code, 200)

    # def test_view_uses_proper_template(self):
    #     """
    #     View should use the proper template.
    #     """
    #     login = self.client.login(
    #         username="RegisteredUser",
    #         password="a_test_password",
    #     )
    #     self.assertTrue(login)
    #     # Test with an `Inspirational` that exists and the user is the author.
    #     response = self.client.get("/boosts/send_inspirational/1/")
    #     self.assertTemplateUsed(response, "boosts/send_inspirational.html")

    # def test_view_context_contains_page_title(self):
    #     """
    #     View context should contain page title.
    #     """
    #     login = self.client.login(
    #         username="RegisteredUser",
    #         password="a_test_password",
    #     )
    #     self.assertTrue(login)
    #     # Test with an `Inspirational` that exists and the user is the author.
    #     response = self.client.get("/boosts/send_inspirational/1/")
    #     # Test that `page_title` is in `response.context`
    #     self.assertTrue("page_title" in response.context)
    #     # Test that `page_title` is equal to "Send an Inspirational"
    #     self.assertEqual(response.context["page_title"], "Send an Inspirational")

    # def test_view_context_contains_the_site_name(self):
    #     """
    #     View context should contain the site name.
    #     """
    #     login = self.client.login(
    #         username="RegisteredUser",
    #         password="a_test_password",
    #     )
    #     self.assertTrue(login)
    #     # Test with an `Inspirational` that exists and the user is the author.
    #     response = self.client.get("/boosts/send_inspirational/1/")
    #     self.assertTrue("the_site_name" in response.context)
    #     self.assertEqual(response.context["the_site_name"], "Personal Assistant")

    # def test_view_context_contains_hide_inspirational_create_link(self):
    #     """
    #     View context should contain hide_inspirational_create_link.
    #     """
    #     login = self.client.login(
    #         username="RegisteredUser",
    #         password="a_test_password",
    #     )
    #     self.assertTrue(login)
    #     # Test with an `Inspirational` that exists and the user is the author.
    #     response = self.client.get("/boosts/send_inspirational/1/")
    #     self.assertTrue("hide_inspirational_create_link" in response.context)
    #     self.assertEqual(response.context["hide_inspirational_create_link"], True)
