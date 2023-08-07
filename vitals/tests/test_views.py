from django.http import HttpRequest
from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse

from vitals.models import BloodPressure
from vitals.models import Pulse
from vitals.views import BloodPressureListView

from accounts.models import CustomUser


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
        cls.blood_pressure = BloodPressure.objects.create(
            user=cls.user,
            systolic=BLOOD_PRESSURE_SYSTOLIC_1,
            diastolic=BLOOD_PRESSURE_DIASTOLIC_1,
        )

    def test_blood_pressure_list_view_url_exists_at_desired_location(self):
        """
        Test that the `BloodPressureListView` view is rendered at the desired location.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(BLOOD_PRESSURE_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_blood_pressure_list_view_url_accessible_by_name(self):
        """
        Test that the `BloodPressureListView` view is rendered at the desired location by name.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(reverse(BLOOD_PRESSURE_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)

    def test_blood_pressure_list_view_uses_correct_template(self):
        """
        Test that the `BloodPressureListView` view uses the correct template.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(reverse(BLOOD_PRESSURE_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, BLOOD_PRESSURE_LIST_TEMPLATE)

    def test_blood_pressure_list_view_uses_correct_context(self):
        """
        Test that the `BloodPressureListView` view uses the correct context.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(reverse(BLOOD_PRESSURE_LIST_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["the_site_name"], THE_SITE_NAME)
        self.assertEqual(response.context["page_title"], BLOOD_PRESSURE_LIST_PAGE_TITLE)
        self.assertEqual(
            response.context["bloodpressure_list"][0].systolic, BLOOD_PRESSURE_SYSTOLIC_1
        )
        self.assertEqual(
            response.context["bloodpressure_list"][0].diastolic, BLOOD_PRESSURE_DIASTOLIC_1
        )
        self.assertEqual(
            response.context["bloodpressure_list"][0].user.registration_accepted, True
        )
        self.assertEqual(
            response.context["bloodpressure_list"][0].user.username,
            USERNAME_REGISTRATION_ACCEPTED_TRUE,
        )

    def test_blood_pressure_list_view_redirects_to_login_if_not_logged_in(self):
        """
        Test that the `BloodPressureListView` view redirects to login if not logged in.
        """
        response = self.client.get(BLOOD_PRESSURE_LIST_URL)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/vitals/bloodpressures/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_blood_pressure_list_view_redirects_to_login_if_logged_in_but_registration_not_accepted(
        self,
    ):
        """
        Test that the `BloodPressureListView` view redirects to login if logged in but registration not accepted.
        """
        login = self.client.login(
            username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
            password=PASSWORD_FOR_TESTING,
        )
        response = self.client.get(BLOOD_PRESSURE_LIST_URL)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/vitals/bloodpressures/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    # def test_blood_pressure_list_view_get_context_data_with_averages_and_medians(self):
    #     """
    #     Test that the `BloodPressureListView` view get_context_data method works correctly.
    #     """
    #     login = self.client.login(
    #         username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
    #         password=PASSWORD_FOR_TESTING,
    #     )
    #     request = self.factory.get("/")
    #     request.user = self.user
    #     view = BloodPressureListView()
    #     view.setup(request=request)
    #     view.object_list = BloodPressure.objects.all()
    #     context = view.get_context_data()
    #     self.assertEqual(context["user_averages_and_medians"]["systolic_average"], 120)
    #     self.assertEqual(context["user_averages_and_medians"]["diastolic_average"], 80)
    #     self.assertEqual(context["user_averages_and_medians"]["systolic_median"], 120)
    #     self.assertEqual(context["user_averages_and_medians"]["diastolic_median"], 80)

    # def test_blood_pressure_list_view_get_context_data_with_averages_and_medians(self):
    #     """
    #     Test that the `BloodPressureListView` view get_context_data method works correctly.
    #     """
    #     login = self.client.login(
    #         username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
    #         password=PASSWORD_FOR_TESTING,
    #     )
    #     request = self.factory.get("/")
    #     request.user = self.user
    #     view = BloodPressureListView()
    #     view.setup(request=request)
    #     view.object_list = CustomUser.get_average_and_median_blood_pressure(self)
    #     context = view.get_context_data()
    #     self.assertEqual(context["user_averages_and_medians"]["systolic_average"], 120)
    #     self.assertEqual(context["user_averages_and_medians"]["diastolic_average"], 80)
    #     self.assertEqual(context["user_averages_and_medians"]["systolic_median"], 120)
    #     self.assertEqual(context["user_averages_and_medians"]["diastolic_median"], 80)

    # def test_blood_pressure_list_view_get_context_data_when_no_blood_pressures(self):
    #     """
    #     Test that the `BloodPressureListView` view get_context_data method works when there are no blood pressures.
    #     """
    #     login = self.client.login(
    #         username=USERNAME_REGISTRATION_ACCEPTED_TRUE,
    #         password=PASSWORD_FOR_TESTING,
    #     )
    #     request = self.factory.get("/")
    #     request.user = self.user
    #     view = BloodPressureListView()
    #     view.setup(request=request)
    #     for blood_pressure in BloodPressure.objects.all():
    #         blood_pressure.delete()
    #     view.object_list = BloodPressure.objects.all()
    #     context = view.get_context_data()
    #     self.assertEqual(context["systolic_average"], None)
    #     self.assertEqual(context["diastolic_average"], None)
    #     self.assertEqual(context["systolic_median"], None)
    #     self.assertEqual(context["diastolic_median"], None)
