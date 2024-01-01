from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView

from .models import PersonalValue


class PersonalValueCreateView(CreateView):
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


class PersonalValueDetailView(DetailView):
    """Detail view for PersonalValue model."""

    model = PersonalValue


class PersonalValueUpdateView(UpdateView):
    """Update view for PersonalValue model."""

    model = PersonalValue
    fields = ["name", "description"]


class PersonalValueDeleteView(DeleteView):
    """Delete view for PersonalValue model."""

    model = PersonalValue

    def get_success_url(self):
        """Return URL to redirect to after processing form."""
        return reverse("value_centric:personal-value-list")


class PersonalValueListView(ListView):
    """List view for PersonalValue model."""

    model = PersonalValue
