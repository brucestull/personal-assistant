# from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from base.mixins import RegistrationAcceptedMixin

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
    # template_name = "activity_tracker/activity_list.html"
    # context_object_name = "activities"


class ActivityDetailView(RegistrationAcceptedMixin, DetailView):
    """
    View function for the `ActivityDetailView` view.
    """

    model = Activity
    # template_name = "activity_tracker/activity_detail.html"
    # context_object_name = "activity"


@login_required
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
