from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .forms import NoteForm
from .models import Note


class NoteListView(FormMixin, ListView):
    """
    A view that displays a list of notes.
    """

    model = Note

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(author=self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = NoteForm()
        return context

    def post(self, request, *args, **kwargs):
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("note_list")  # Redirect to the item list view

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # paginate_by = 10
