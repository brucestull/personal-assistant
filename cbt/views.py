from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .forms import CognativeDistortionForm
from .models import CognativeDistortion


def home(request):
    """
    View function for the home page of the `cbt` app.
    """
    return render(
        # Need to return the `request` object so data is preserved.
        request,
        # Need to specify the template directory, this is name-spaced using the
        # directory name.
        "cbt/home.html",
        # Pass in the necessary context data.
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "Cognative Behavioral Therapy",
        },
    )


class CognitiveDistortionListView(RegistrationAcceptedMixin, ListView):
    """
    `ListView` for the `CognativeDistortion` model.
    """

    model = CognativeDistortion
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Cognitive Distortions",
    }
