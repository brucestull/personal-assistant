from django.shortcuts import render

from config.settings.common import THE_SITE_NAME


def home(request):
    """
    View function for the home page of the `app_tracker` app.
    """
    return render(
        request,
        "app_tracker/home.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "App Tracker Home",
        },
    )
