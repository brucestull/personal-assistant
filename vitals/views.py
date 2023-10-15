from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import CreateView, ListView

from config.settings import THE_SITE_NAME
from vitals.models import BloodPressure


def home(request):
    """
    View function for the home page of the `vitals` app.
    """
    return render(
        request,
        "vitals/home.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "Vitals Home",
        },
    )


class BloodPressureListView(LoginRequiredMixin, ListView):
    """
    `ListView` for a user's blood pressure measurements.
    """

    """
    The model attribute `model = BloodPressure` is not needed because the
    `get_queryset` method is defined.
    model = BloodPressure

    The template_name attribute `template_name =
    "vitals/bloodpressure_list.html"` is not needed since Django will use
    the default template name.
    template_name = "vitals/bloodpressure_list.html"

    The context_object_name attribute `context_object_name =
    "bloodpressure_list"` is not needed since Django will use the default
    context object name.
    context_object_name = "bloodpressure_list"

    This attribute `paginate_by = 10` will be implemented in the future.
    paginate_by = 10
    """

    def get_context_data(self, **kwargs):
        """
        Override the `get_context_data` method to add
        `user_averages_and_medians`.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Get the average and median of the current user's blood pressure
        # measurements.
        user_blood_pressure_averages_and_medians = (
            user.get_average_and_median_blood_pressure()
        )
        user_blood_pressure_range = user.get_blood_pressure_range()
        if user_blood_pressure_averages_and_medians is None:
            context["user_averages_and_medians"] = {
                "systolic_average": None,
                "diastolic_average": None,
                "systolic_median": None,
                "diastolic_median": None,
            }
        else:
            context[
                "user_averages_and_medians"
            ] = user_blood_pressure_averages_and_medians
            context["user_pressure_range"] = user_blood_pressure_range
        return context

    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Blood Pressures",
    }

    def get_queryset(self):
        """
        Override the `get_queryset` method to return a `QuerySet` of
        `BloodPressure` objects for the current user.
        """
        return BloodPressure.objects.filter(
            user=self.request.user,
        ).order_by("-created")


# Check if user is logged in and then check if the user has
# "registration_accepted" set to "True".
# TODO: Check if the order of the mixins matters. Order does matter:
# It's best practice to use mixins from more general to more specific.
class BloodPressureCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    CreateView,
):
    """
    `CreateView` for a user to create a blood pressure measurement.
    """

    model = BloodPressure
    # Redirect to the list of blood pressure measurements after a successful
    # creation.
    success_url = "/vitals/bloodpressures/"
    # TODO: Understand why this test doesn't work as expected.
    # success_url = reverse("vitals:bloodpressures")
    # Template name is not needed since we are using Django,s default template
    # naming convention `bloodpressure_form.html`.

    fields = [
        "systolic",
        "diastolic",
        "pulse",
    ]

    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Create Blood Pressure",
    }

    def test_func(self):
        """
        Override the `test_func` method to check if the current user has
        `registration_accepted` `True`.
        """
        return self.request.user.registration_accepted

    def form_valid(self, form):
        """
        Override the `form_valid` method to add the current user to the
        `BloodPressure` object.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)
