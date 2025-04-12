# Tests

* Various tests provided by GitHub Copilot.
* Some tests have worked as expected and some have not.

## Accounts

* [`accounts/tests/test_customuser_model.py`](../accounts/tests/test_customuser_model.py):

    ```python
    class CustomUserModelTest(TestCase):
        #...
        def test_has_registration_accepted_field(self):
            """
            `CustomUser` model should have `registration_accepted` field.
            """
            self.assertTrue(hasattr(CustomUser, 'registration_accepted'))

        def test_registration_accepted_field_is_boolean_field(self):
            """
            `CustomUser` model `registration_accepted` field should be `BooleanField`.
            """
            self.assertIsInstance(CustomUser.registration_accepted, models.BooleanField)

        def test_registration_accepted_default_attribute(self):
            """
            `CustomUser` model `registration_accepted` field `default` attribute should be `False`.
            """
            self.assertFalse(CustomUser.registration_accepted.default)

        def test_dunder_string(self):
            """
            `CustomUser` model `__str__` method should return `self.username`.
            """
            user = CustomUser.objects.create(
                username=A_TEST_USERNAME,
            )
            self.assertEqual(str(user), A_TEST_USERNAME)
    ```

* [`accounts/tests/test_custom_user_views.py`](../accounts/tests/test_custom_user_views.py):

    ```python
    class CustomUserSignUpViewTest(TestCase):
        """
        Tests for `CustomUser` sign up view.
        """

        def test_signup_view_url_exists_at_desired_location(self):
            """
            `CustomUser` sign up view should be accessible at `/accounts/signup/`.
            """
            response = self.client.get(CUSTOM_USER_SIGNUP_URL)
            self.assertEqual(response.status_code, 200)

        def test_signup_view_url_accessible_by_name(self):
            """
            `CustomUser` sign up view should be accessible by name.
            """
            response = self.client.get(reverse(CUSTOM_USER_SIGNUP_VIEW_NAME))
            self.assertEqual(response.status_code, 200)

        def test_signup_view_uses_correct_template(self):
            """
            `CustomUser` sign up view should use `registration/signup.html` template.
            """
            response = self.client.get(reverse(CUSTOM_USER_SIGNUP_VIEW_NAME))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, CUSTOM_USER_SIGNUP_TEMPLATE)

        def test_signup_view_has_the_site_name_in_context(self):
            """
            `CustomUser` sign up view should have `the_site_name` in the context.
            """
            response = self.client.get(reverse(CUSTOM_USER_SIGNUP_VIEW_NAME))
            self.assertEqual(response.status_code, 200)
            self.assertIn("the_site_name", response.context)
            self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)

        def test_signup_view_has_hide_signup_link_in_context(self):
            """
            `CustomUser` sign up view should have `hide_signup_link` in the context.
            """
            response = self.client.get(reverse(CUSTOM_USER_SIGNUP_VIEW_NAME))
            self.assertEqual(response.status_code, 200)
            self.assertIn("hide_signup_link", response.context)
            self.assertTrue(response.context["hide_signup_link"])

        def test_signup_view_has_form_in_context(self):
            """
            `CustomUser` sign up view should have `form` in the context.
            """
            response = self.client.get(reverse(CUSTOM_USER_SIGNUP_VIEW_NAME))
            self.assertEqual(response.status_code, 200)
            self.assertIn("form", response.context)

        def test_signup_view_has_form_with_username_field(self):
            """
            `CustomUser` sign up view should have `form` in the context with `username` field.
            """
            response = self.client.get(reverse(CUSTOM_USER_SIGNUP_VIEW_NAME))
            self.assertEqual(response.status_code, 200)
            self.assertIn("form", response.context)
            self.assertIn("username", response.context["form"].fields)
    ```

    ```python
    class CustomLoginViewTest(TestCase):
        """
        Tests for `CustomLoginView` view.
        """

        def test_login_view_url_exists_at_desired_location(self):
            """
            `CustomUser` login view should be accessible at `/accounts/login/`.
            """
            response = self.client.get(CUSTOM_USER_LOGIN_URL)
            self.assertEqual(response.status_code, 200)

        def test_login_view_url_accessible_by_name(self):
            """
            `CustomUser` login view should be accessible by name.
            """
            response = self.client.get(reverse(CUSTOM_USER_LOGIN_VIEW_NAME))
            self.assertEqual(response.status_code, 200)

        def test_login_view_uses_correct_form(self):
            """
            `CustomUser` login view should use `AuthenticationForm`.
            """
            response = self.client.get(reverse(CUSTOM_USER_LOGIN_VIEW_NAME))
            self.assertEqual(response.status_code, 200)
            self.assertIn("form", response.context)
            self.assertEqual(response.context["form"].__class__.__name__, "AuthenticationForm")

        def test_login_view_redirects_to_correct_view_on_success(self):
            """
            `CustomUser` login view should redirect to the `home` view on success.
            """
            CustomUser.objects.create_user(
                username=A_TEST_USERNAME, password=A_TEST_PASSWORD
            )
            response = self.client.post(
                reverse(CUSTOM_USER_LOGIN_VIEW_NAME),
                {"username": A_TEST_USERNAME, "password": A_TEST_PASSWORD},
            )
            self.assertRedirects(
                response,
                reverse_lazy("home"),
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True,
            )

        def test_login_view_uses_correct_template(self):
            """
            `CustomUser` login view should use `registration/login.html` template.
            """
            response = self.client.get(CUSTOM_USER_LOGIN_URL)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, CUSTOM_USER_LOGIN_TEMPLATE)

        def test_login_view_has_the_site_name_in_context(self):
            """
            `CustomUser` login view should have `the_site_name` in the context.
            """
            response = self.client.get(CUSTOM_USER_LOGIN_URL)
            self.assertEqual(response.status_code, 200)
            self.assertIn("the_site_name", response.context)
            self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)

        # This probably doesn't need to be tested since the form is provided by a built-in Django view.
        def test_login_view_uses_correct_form(self):
            """
            `CustomUser` login view should use `AuthenticationForm`.
            """
            response = self.client.get(reverse(CUSTOM_USER_LOGIN_VIEW_NAME))
            self.assertEqual(response.status_code, 200)
            self.assertIn("form", response.context)
            self.assertEqual(response.context["form"].__class__.__name__, "AuthenticationForm")

    ```

## Inspirational

* [`boosts/tests/test_inspirational_model.py`](../boosts/tests/test_inspirational_model.py):

    ```python
    def test_get_absolute_url(self):
        """
        `get_absolute_url` method should return a string in the format:
        `/boosts/inspirational/<id>/`
        """
        inspirational = Inspirational.objects.get(id=1)
        expected_url = f'/boosts/inspirational/{inspirational.id}/'
        self.assertEqual(inspirational.get_absolute_url(), expected_url)
    ```

* [`boosts/models.py`](../boosts/models.py):

    ```python
    class Inspirational(models.Model):
        # ...
        def get_absolute_url(self):
            return reverse("boosts:inspirational-detail", kwargs={"pk": self.pk})
    ```
