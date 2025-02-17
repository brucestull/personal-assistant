from django.views.generic import DetailView, ListView

from base.mixins import RegistrationAcceptedMixin

# from config.settings import THE_SITE_NAME

from .models import Entry


class EntryListView(RegistrationAcceptedMixin, ListView):
    model = Entry

    def get_queryset(self):
        """
        Override the default queryset to only show entries created by the user.
        """
        return Entry.objects.filter(author=self.request.user).order_by("-date_created")


class EntryDetailView(RegistrationAcceptedMixin, DetailView):
    model = Entry

    def get_queryset(self):
        """
        Override the default queryset to only show entries created by the user.
        """
        return Entry.objects.filter(author=self.request.user)
