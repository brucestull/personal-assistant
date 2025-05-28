# storage/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Type URLs
    path("types/", views.TypeListView.as_view(), name="type_list"),
    path("types/<int:pk>/", views.TypeDetailView.as_view(), name="type_detail"),
    path("types/create/", views.TypeCreateView.as_view(), name="type_create"),
    path("types/<int:pk>/update/", views.TypeUpdateView.as_view(), name="type_update"),
    path("types/<int:pk>/delete/", views.TypeDeleteView.as_view(), name="type_delete"),
    # StorageArea URLs
    path("storageareas/", views.StorageAreaListView.as_view(), name="storagearea_list"),
    path(
        "storageareas/<int:pk>/",
        views.StorageAreaDetailView.as_view(),
        name="storagearea_detail",
    ),
    path(
        "storageareas/create/",
        views.StorageAreaCreateView.as_view(),
        name="storagearea_create",
    ),
    path(
        "storageareas/<int:pk>/update/",
        views.StorageAreaUpdateView.as_view(),
        name="storagearea_update",
    ),
    path(
        "storageareas/<int:pk>/delete/",
        views.StorageAreaDeleteView.as_view(),
        name="storagearea_delete",
    ),
]
