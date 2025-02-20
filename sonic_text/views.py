from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from base.mixins import RegistrationAcceptedMixin

from .forms import AudioFileForm
from .models import AudioFile


class AudioFileListView(RegistrationAcceptedMixin, ListView):
    model = AudioFile

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AudioFileDetailView(RegistrationAcceptedMixin, UserPassesTestMixin, DetailView):
    model = AudioFile

    def test_func(self):
        """
        Only the user of the audio file can view it.
        """
        audio_file = self.get_object()
        return self.request.user == audio_file.user


class AudioFileCreateView(RegistrationAcceptedMixin, CreateView):
    model = AudioFile
    form_class = AudioFileForm

    def get_success_url(self):
        return reverse("sonic_text:audiofile_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user


class AudioFileUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = AudioFile
    form_class = AudioFileForm

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class AudioFileDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = AudioFile

    success_url = reverse_lazy("sonic_text:audiofile_list")
