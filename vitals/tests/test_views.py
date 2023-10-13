from django.test import RequestFactory, TestCase
from django.urls import reverse

from accounts.models import CustomUser
from vitals.models import BloodPressure

USERNAME_REGISTRATION_ACCEPTED_TRUE = "RegisteredUser"
USERNAME_REGISTRATION_ACCEPTED_FALSE = "UnregisteredUser"
PASSWORD_FOR_TESTING = "a_test_password"

THE_SITE_NAME = "Personal Assistant"

HOME_URL = "/"

BLOOD_PRESSURE_LIST_URL = "/vitals/bloodpressures/"
BLOOD_PRESSURE_LIST_VIEW_NAME = "vitals:bloodpressure-list"
BLOOD_PRESSURE_LIST_PAGE_TITLE = "Blood Pressures"
BLOOD_PRESSURE_LIST_TEMPLATE = "vitals/bloodpressure_list.html"

BLOOD_PRESSURE_SYSTOLIC_1 = 120
BLOOD_PRESSURE_DIASTOLIC_1 = 80
BLOOD_PRESSURE_PULSE__1 = 72
BLOOD_PRESSURE_SYSTOLIC_2 = 110
BLOOD_PRESSURE_DIASTOLIC_2 = 70
BLOOD_PRESSURE_PULSE__2 = 72

BLOOD_PRESSURE_SYSTOLIC_MAX = 120
BLOOD_PRESSURE_SYSTOLIC_MIN = 110
BLOOD_PRESSURE_DIASTOLIC_MAX = 80
BLOOD_PRESSURE_DIASTOLIC_MIN = 70


