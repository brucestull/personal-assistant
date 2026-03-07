# ideas/views.py

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .forms import IdeaForm
from .models import Idea


class IdeaListView(RegistrationAcceptedMixin, ListView):
    """
    A view that displays a list of ideas for the authenticated user.
    """

    model = Idea
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Ideas",
    }

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(author=self.request.user)


class IdeaDetailView(RegistrationAcceptedMixin, UserPassesTestMixin, DetailView):
    """
    A view that displays the detail of an idea.
    """

    model = Idea
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Idea",
    }

    def test_func(self) -> bool:
        """
        Only the author of the idea can view it.
        """
        idea = self.get_object()
        return self.request.user == idea.author


class IdeaCreateView(RegistrationAcceptedMixin, CreateView):
    """
    A view that displays a form for creating an idea.
    """

    model = Idea
    form_class = IdeaForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Create Idea",
        "mode": "create",
    }
    success_url = reverse_lazy("ideas:idea_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class IdeaUpdateView(RegistrationAcceptedMixin, UserPassesTestMixin, UpdateView):
    """
    A view that displays a form for updating an idea.
    """

    model = Idea
    form_class = IdeaForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "mode": "update",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Editing: {self.object.name}"
        return context

    def test_func(self) -> bool:
        """
        Only the author of the idea can update it.
        """
        idea = self.get_object()
        return self.request.user == idea.author


class IdeaDeleteView(RegistrationAcceptedMixin, UserPassesTestMixin, DeleteView):
    """
    A view that displays a confirmation page for deleting an idea.
    """

    model = Idea
    success_url = reverse_lazy("ideas:idea_list")

    def test_func(self) -> bool:
        """
        Only the author of the idea can delete it.
        """
        idea = self.get_object()
        return self.request.user == idea.author
