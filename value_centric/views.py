from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView

from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

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

    def get_context_data(self, **kwargs):
        """Add site name to context."""
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        context["page_title"] = "Create Personal Value"
        return context


class PersonalValueDetailView(RegistrationAcceptedMixin, DetailView):
    """Detail view for PersonalValue model."""

    model = PersonalValue

    def get_context_data(self, **kwargs):
        """Add site name to context."""
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        context["page_title"] = "Personal Value Detail"
        return context


class PersonalValueUpdateView(RegistrationAcceptedMixin, UpdateView):
    """Update view for PersonalValue model."""

    model = PersonalValue
    fields = ["name", "description"]

    def get_context_data(self, **kwargs):
        """Add site name to context."""
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        context["page_title"] = "Update Personal Value"
        return context


class PersonalValueDeleteView(RegistrationAcceptedMixin, DeleteView):
    """Delete view for PersonalValue model."""

    model = PersonalValue

    def get_success_url(self):
        """Return URL to redirect to after processing form."""
        return reverse("value_centric:personal-value-list")

    def get_context_data(self, **kwargs):
        """Add site name to context."""
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        context["page_title"] = "Delete Personal Value"
        return context


class PersonalValueListView(RegistrationAcceptedMixin, ListView):
    """List view for PersonalValue model."""

    model = PersonalValue

    def get_queryset(self):
        """Return queryset of PersonalValue objects for current user."""
        return PersonalValue.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add site name to context."""
        context = super().get_context_data(**kwargs)
        context["the_site_name"] = THE_SITE_NAME
        context["page_title"] = "Personal Values"
        return context
