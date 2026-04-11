from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .api_views import ItemViewSet, StorageLocationViewSet

app_name = "item_location"

router = DefaultRouter()
router.register(r"locations", StorageLocationViewSet, basename="api-location")
router.register(r"items", ItemViewSet, basename="api-item")

urlpatterns = [
    # Dashboard
    path("", views.DashboardView.as_view(), name="dashboard"),
    # Vue.js SPA
    path("spa/", views.SPAView.as_view(), name="spa"),
    # StorageLocation CRUD
    path(
        "locations/",
        views.StorageLocationListView.as_view(),
        name="location-list",
    ),
    path(
        "locations/add/",
        views.StorageLocationCreateView.as_view(),
        name="location-create",
    ),
    path(
        "locations/<int:pk>/",
        views.StorageLocationDetailView.as_view(),
        name="location-detail",
    ),
    path(
        "locations/<int:pk>/edit/",
        views.StorageLocationUpdateView.as_view(),
        name="location-update",
    ),
    path(
        "locations/<int:pk>/delete/",
        views.StorageLocationDeleteView.as_view(),
        name="location-delete",
    ),
    # Item CRUD
    path("items/", views.ItemListView.as_view(), name="item-list"),
    path("items/add/", views.ItemCreateView.as_view(), name="item-create"),
    path("items/<int:pk>/", views.ItemDetailView.as_view(), name="item-detail"),
    path(
        "items/<int:pk>/edit/",
        views.ItemUpdateView.as_view(),
        name="item-update",
    ),
    path(
        "items/<int:pk>/delete/",
        views.ItemDeleteView.as_view(),
        name="item-delete",
    ),
    # REST API
    path("api/", include(router.urls)),
]
