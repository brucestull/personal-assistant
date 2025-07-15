# todo/views.py
"""Class-based views for the tasks app."""

from django.shortcuts import get_object_or_404, redirect
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

from .models import Priority, Tag, Task


# --- Tag CBVs ---
class TagListView(RegistrationAcceptedMixin, ListView):
    model = Tag


class TagDetailView(RegistrationAcceptedMixin, DetailView):
    model = Tag


class TagCreateView(RegistrationAcceptedMixin, CreateView):
    model = Tag
    fields = ["name", "description"]
    success_url = reverse_lazy("tasks:tag_list")

    def form_valid(self, form):
        """Assign the current user as the owner of the Tag."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class TagUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Tag
    fields = ["name", "description"]
    success_url = reverse_lazy("tasks:tag_list")


class TagDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy("tasks:tag_list")


# --- Priority CBVs ---
class PriorityListView(RegistrationAcceptedMixin, ListView):
    model = Priority


class PriorityDetailView(RegistrationAcceptedMixin, DetailView):
    model = Priority


class PriorityCreateView(RegistrationAcceptedMixin, CreateView):
    model = Priority
    fields = ["name", "level"]
    success_url = reverse_lazy("tasks:priority_list")

    def form_valid(self, form):
        """Assign the current user as the owner of the Priority."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class PriorityUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Priority
    fields = ["name", "level"]
    success_url = reverse_lazy("tasks:priority_list")


class PriorityDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Priority
    success_url = reverse_lazy("tasks:priority_list")


# --- Task CBVs ---
class TaskListView(RegistrationAcceptedMixin, ListView):
    model = Task


class TaskDetailView(RegistrationAcceptedMixin, DetailView):
    model = Task


class TaskCreateView(RegistrationAcceptedMixin, CreateView):
    model = Task
    fields = ["completed", "name", "information", "tag", "priority"]
    success_url = reverse_lazy("tasks:task_list")

    def form_valid(self, form):
        """Assign the current user as the owner of the Task."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Task
    fields = ["completed", "name", "information", "tag", "priority"]
    success_url = reverse_lazy("tasks:task_list")


class TaskDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task_list")


@registration_accepted_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = True
    task.save()
    return redirect("tasks:task_list")
