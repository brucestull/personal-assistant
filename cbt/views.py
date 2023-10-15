from django.shortcuts import render

from config.settings import THE_SITE_NAME

HOME_PAGE_TITLE = "Cognative Behavioral Therapy"


def home(request):
    """
    View function for the home page of the `cbt` app.
    """
    return render(
        request,
        "cbt/home.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": HOME_PAGE_TITLE,
        },
    )
