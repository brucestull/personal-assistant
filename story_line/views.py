# story_line/views.py

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from base.mixins import RegistrationAcceptedMixin

from .models import StoryLineNote


class StoryLineNoteListView(RegistrationAcceptedMixin, ListView):
    model = StoryLineNote
    context_object_name = "notes"

    def get_queryset(self):
        return StoryLineNote.objects.filter(user=self.request.user)


class StoryLineNoteDetailView(RegistrationAcceptedMixin, DetailView):
    model = StoryLineNote


class StoryLineNoteCreateView(RegistrationAcceptedMixin, CreateView):
    model = StoryLineNote
    fields = ["title", "content", "url", "main_image"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class StoryLineNoteUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = StoryLineNote
    fields = ["title", "content", "url", "main_image"]

    def get_queryset(self):
        return StoryLineNote.objects.filter(user=self.request.user)


class StoryLineNoteDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = StoryLineNote
    success_url = reverse_lazy("story_line:note_list")

    def get_queryset(self):
        return StoryLineNote.objects.filter(user=self.request.user)
