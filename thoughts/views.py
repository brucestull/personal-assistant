# thoughts/views.py

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from base.mixins import RegistrationAcceptedMixin, SiteContextMixin

from .forms import ThoughtForm
from .models import Thought


class DashboardView(SiteContextMixin, RegistrationAcceptedMixin, TemplateView):
    template_name = "thoughts/dashboard.html"
    page_title = "Thoughts Dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_thoughts = Thought.objects.filter(user=self.request.user)
        context["total_thoughts"] = user_thoughts.count()
        context["recent_thoughts"] = user_thoughts.order_by("-created")[:5]
        return context


class ThoughtListView(SiteContextMixin, RegistrationAcceptedMixin, ListView):
    model = Thought
    template_name = "thoughts/thought_list.html"
    page_title = "My Thoughts"
    paginate_by = 20

    def get_queryset(self):
        return Thought.objects.filter(user=self.request.user)


class ThoughtCreateView(SiteContextMixin, RegistrationAcceptedMixin, CreateView):
    model = Thought
    form_class = ThoughtForm
    template_name = "thoughts/thought_form.html"
    success_url = reverse_lazy("thoughts:thought-list")
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
    template_name = "thoughts/thought_form.html"
    success_url = reverse_lazy("thoughts:thought-list")

    def get_page_title(self):
        return "Edit Thought"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Thought updated.")
        return super().form_valid(form)


class ThoughtDeleteView(
    SiteContextMixin, RegistrationAcceptedMixin, UserPassesTestMixin, DeleteView
):
    model = Thought
    template_name = "thoughts/thought_confirm_delete.html"
    success_url = reverse_lazy("thoughts:thought-list")
    page_title = "Delete Thought"

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Thought deleted.")
        return super().form_valid(form)
