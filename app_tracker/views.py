# app_tracker/views.py

from django.db.models import Count
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
    Host,
    URL,
)
from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME


@registration_accepted_required
def dashboard(request):
    """
    Dashboard view for the app_tracker app providing useful statistics
    and overviews of tracked applications.
    """
    # Get all applications
    all_applications = Application.objects.all()

    # Basic counts
    total_applications = all_applications.count()
    total_projects = Project.objects.count()
    total_hosts = Host.objects.count()
    total_lfs = LanguageFrameworkSystem.objects.count()

    # Applications with specific features
    apps_with_production = all_applications.filter(has_prod_deployment=True).count()
    apps_with_cicd = all_applications.filter(has_cicd=True).count()
    apps_with_custom_user = all_applications.filter(has_custom_user=True).count()
    apps_public_repo = all_applications.filter(repository_is_public=True).count()
    apps_all_tests_passing = all_applications.filter(all_tests_passing=True).count()

    # Favorite applications
    favorite_apps = all_applications.filter(is_favorite=True)[:10]

    # Recent applications (by created date)
    recent_apps = all_applications.order_by("-created")[:5]

    # Applications by testing level
    testing_level_counts = (
        all_applications.exclude(testing_level__isnull=True)
        .exclude(testing_level="")
        .values("testing_level")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Language/Framework/System usage with application counts
    lfs_usage = LanguageFrameworkSystem.objects.annotate(
        app_count=Count("applications")
    ).order_by("-app_count")[:10]

    # Projects with their application counts
    projects_overview = Project.objects.annotate(
        app_count=Count("applications")
    ).order_by("-app_count")[:10]

    # Hosts by environment
    hosts_by_environment = (
        Host.objects.exclude(environment__isnull=True)
        .exclude(environment="")
        .values("environment")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Template/Archive/Official repository counts
    template_repos = all_applications.filter(is_template_repository=True).count()
    archive_repos = all_applications.filter(is_archive_repository=True).count()
    official_repos = all_applications.filter(is_official_repository=True).count()

    # Simple example applications
    simple_example_apps = all_applications.filter(is_simple_example=True).count()

    # Pending deployment applications
    pending_deployment_apps = all_applications.filter(is_pending_deployment=True)

    context = {
        "the_site_name": THE_SITE_NAME,
        "page_title": "App Tracker Dashboard",
        # Basic counts
        "total_applications": total_applications,
        "total_projects": total_projects,
        "total_hosts": total_hosts,
        "total_lfs": total_lfs,
        # Feature counts
        "apps_with_production": apps_with_production,
        "apps_with_cicd": apps_with_cicd,
        "apps_with_custom_user": apps_with_custom_user,
        "apps_public_repo": apps_public_repo,
        "apps_all_tests_passing": apps_all_tests_passing,
        # Lists
        "favorite_apps": favorite_apps,
        "recent_apps": recent_apps,
        "testing_level_counts": testing_level_counts,
        "lfs_usage": lfs_usage,
        "projects_overview": projects_overview,
        "hosts_by_environment": hosts_by_environment,
        # Repository type counts
        "template_repos": template_repos,
        "archive_repos": archive_repos,
        "official_repos": official_repos,
        "simple_example_apps": simple_example_apps,
        # Pending deployment
        "pending_deployment_apps": pending_deployment_apps,
    }

    return render(request, "app_tracker/dashboard.html", context)


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


# Host views
class HostListView(RegistrationAcceptedMixin, ListView):
    model = Host


class HostDetailView(RegistrationAcceptedMixin, DetailView):
    model = Host


class HostCreateView(RegistrationAcceptedMixin, CreateView):
    model = Host
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:host_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["operating_system"].queryset = OperatingSystem.objects.order_by(
            "name"
        )
        return form


class HostUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = Host
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:host_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["operating_system"].queryset = OperatingSystem.objects.order_by(
            "name"
        )
        return form


class HostDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = Host
    success_url = reverse_lazy("app_tracker:host_list")


# URL views
class URLListView(RegistrationAcceptedMixin, ListView):
    model = URL


class URLDetailView(RegistrationAcceptedMixin, DetailView):
    model = URL


class URLCreateView(RegistrationAcceptedMixin, CreateView):
    model = URL
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:url_list")


class URLUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = URL
    fields = "__all__"
    success_url = reverse_lazy("app_tracker:url_list")


class URLDeleteView(RegistrationAcceptedMixin, DeleteView):
    model = URL
    success_url = reverse_lazy("app_tracker:url_list")
