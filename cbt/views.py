from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormMixin

from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .forms import ThoughtForm
from .models import CognitiveDistortion, Thought


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
            "page_title": "Cognitive Behavioral Therapy",
        },
    )


class CognitiveDistortionListView(RegistrationAcceptedMixin, ListView):
    """
    `ListView` for the `CognitiveDistortion` model.
    """

    model = CognitiveDistortion
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Cognitive Distortions",
    }


class ThoughtListView(RegistrationAcceptedMixin, FormMixin, ListView):
    """
    `ListView` for the `Thought` model.
    """

    model = Thought
    form_class = ThoughtForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Thoughts",
    }

    def get_queryset(self):
        """
        Override the `get_queryset` method to filter the `Thought` objects
        returned to only those belonging to the current user.
        """
        # Get the `Thought` objects belonging to the current user.
        queryset = Thought.objects.filter(user=self.request.user)
        # Return the `queryset`.
        return queryset


class ThoughtCreateView(RegistrationAcceptedMixin, CreateView):
    """
    `CreateView` for the `Thought` model.
    """

    model = Thought
    form_class = ThoughtForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Create a Thought",
    }
    success_url = reverse_lazy("cbt:thought-list")

    def get(self, request, *args, **kwargs):
        """
        Override the `get` method to add the `cognitive_distortion` field to the form's
        `initial` data.
        """
        # If there is a `cognitive_distortion_id` in the URL kwargs...
        if "cognitive_distortion_id" in kwargs:
            # Get the `CognitiveDistortion` object.
            cognitive_distortion = CognitiveDistortion.objects.get(
                pk=kwargs["cognitive_distortion_id"]
            )
            # Add the `cognitive_distortion` field to the form's `initial` data.
            self.initial["cognitive_distortion"] = cognitive_distortion
        # Return the `super` call.
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Override the `form_valid` method to add the current user to the form's
        `user` field.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class ThoughtDetailView(RegistrationAcceptedMixin, UserPassesTestMixin, DetailView):
    """
    `DetailView` for the `Thought` model.
    """

    model = Thought
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Thought",
    }

    def test_func(self):
        """
        Override the `test_func` method to ensure that the user is the owner of
        the `Thought` object.
        """
        # Get the `Thought` object.
        thought = self.get_object()
        # Return whether the user is the owner of the `Thought` object.
        return self.request.user == thought.user
