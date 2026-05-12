from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .api_views import ThoughtViewSet

app_name = "bus_drive"

router = DefaultRouter()
router.register(r"thoughts", ThoughtViewSet, basename="api-thought")

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("spa/", views.SPAView.as_view(), name="spa"),
    path("thoughts/", views.ThoughtListView.as_view(), name="thought-list"),
    path("thoughts/add/", views.ThoughtCreateView.as_view(), name="thought-create"),
    path(
        "thoughts/<int:pk>/",
        views.ThoughtDetailView.as_view(),
        name="thought-detail",
    ),
    path(
        "thoughts/<int:pk>/edit/",
        views.ThoughtUpdateView.as_view(),
        name="thought-update",
    ),
    path(
        "thoughts/<int:pk>/delete/",
        views.ThoughtDeleteView.as_view(),
        name="thought-delete",
    ),
    path(
        "thoughts/<int:pk>/send-email/",
        views.ThoughtSendEmailView.as_view(),
        name="thought-send-email",
    ),
    path("api/", include(router.urls)),
]
