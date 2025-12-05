from django.urls import path

from . import views

app_name = "kanban_cabinet"

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    # Stock items
    path("items/", views.StockItemListView.as_view(), name="stockitem_list"),
    path("items/add/", views.StockItemCreateView.as_view(), name="stockitem_create"),
    path(
        "items/<int:pk>/",
        views.StockItemDetailView.as_view(),
        name="stockitem_detail",
    ),
    path(
        "items/<int:pk>/edit/",
        views.StockItemUpdateView.as_view(),
        name="stockitem_update",
    ),
    path(
        "items/<int:pk>/delete/",
        views.StockItemDeleteView.as_view(),
        name="stockitem_delete",
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
