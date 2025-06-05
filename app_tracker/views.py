# app_tracker/views.py

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from app_tracker.models import (
    Application,
    Label,
    LanguageFrameworkSystem,
    Note,
    OperatingSystem,
    OrganizationalConcept,
    Project,
    Server,
)
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME


def home(request):
    """
    View function for the home page of the `app_tracker` app.

    This function adds the `the_site_name` and `page_title` variables to
    the context dictionary, which are used in the base template to set
    the page title and the site name.

    Context variables:

        the_site_name (str): The name of the site.

            - This is set in the `THE_SITE_NAME` variable in
            `config/settings/common.py`.

        page_title (str): The title of the page.

            - This is set to "App Tracker Home" in this view function.
    """
    return render(
        request,
        "app_tracker/home.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "App Tracker Home",
        },
    )


# Application views
class ApplicationListView(RegistrationAcceptedMixin, ListView):
    model = Application


class ApplicationDetailView(RegistrationAcceptedMixin, DetailView):
    model = Application


class ApplicationCreateView(RegistrationAcceptedMixin, CreateView):
    model = Application
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:application_list")


class ApplicationUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Application
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:application_list")


class ApplicationDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Application
    success_url = reverse_lazy("app_tracker:application_list")


# Label views
class LabelListView(RegistrationAcceptedMixin, ListView):
    model = Label


class LabelDetailView(RegistrationAcceptedMixin, DetailView):
    model = Label


class LabelCreateView(RegistrationAcceptedMixin, CreateView):
    model = Label
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:label_list")


class LabelUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Label
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:label_list")


class LabelDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Label
    success_url = reverse_lazy("app_tracker:label_list")


# LanguageFrameworkSystem views
class LanguageFrameworkSystemListView(RegistrationAcceptedMixin, ListView):
    model = LanguageFrameworkSystem


class LanguageFrameworkSystemDetailView(RegistrationAcceptedMixin, DetailView):
    model = LanguageFrameworkSystem


class LanguageFrameworkSystemCreateView(RegistrationAcceptedMixin, CreateView):
    model = LanguageFrameworkSystem
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:lfs_list")


class LanguageFrameworkSystemUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = LanguageFrameworkSystem
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:lfs_list")


class LanguageFrameworkSystemDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = LanguageFrameworkSystem
    success_url = reverse_lazy("app_tracker:lfs_list")


# Note views
class NoteListView(RegistrationAcceptedMixin, ListView):
    model = Note


class NoteDetailView(RegistrationAcceptedMixin, DetailView):
    model = Note


class NoteCreateView(RegistrationAcceptedMixin, CreateView):
    model = Note
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:note_list")


class NoteUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Note
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:note_list")


class NoteDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Note
    success_url = reverse_lazy("app_tracker:note_list")


# OperatingSystem views
class OperatingSystemListView(RegistrationAcceptedMixin, ListView):
    model = OperatingSystem


class OperatingSystemDetailView(RegistrationAcceptedMixin, DetailView):
    model = OperatingSystem


class OperatingSystemCreateView(RegistrationAcceptedMixin, CreateView):
    model = OperatingSystem
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:os_list")


class OperatingSystemUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = OperatingSystem
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:os_list")


class OperatingSystemDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = OperatingSystem
    success_url = reverse_lazy("app_tracker:os_list")


# OrganizationalConcept views
class OrganizationalConceptListView(RegistrationAcceptedMixin, ListView):
    model = OrganizationalConcept


class OrganizationalConceptDetailView(RegistrationAcceptedMixin, DetailView):
    model = OrganizationalConcept


class OrganizationalConceptCreateView(RegistrationAcceptedMixin, CreateView):
    model = OrganizationalConcept
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:oc_list")


class OrganizationalConceptUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = OrganizationalConcept
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:oc_list")


class OrganizationalConceptDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = OrganizationalConcept
    success_url = reverse_lazy("app_tracker:oc_list")


# Project views
class ProjectListView(RegistrationAcceptedMixin, ListView):
    model = Project


class ProjectDetailView(RegistrationAcceptedMixin, DetailView):
    model = Project


class ProjectCreateView(RegistrationAcceptedMixin, CreateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:project_list")


class ProjectUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:project_list")


class ProjectDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("app_tracker:project_list")


# Server views
class ServerListView(RegistrationAcceptedMixin, ListView):
    model = Server


class ServerDetailView(RegistrationAcceptedMixin, DetailView):
    model = Server


class ServerCreateView(RegistrationAcceptedMixin, CreateView):
    model = Server
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:server_list")


class ServerUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Server
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:server_list")


class ServerDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Server
    success_url = reverse_lazy("app_tracker:server_list")
