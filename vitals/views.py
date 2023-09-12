from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from config.settings.common import THE_SITE_NAME
from vitals.models import (
    BloodPressure,
)


BLOOD_PRESSURE_LIST_PAGE_TITLE = "Blood Pressures"


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

    # TODO: Remove this?
    # Get the average and median of all the blood pressure measurements.
    average_and_median_all = BloodPressure.get_average_and_median()

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
        "page_title": BLOOD_PRESSURE_LIST_PAGE_TITLE,
        "average_and_median_all": average_and_median_all,
    }

    def get_queryset(self):
        """
        Override the `get_queryset` method to return a `QuerySet` of
        `BloodPressure` objects for the current user.
        """
        return BloodPressure.objects.filter(
            user=self.request.user,
        ).order_by("-created")
