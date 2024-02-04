from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
# from django.views.generic.edit import CreateView

from .models import (
    Activity,
    ActivityCompleted,
    # ActivityType,
    )


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


class ActivityListView(ListView):
    """
    View function for the `ActivityListView` view.
    """

    model = Activity
    # template_name = "activity_tracker/activity_list.html"
    # context_object_name = "activities"


class ActivityDetailView(DetailView):
    """
    View function for the `ActivityDetailView` view.
    """

    model = Activity
    # template_name = "activity_tracker/activity_detail.html"
    # context_object_name = "activity"


def complete_an_activity_view(request, pk):
    """
    View function for the `activity_complete_view` view.
    """
    # Send a message that the `get` method returns user to the activity list
    if request.method == "GET":
        return redirect(reverse_lazy("activity_tracker:activity-list"))
    elif request.method == "POST":
        # `post` method is used to complete the activity
        activity = Activity.objects.get(pk=pk)
        user = request.user
        activity_completed = ActivityCompleted.objects.create(activity=activity, user=user) # noqa F481
        return redirect(reverse_lazy("activity_tracker:activity-list"))
    else:
        return redirect(reverse_lazy("activity_tracker:activity-list"))