class HomeViewTest(TestCase):
    """
    Test the `home` view.
    """

    def test_home_view_url_exists_at_desired_location(self):
        """
        Test that the `home` view is rendered at the desired location.
        """
        response = self.client.get(HOME_URL)
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_accessible_by_name(self):
        """
        Test that the `home` view is rendered at the desired location by name.
        """
        response = self.client.get(reverse("vitals:home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """
        Test that the `home` view uses the correct template.
        """
        response = self.client.get(reverse("vitals:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vitals/home.html")

    def test_home_view_uses_correct_context(self):
        """
        Test that the `home` view uses the correct context.
        """
        response = self.client.get(reverse("vitals:home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)
        self.assertEqual(response.context["page_title"], "Vitals Home")


class BloodPressureListViewTest(TestCase):
    """
    Test the `BloodPressureListView` view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create `CustomUser`s object and `BloodPressure`s object for testing.
        """
        cls.factory = RequestFactory()
        # Create a `CustomUser` object for testing.
        cls.user = CustomUser.objects.create_user(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
            registration_accepted=True,
        )
        # Create a `BloodPressure` object for testing.
        cls.blood_pressure_1 = BloodPressure.objects.create(
            user=cls.user,
            systolic=BLOOD_PRESSURE_SYSTOLIC_1,
            diastolic=BLOOD_PRESSURE_DIASTOLIC_1,
            pulse=BLOOD_PRESSURE_PULSE__1,
        )
        cls.blood_pressure_2 = BloodPressure.objects.create(
            user=cls.user,
            systolic=BLOOD_PRESSURE_SYSTOLIC_2,
            diastolic=BLOOD_PRESSURE_DIASTOLIC_2,
            pulse=BLOOD_PRESSURE_PULSE__2,
        )

    def test_url_exists_at_desired_location(self):
        """
        Test that the `BloodPressureListView` view is rendered at the desired
        location.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        self.assertTrue(login)
        response = self.client.get(BLOOD_PRESSURE_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        """
        Test that the `BloodPressureListView` view is rendered at the desired
        location by name.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(BLOOD_PRESSURE_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        """
        Test that the `BloodPressureListView` view uses the correct template.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(BLOOD_PRESSURE_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, BLOOD_PRESSURE_LIST_TEMPLATE)

    def test_get_context_data(self):
        """
        Test `get_context_data` method of `BloodPressureListView`.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(BLOOD_PRESSURE_LIST_VIEW_NAME))
        self.assertEqual(
            response.context["page_title"],
            BLOOD_PRESSURE_LIST_PAGE_TITLE,
        )
        self.assertEqual(
            response.context["bloodpressure_list"].count(),
            BloodPressure.objects.filter(user=self.user).count(),
        )

    def test_has_correct_context_with_one_blood_pressure(self):
        """
        Test that the `BloodPressureListView` view uses the correct context.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        self.assertTrue(login)
        self.blood_pressure_2.delete()
        response = self.client.get(reverse(BLOOD_PRESSURE_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)
        self.assertEqual(
            response.context["page_title"], BLOOD_PRESSURE_LIST_PAGE_TITLE)
        self.assertEqual(
            response.context["bloodpressure_list"][0].systolic,
            BLOOD_PRESSURE_SYSTOLIC_1,
        )
        self.assertEqual(
            response.context["bloodpressure_list"][0].diastolic,
            BLOOD_PRESSURE_DIASTOLIC_1,
        )
        self.assertEqual(
            response.context[
                "bloodpressure_list"
            ][0].user.registration_accepted,
            True,
        )
        self.assertEqual(
            response.context["bloodpressure_list"][0].user.username,
            USERNAME_REGISTRATION_ACCEPTED_TRUE,
        )

    def test_context_has_user_pressure_range(self):
        """
        Test that the `BloodPressureListView` view uses the correct context.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        self.assertTrue(login)
        response = self.client.get(reverse(BLOOD_PRESSURE_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)
        self.assertEqual(
            response.context["page_title"], BLOOD_PRESSURE_LIST_PAGE_TITLE)
        self.assertEqual(
            response.context["user_pressure_range"],
            {
                "systolic_min": BLOOD_PRESSURE_SYSTOLIC_MIN,
                "diastolic_min": BLOOD_PRESSURE_DIASTOLIC_MIN,
                "systolic_max": BLOOD_PRESSURE_SYSTOLIC_MAX,
                "diastolic_max": BLOOD_PRESSURE_DIASTOLIC_MAX,
            }
        )

    def test_has_basic_context_with_zero_blood_pressures(self):
        """
        Test that the `BloodPressureListView` view uses the correct context.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        # Verify that user is logged in.
        self.assertTrue(login)
        # Delete the `BloodPressure` object for testing.
        self.blood_pressure_1.delete()
        response = self.client.get(reverse(BLOOD_PRESSURE_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)
        self.assertEqual(
            response.context["page_title"], BLOOD_PRESSURE_LIST_PAGE_TITLE)

    def test_has_blood_pressure_context_with_zero_blood_pressures(self):
        """
        Test that the `BloodPressureListView` view uses the correct context.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        # Verify that user is logged in.
        self.assertTrue(login)
        # Delete the `BloodPressure` object for testing.
        self.blood_pressure_1.delete()
        self.blood_pressure_2.delete()
        response = self.client.get(reverse(BLOOD_PRESSURE_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["user_averages_and_medians"],
            {
                "systolic_average": None,
                "diastolic_average": None,
                "systolic_median": None,
                "diastolic_median": None,
            }
        )

    def test_redirects_to_login_if_not_logged_in(self):
        """
        Test that the `BloodPressureListView` view redirects to login if not
        logged in.
        """
        response = self.client.get(BLOOD_PRESSURE_LIST_URL)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/vitals/bloodpressures/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_redirects_to_login_if_logged_in_but_registration_not_accepted(
        self,
    ):
        """
        Test that the `BloodPressureListView` view redirects to login if logged
        in but registration not accepted.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        self.assertFalse(login)
        response = self.client.get(BLOOD_PRESSURE_LIST_URL)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/vitals/bloodpressures/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
