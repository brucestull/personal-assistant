from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView

from base.mixins import RegistrationAcceptedMixin

from .models import PersonalValue


class PersonalValueCreateView(RegistrationAcceptedMixin, CreateView):
    """Create view for PersonalValue model."""

    model = PersonalValue
    fields = ["name", "description"]

    def form_valid(self, form):
        """Set form instance user to current user."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Return URL to redirect to after processing form."""
        return reverse("value_centric:personal-value-list")


class PersonalValueDetailView(RegistrationAcceptedMixin, DetailView):
    """Detail view for PersonalValue model."""

    model = PersonalValue


class PersonalValueUpdateView(RegistrationAcceptedMixin, UpdateView):
    """Update view for PersonalValue model."""

    model = PersonalValue
    fields = ["name", "description"]


class PersonalValueDeleteView(RegistrationAcceptedMixin, DeleteView):
    """Delete view for PersonalValue model."""

    model = PersonalValue

    def get_success_url(self):
        """Return URL to redirect to after processing form."""
        return reverse("value_centric:personal-value-list")


class PersonalValueListView(RegistrationAcceptedMixin, ListView):
    """List view for PersonalValue model."""

    model = PersonalValue

    def get_queryset(self):
        """Return queryset of PersonalValue objects for current user."""
        return PersonalValue.objects.filter(user=self.request.user)
