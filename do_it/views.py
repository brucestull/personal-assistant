# do_it/views.py

from base.mixins import RegistrationAcceptedMixin

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# REST imports
from rest_framework import viewsets, permissions

from .models import Tag, Cycle, Task

# from .models import TaskCompleted

from .serializers import (
    TagSerializer,
    CycleSerializer,
    TaskSerializer,
    # TaskCompletedSerializer,
)


# --- Vanilla Django CRUD Views for Tag ---


class TagListView(RegistrationAcceptedMixin, generic.ListView):
    model = Tag
    template_name = "do_it/tag_list.html"
    context_object_name = "tags"

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class TagDetailView(RegistrationAcceptedMixin, generic.DetailView):
    model = Tag
    template_name = "do_it/tag_detail.html"
    context_object_name = "tag"

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class TagCreateView(RegistrationAcceptedMixin, generic.CreateView):
    model = Tag
    fields = ["name", "description"]
    template_name = "do_it/tag_form.html"
    success_url = reverse_lazy("do_it:tag_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TagUpdateView(RegistrationAcceptedMixin, generic.UpdateView):
    model = Tag
    fields = ["name", "description"]
    template_name = "do_it/tag_form.html"
    success_url = reverse_lazy("do_it:tag_list")

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    template_name = "do_it/tag_confirm_delete.html"
    success_url = reverse_lazy("do_it:tag_list")

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


# --- Vanilla Django CRUD Views for Cycle ---
class CycleListView(RegistrationAcceptedMixin, generic.ListView):
    model = Cycle
    template_name = "do_it/cycle_list.html"
    context_object_name = "cycles"

    def get_queryset(self):
        return Cycle.objects.filter(user=self.request.user)


class CycleDetailView(RegistrationAcceptedMixin, generic.DetailView):
    model = Cycle
    template_name = "do_it/cycle_detail.html"
    context_object_name = "cycle"

    def get_queryset(self):
        return Cycle.objects.filter(user=self.request.user)


class CycleCreateView(RegistrationAcceptedMixin, generic.CreateView):
    model = Cycle
    fields = ["name", "periodicity"]
    template_name = "do_it/cycle_form.html"
    success_url = reverse_lazy("do_it:cycle_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CycleUpdateView(RegistrationAcceptedMixin, generic.UpdateView):
    model = Cycle
    fields = ["name", "periodicity"]
    template_name = "do_it/cycle_form.html"
    success_url = reverse_lazy("do_it:cycle_list")

    def get_queryset(self):
        return Cycle.objects.filter(user=self.request.user)


class CycleDeleteView(RegistrationAcceptedMixin, generic.DeleteView):
    model = Cycle
    template_name = "do_it/cycle_confirm_delete.html"
    success_url = reverse_lazy("do_it:cycle_list")

    def get_queryset(self):
        return Cycle.objects.filter(user=self.request.user)


# --- Vanilla Django CRUD Views for Task ---


class TaskListView(RegistrationAcceptedMixin, generic.ListView):
    model = Task
    template_name = "do_it/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDetailView(RegistrationAcceptedMixin, generic.DetailView):
    model = Task
    template_name = "do_it/task_detail.html"
    context_object_name = "task"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(RegistrationAcceptedMixin, generic.CreateView):
    model = Task
    fields = ["name", "description", "tag", "cycle", "is_recurrent"]
    template_name = "do_it/task_form.html"
    success_url = reverse_lazy("do_it:task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(RegistrationAcceptedMixin, generic.UpdateView):
    model = Task
    fields = ["name", "description", "tag", "cycle", "is_recurrent"]
    template_name = "do_it/task_form.html"
    success_url = reverse_lazy("do_it:task_list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDeleteView(RegistrationAcceptedMixin, generic.DeleteView):
    model = Task
    template_name = "do_it/task_confirm_delete.html"
    success_url = reverse_lazy("do_it:task_list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


# --- Vanilla Django CRUD Views for TaskCompleted ---


# class TaskCompletedListView(RegistrationAcceptedMixin, generic.ListView):
#     model = TaskCompleted
#     template_name = "do_it/task_completed_list.html"
#     context_object_name = "task_completed_list"

#     def get_queryset(self):
#         return TaskCompleted.objects.filter(user=self.request.user)


# class TaskCompletedDetailView(RegistrationAcceptedMixin, generic.DetailView):
#     model = TaskCompleted
#     template_name = "do_it/task_completed_detail.html"
#     context_object_name = "task_completed"

#     def get_queryset(self):
#         return TaskCompleted.objects.filter(user=self.request.user)


# class TaskCompletedCreateView(RegistrationAcceptedMixin, generic.CreateView):
#     model = TaskCompleted
#     fields = ["task_repr", "date_scheduled"]
#     template_name = "do_it/task_completed_form.html"
#     success_url = reverse_lazy("do_it:task_completed_list")

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


# class TaskCompletedUpdateView(RegistrationAcceptedMixin, generic.UpdateView):
#     model = TaskCompleted
#     fields = ["task_repr", "date_scheduled"]
#     template_name = "do_it/task_completed_form.html"
#     success_url = reverse_lazy("do_it:task_completed_list")

#     def get_queryset(self):
#         return TaskCompleted.objects.filter(user=self.request.user)


# class TaskCompletedDeleteView(RegistrationAcceptedMixin, generic.DeleteView):
#     model = TaskCompleted
#     template_name = "do_it/task_completed_confirm_delete.html"
#     success_url = reverse_lazy("do_it:task_completed_list")

#     def get_queryset(self):
#         return TaskCompleted.objects.filter(user=self.request.user)


# --- REST Framework ViewSets (browsable API) ---


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that lets you list, create, retrieve, update & delete Tags.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CycleViewSet(viewsets.ModelViewSet):
    serializer_class = CycleSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cycle.objects.all()

    def get_queryset(self):
        return Cycle.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class TaskCompletedViewSet(viewsets.ModelViewSet):
#     serializer_class = TaskCompletedSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return TaskCompleted.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         # date_completed is auto-set; user is set here
#         serializer.save(user=self.request.user)
