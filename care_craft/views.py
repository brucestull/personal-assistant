# care_craft/views.py

from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin

from .forms import ActivityForm
from .models import Activity, CareCraftNote

# CoPilot response to import RegistrationAcceptedMixin
# Import RegistrationAcceptedMixin if it exists in base.mixins
# try:
#     from base.mixins import RegistrationAcceptedMixin
# except ImportError:
#     # Define a dummy mixin if not available (remove this if you add the real mixin)
#     from django.contrib.auth.mixins import LoginRequiredMixin

#     class RegistrationAcceptedMixin(LoginRequiredMixin):
#         pass


class CareCraftNoteListView(RegistrationAcceptedMixin, ListView):
    model = CareCraftNote

    def get_queryset(self) -> QuerySet[Any]:
        """
        Override the default queryset to filter notes by the current user.
        """
        return super().get_queryset().filter(user=self.request.user)


class CareCraftNoteDetailView(RegistrationAcceptedMixin, DetailView):
    model = CareCraftNote


class CareCraftNoteCreateView(RegistrationAcceptedMixin, CreateView):
    model = CareCraftNote
    fields = ["title", "content", "url", "main_image"]

    def form_valid(self, form):
        """
        Override form_valid to set the user to the current request user.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class CareCraftNoteUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = CareCraftNote
    fields = ["title", "content", "url", "main_image"]


class CareCraftNoteDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = CareCraftNote
    success_url = reverse_lazy("care_craft:note_list")


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
            return redirect("care_craft:activity_list")
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
            return redirect("care_craft:activity_detail", pk=pk)
    else:
        form = ActivityForm(instance=activity)
    return render(request, "care_craft/activity_form.html", {"form": form})


@registration_accepted_required
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        activity.delete()
        return redirect("care_craft:activity_list")
    return render(
        request, "care_craft/activity_confirm_delete.html", {"activity": activity}
    )
