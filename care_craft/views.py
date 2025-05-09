from django.shortcuts import get_object_or_404, redirect, render

from base.decorators import registration_accepted_required

from .forms import ActivityForm
from .models import Activity


@registration_accepted_required
def activity_list(request):
    activities = Activity.objects.all()
    return render(request, "care_craft/activity_list.html", {"activities": activities})


@registration_accepted_required
def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    return render(request, "care_craft/activity_detail.html", {"activity": activity})


@registration_accepted_required
def activity_create(request):
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("activity_list")
    else:
        form = ActivityForm()
    return render(request, "care_craft/activity_form.html", {"form": form})


@registration_accepted_required
def activity_update(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("activity_detail", pk=pk)
    else:
        form = ActivityForm(instance=activity)
    return render(request, "care_craft/activity_form.html", {"form": form})


@registration_accepted_required
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        activity.delete()
        return redirect("activity_list")
    return render(
        request, "care_craft/activity_confirm_delete.html", {"activity": activity}
    )
