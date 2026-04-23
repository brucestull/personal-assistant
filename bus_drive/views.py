from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from base.mixins import RegistrationAcceptedMixin, SiteContextMixin

from .forms import ThoughtForm
from .models import Thought


class DashboardView(SiteContextMixin, RegistrationAcceptedMixin, TemplateView):
    template_name = "bus_drive/dashboard.html"
    page_title = "Bus Drive"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_thoughts = Thought.objects.filter(user=self.request.user)
        context["total_thoughts"] = user_thoughts.count()
        context["recent_thoughts"] = user_thoughts[:5]
        return context


class SPAView(SiteContextMixin, RegistrationAcceptedMixin, TemplateView):
    template_name = "bus_drive/spa.html"
    page_title = "Bus Drive React App"


class ThoughtListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = Thought
    template_name = "bus_drive/thought_list.html"
    page_title = "Bus Drive Thoughts"
    paginate_by = 20

    def get_queryset(self):
        return Thought.objects.filter(user=self.request.user)


class ThoughtDetailView(SiteContextMixin, RegistrationAcceptedMixin, DetailView):
    model = Thought
    template_name = "bus_drive/thought_detail.html"
    page_title = "Thought Detail"

    def get_queryset(self):
        return Thought.objects.filter(user=self.request.user)


class ThoughtCreateView(SiteContextMixin, RegistrationAcceptedMixin, CreateView):
    model = Thought
    form_class = ThoughtForm
    template_name = "bus_drive/thought_form.html"
    success_url = reverse_lazy("bus_drive:thought-list")
    page_title = "Add Thought"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Thought saved.")
        return super().form_valid(form)


class ThoughtUpdateView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, UpdateView
):
    model = Thought
    form_class = ThoughtForm
    template_name = "bus_drive/thought_form.html"
    success_url = reverse_lazy("bus_drive:thought-list")
    page_title = "Edit Thought"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Thought updated.")
        return super().form_valid(form)


class ThoughtDeleteView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, DeleteView
):
    model = Thought
    template_name = "bus_drive/thought_confirm_delete.html"
    success_url = reverse_lazy("bus_drive:thought-list")
    page_title = "Delete Thought"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Thought deleted.")
        return super().form_valid(form)
