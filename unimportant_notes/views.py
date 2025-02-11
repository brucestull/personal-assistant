from typing import Any

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, FormMixin, UpdateView

from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .forms import UnimportantNoteForm
from .models import NoteTag, UnimportantNote


class NoteTagDetailView(RegistrationAcceptedMixin, UserPassesTestMixin, DetailView):
    """
    A view that displays a detail of a note tag.
    """

    model = NoteTag
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Note Tag",
    }

    def test_func(self) -> bool:
        """
        Only the author of the note can view it.
        """
        note_tag = self.get_object()
        return self.request.user == note_tag.author


class NoteTagListView(RegistrationAcceptedMixin, ListView):
    """
    A view that displays a list of note tags.
    """

    model = NoteTag
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Note Tags",
    }

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(author=self.request.user)


# from django.shortcuts import redirect, render
# from django.contrib.auth.decorators import login_required


# @login_required
# def unimportant_notes(request):
#     if request.method == "POST":
#         form = UnimportantNoteForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the form with `commit=False` to add the `author` to the
#             # `UnimportantNote` instance.
#             unimportant_note = form.save(commit=False)
#             # Set the `author` of the `UnimportantNote` instance.
#             unimportant_note.author = request.user
#             # Save the `UnimportantNote` instance.
#             unimportant_note.save()
#             return redirect("unimportant_notes:note_list")
#     else:
#         form = UnimportantNoteForm()
#         object_list = UnimportantNote.objects.all().order_by("-id")
#     return render(
#         request,
#         "unimportant_notes/note_list.html",
#         {
#             "form": form,
#             "object_list": object_list,
#             "the_site_name": THE_SITE_NAME,
#             "page_title": "Notes",
#         },
#     )


class UnimportantNoteCreateView(RegistrationAcceptedMixin, CreateView):
    """
    A view that displays a form for creating a note.
    """

    model = UnimportantNote
    form_class = UnimportantNoteForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Create Note",
        "mode": "create",
    }
    success_url = reverse_lazy("unimportant_notes:note_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self) -> dict[str, Any]:
        """
        Return the keyword arguments for instantiating the form.
        """
        kwargs = super(UnimportantNoteCreateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user  # Add the user to the form kwargs.
        return kwargs


class UnimportantNoteDetailView(
    RegistrationAcceptedMixin, UserPassesTestMixin, DetailView
):
    """
    A view that displays a detail of a note.
    """

    model = UnimportantNote
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Note",
    }

    def test_func(self) -> bool:
        """
        Only the author of the note can view it.
        """
        note = self.get_object()
        return self.request.user == note.author


class UnimportantNoteUpdateView(
    RegistrationAcceptedMixin, UserPassesTestMixin, UpdateView
):
    """
    View for updating the `UnimportantNote`.
    """

    model = UnimportantNote
    form_class = UnimportantNoteForm
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "mode": "update",
    }

    def get_context_data(self, **kwargs):
        """
        Override the `get_context_data` method to add the `page_title`, the object
        title, to the context.
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Editing: {self.object.title}"
        return context

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
        "page_title": "Unimportant Notes",
    }

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(author=self.request.user)

    def get_form_kwargs(self) -> dict[str, Any]:
        """
        Return the keyword arguments for instantiating the form.
        """
        kwargs = super(UnimportantNoteListView, self).get_form_kwargs()
        kwargs["user"] = self.request.user  # Add the user to the form kwargs.
        return kwargs
