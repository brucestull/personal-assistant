from typing import Any

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormMixin, UpdateView

from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .forms import UnimportantNoteForm
from .models import UnimportantNote


class UnimportantNoteCreateView(RegistrationAcceptedMixin, CreateView):
    """
    A view that displays a form for creating a note.
    """

    model = UnimportantNote
    form_class = UnimportantNoteForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Create Note",
    }
    success_url = reverse_lazy("unimportant_notes:note_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UnimportantNoteUpdateView(
    RegistrationAcceptedMixin, UserPassesTestMixin, UpdateView
):
    """
    View for updating the `UnimportantNote`.
    """

    model = UnimportantNote
    form_class = UnimportantNoteForm
    success_url = reverse_lazy("unimportant_notes:note_list")

    def test_func(self) -> bool:
        """
        Only the author of the note can update it.
        """
        note = self.get_object()
        return self.request.user == note.author


class UnimportantNoteListView(RegistrationAcceptedMixin, FormMixin, ListView):
    """
    A view that displays a list of notes.
    """

    model = UnimportantNote
    form_class = UnimportantNoteForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Notes",
    }

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(author=self.request.user)
