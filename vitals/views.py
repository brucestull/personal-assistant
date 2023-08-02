from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from config.settings.common import THE_SITE_NAME
from vitals.models import BloodPressure


BLOOD_PRESSURE_LIST_PAGE_TITLE = "Blood Pressures"


def home(request):
    """
    View function for the home page of the site.
    """
    return render(
        request,
        "vitals/home.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "Vitals Home",
        },
    )


class BloodPressureListView(ListView):
    model = BloodPressure
    template_name = "vitals/bloodpressure_list.html"
    context_object_name = "bloodpressure_list"
    paginate_by = 10
    average_and_median = BloodPressure.get_average_and_median()
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": BLOOD_PRESSURE_LIST_PAGE_TITLE,
        "average_and_median": average_and_median,
    }

    def get_queryset(self):
        return BloodPressure.objects.filter(user=self.request.user).order_by("-created")
