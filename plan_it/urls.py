# plan_it/urls.py

from django.urls import path

from . import views

app_name = "plan_it"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # StorageLocation
    path(
        "locations/",
        views.StorageLocationListView.as_view(),
        name="storage_location_list",
    ),
    path(
        "locations/add/",
        views.StorageLocationCreateView.as_view(),
        name="storage_location_add",
    ),
    path(
        "locations/<int:pk>/edit/",
        views.StorageLocationUpdateView.as_view(),
        name="storage_location_edit",
    ),
    path(
        "locations/<int:pk>/delete/",
        views.StorageLocationDeleteView.as_view(),
        name="storage_location_delete",
    ),
    # Item
    path("items/", views.ItemListView.as_view(), name="item_list"),
    path("items/add/", views.ItemCreateView.as_view(), name="item_add"),
    path("items/<int:pk>/edit/", views.ItemUpdateView.as_view(), name="item_edit"),
    path("items/<int:pk>/delete/", views.ItemDeleteView.as_view(), name="item_delete"),
    # ActivityType
    path(
        "activity-types/",
        views.ActivityTypeListView.as_view(),
        name="activity_type_list",
    ),
    path(
        "activity-types/add/",
        views.ActivityTypeCreateView.as_view(),
        name="activity_type_add",
    ),
    path(
        "activity-types/<int:pk>/edit/",
        views.ActivityTypeUpdateView.as_view(),
        name="activity_type_edit",
    ),
    path(
        "activity-types/<int:pk>/delete/",
        views.ActivityTypeDeleteView.as_view(),
        name="activity_type_delete",
    ),
    # Activity
    path("activities/", views.ActivityListView.as_view(), name="activity_list"),
    path("activities/add/", views.ActivityCreateView.as_view(), name="activity_add"),
    path(
        "activities/<int:pk>/edit/",
        views.ActivityUpdateView.as_view(),
        name="activity_edit",
    ),
    path(
        "activities/<int:pk>/delete/",
        views.ActivityDeleteView.as_view(),
        name="activity_delete",
    ),
    path(
        "activities/<int:pk>/complete/",
        views.mark_activity_completed,
        name="activity_complete",
    ),
    # ActivityLocation routes
    path(
        "activity-locations/",
        views.ActivityLocationListView.as_view(),
        name="activity_location_list",
    ),
    path(
        "activity-locations/add/",
        views.ActivityLocationCreateView.as_view(),
        name="activity_location_add",
    ),
    path(
        "activity-locations/<int:pk>/edit/",
        views.ActivityLocationUpdateView.as_view(),
        name="activity_location_edit",
    ),
    path(
        "activity-locations/<int:pk>/delete/",
        views.ActivityLocationDeleteView.as_view(),
        name="activity_location_delete",
    ),
]
