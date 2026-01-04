# app_tracker/api/viewsets.py

from rest_framework.viewsets import ModelViewSet

from app_tracker.models import (
    Application,
    DjangoModel,
    Host,
    Label,
    LanguageFrameworkSystem,
    Note,
    OperatingSystem,
    OrganizationalConcept,
    Project,
    URL,
)
from app_tracker.api.serializers import (
    ApplicationSerializer,
    DjangoModelSerializer,
    HostSerializer,
    LabelSerializer,
    LanguageFrameworkSystemSerializer,
    NoteSerializer,
    OperatingSystemSerializer,
    OrganizationalConceptSerializer,
    ProjectSerializer,
    URLSerializer,
)


class OperatingSystemViewSet(ModelViewSet):
    queryset = OperatingSystem.objects.all().order_by("name")
    serializer_class = OperatingSystemSerializer


class LanguageFrameworkSystemViewSet(ModelViewSet):
    queryset = LanguageFrameworkSystem.objects.all().order_by("name")
    serializer_class = LanguageFrameworkSystemSerializer


class OrganizationalConceptViewSet(ModelViewSet):
    queryset = OrganizationalConcept.objects.all().order_by("name")
    serializer_class = OrganizationalConceptSerializer


class LabelViewSet(ModelViewSet):
    queryset = Label.objects.all().order_by("name")
    serializer_class = LabelSerializer


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all().order_by("-updated")
    serializer_class = NoteSerializer


class URLViewSet(ModelViewSet):
    queryset = URL.objects.all().order_by("label")
    serializer_class = URLSerializer


class HostViewSet(ModelViewSet):
    queryset = Host.objects.all().order_by("host_name")
    serializer_class = HostSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all().order_by("name")
    serializer_class = ProjectSerializer


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all().order_by("name")
    serializer_class = ApplicationSerializer


class DjangoModelViewSet(ModelViewSet):
    queryset = DjangoModel.objects.all().order_by("name")
    serializer_class = DjangoModelSerializer
