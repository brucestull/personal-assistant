from typing import Any

from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormMixin

from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .forms import NoteForm
from .models import UnimportantNote


class NoteCreateView(RegistrationAcceptedMixin, CreateView):
    """
    A view that displays a form for creating a note.
    """

    model = UnimportantNote
    form_class = NoteForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Create Note",
    }
    success_url = reverse_lazy("unimportant_notes:note_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteListView(RegistrationAcceptedMixin, FormMixin, ListView):
    """
    A view that displays a list of notes.
    """

    model = UnimportantNote
    form_class = NoteForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Notes",
    }

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(author=self.request.user)
