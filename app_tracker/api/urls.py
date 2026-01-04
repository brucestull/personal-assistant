# app_tracker/api/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app_tracker.api.viewsets import (
    ApplicationViewSet,
    DjangoModelViewSet,
    HostViewSet,
    LabelViewSet,
    LanguageFrameworkSystemViewSet,
    NoteViewSet,
    OperatingSystemViewSet,
    OrganizationalConceptViewSet,
    ProjectViewSet,
    URLViewSet,
)

router = DefaultRouter()
router.register(r"operating-systems", OperatingSystemViewSet, basename="operating-system")
router.register(r"language-framework-systems", LanguageFrameworkSystemViewSet, basename="language-framework-system")
router.register(r"organizational-concepts", OrganizationalConceptViewSet, basename="organizational-concept")
router.register(r"labels", LabelViewSet, basename="label")
router.register(r"notes", NoteViewSet, basename="note")
router.register(r"urls", URLViewSet, basename="url")
router.register(r"hosts", HostViewSet, basename="host")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"applications", ApplicationViewSet, basename="application")
router.register(r"django-models", DjangoModelViewSet, basename="django-model")

urlpatterns = [
    path("", include(router.urls)),
]
