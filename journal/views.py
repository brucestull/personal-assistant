from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from base.mixins import RegistrationAcceptedMixin

# from config.settings import THE_SITE_NAME

from .models import Entry


class EntryCreateView(RegistrationAcceptedMixin, SuccessMessageMixin, CreateView):
    model = Entry
    fields = ["title", "content"]
    success_message = "Your new entry was created!"

    def form_valid(self, form):
        """
        Override the default form_valid method to add the author to the form.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class EntryDetailView(RegistrationAcceptedMixin, DetailView):
    model = Entry

    def get_queryset(self):
        """
        Override the default queryset to only show entries created by the user.
        """
        return Entry.objects.filter(author=self.request.user)


class EntryUpdateView(RegistrationAcceptedMixin, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["title", "content"]
    success_message = "Your entry was updated!"

    def get_queryset(self):
        """
        Override the default queryset to only show entries created by the user.
        """
        return Entry.objects.filter(author=self.request.user)

    # def get_success_url(self):
    #     return reverse_lazy("journal:entry_detail", kwargs={"pk": self.object.pk})


class EntryDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("journal:entry_list")
    success_message = "Your entry was deleted!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        """
        Override the default queryset to only show entries created by the user.
        """
        return Entry.objects.filter(author=self.request.user)


class EntryListView(RegistrationAcceptedMixin, ListView):
    model = Entry

    def get_queryset(self):
        """
        Override the default queryset to only show entries created by the user.
        """
        return Entry.objects.filter(author=self.request.user).order_by("-date_created")
