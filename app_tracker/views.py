from typing import Any
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import render

from config.settings.common import THE_SITE_NAME

HOME_PAGE_TITLE = "App Tracker Home"


def home(request):
    """
    View function for the home page of the `app_tracker` app.
    """
    return render(
        request,
        "app_tracker/home.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": HOME_PAGE_TITLE,
        },
    )
