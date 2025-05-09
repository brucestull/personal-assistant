# from django.views.generic.edit import CreateView
from typing import Any

from django.contrib import messages
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from base.mixins import RegistrationAcceptedMixin
from base.decorators import registration_accepted_required
from config.settings import THE_SITE_NAME

from .models import Activity, ActivityCompleted  # ActivityType,


def json_response(request):
    """
    View function for the `json_response` view.
    """
    return JsonResponse(
        {
            "message": "Goodbuy, World! Enjoy the sails and bar guns!",
            "status": 200,
        }
    )


class ActivityListView(RegistrationAcceptedMixin, ListView):
    """
    View function for the `ActivityListView` view.
    """

    model = Activity
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Activities",
    }

    # template_name = "activity_tracker/activity_list.html"
    # context_object_name = "activities"
    def get_queryset(self) -> QuerySet[Any]:
        return Activity.objects.filter(user=self.request.user)


class ActivityDetailView(RegistrationAcceptedMixin, DetailView):
    """
    View function for the `ActivityDetailView` view.
    """

    model = Activity
    extra_context = {
        "the_site_name": THE_SITE_NAME,
    }

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.object.name
        return context

    # template_name = "activity_tracker/activity_detail.html"
    # context_object_name = "activity"
    # Override the `get_object` method to filter by the user
    def get_object(self, queryset=None) -> Model:
        return Activity.objects.get(pk=self.kwargs.get("pk"), user=self.request.user)


@registration_accepted_required
def complete_an_activity_view(request, pk):
    """
    View function for the `activity_complete_view` view.
    """
    # Send a message that the `get` method returns user to the activity list
    if request.method == "GET":
        messages.success(request, "`GET` requests redirect to the activity list.")
        return redirect(reverse_lazy("activity_tracker:activity-list"))
    elif request.method == "POST":
        # `post` method is used to complete the activity
        activity = Activity.objects.get(pk=pk)
        user = request.user
        completed_activity = ActivityCompleted.objects.create(
            activity=activity, user=user
        )
        messages.success(
            request,
            f"Activity `{completed_activity.activity.name}` "
            f"completed by {user.username}.",
        )
        return redirect(reverse_lazy("activity_tracker:activity-list"))
    else:
        return redirect(reverse_lazy("activity_tracker:activity-list"))
