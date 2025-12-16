from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "kanban_cabinet"

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # Stock items
    path("items/", views.StockItemListView.as_view(), name="stockitem_list"),
    path("items/add/", views.StockItemCreateView.as_view(), name="stockitem_create"),
    # New slug-based detail route
    path(
        "items/<slug:slug>/",
        views.StockItemDetailView.as_view(),
        name="stockitem_detail",
    ),
    path(
        "items/<slug:slug>/edit/",
        views.StockItemUpdateView.as_view(),
        name="stockitem_update",
    ),
    path(
        "items/<slug:slug>/delete/",
        views.StockItemDeleteView.as_view(),
        name="stockitem_delete",
    ),
    # Backwards compatibility: pk-based routes redirect to slug
    path(
        "items/by-id/<int:pk>/",
        views.StockItemPkRedirectView.as_view(),
        name="stockitem_detail_by_pk",
    ),
    # Locations
    path("locations/", views.LocationListView.as_view(), name="location_list"),
    path(
        "locations/add/",
        views.LocationCreateView.as_view(),
        name="location_create",
    ),
    path(
        "locations/<int:pk>/",
        views.LocationDetailView.as_view(),
        name="location_detail",
    ),
    path(
        "locations/<int:pk>/edit/",
        views.LocationUpdateView.as_view(),
        name="location_update",
    ),
    path(
        "locations/<int:pk>/delete/",
        views.LocationDeleteView.as_view(),
        name="location_delete",
    ),
]
