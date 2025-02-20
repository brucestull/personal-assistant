from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .forms import AudioFileForm
from .models import AudioFile


class AudioFileListView(RegistrationAcceptedMixin, ListView):
    model = AudioFile
    extra_context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "Audio Files",
    }

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AudioFileDetailView(RegistrationAcceptedMixin, UserPassesTestMixin, DetailView):
    model = AudioFile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        context["page_title"] = f"Audio: {self.object.pk} - {self.object.name}"
        return context

    def test_func(self):
        """
        Only the user of the audio file can view it.
        """
        audio_file = self.get_object()
        return self.request.user == audio_file.user


class AudioFileCreateView(RegistrationAcceptedMixin, CreateView):
    model = AudioFile
    form_class = AudioFileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        context["page_title"] = "Create Audio File"
        return context

    def get_success_url(self):
        return reverse("sonic_text:audiofile_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AudioFileUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = AudioFile
    form_class = AudioFileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        context["page_title"] = (
            f"Update Audio File: {self.object.pk} - {self.object.name}"
        )
        return context

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AudioFileDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = AudioFile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        context["page_title"] = (
            f"Delete Audio File: {self.object.pk} - {self.object.name}"
        )
        return context

    success_url = reverse_lazy("sonic_text:audiofile_list")
