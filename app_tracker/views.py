from typing import Any
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import render
from django.views.generic import ListView

from config.settings import THE_SITE_NAME
from app_tracker.models import OrganizationalConcept


def home(request):
    """
    View function for the home page of the `app_tracker` app.

    This function adds the `the_site_name` and `page_title` variables to
    the context dictionary, which are used in the base template to set
    the page title and the site name.

    Context variables:

        the_site_name (str): The name of the site.

            - This is set in the `THE_SITE_NAME` variable in
            `config/settings/common.py`.

        page_title (str): The title of the page.

            - This is set to "App Tracker Home" in this view function.
    """
    return render(
        request,
        "app_tracker/home.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "App Tracker Home",
        },
    )


class OrganizationalConceptListView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    ListView,
):
    """
    View function for the list of a user's `OrganizationalConcept`s.
    """

    model = OrganizationalConcept

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Adds the `the_site_name` and `page_title` variables to the context
        dictionary.

        These variables are used in the base template to set the page title
        and the site name.
        """
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        context["page_title"] = "Organizational Concepts"
        return context

    def test_func(self) -> bool:
        """
        Test whether user has `registration_accepted` set to True.
        """
        return self.request.user.registration_accepted
