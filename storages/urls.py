# storage/urls.py

from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "storage"
urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="storage/how_to_org.html"),
        name="storage_home",
    ),
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
    # SortDecision URLs
    path(
        "sortdecisions/", views.SortDecisionListView.as_view(), name="sortdecision_list"
    ),
    path(
        "sortdecisions/create/",
        views.SortDecisionCreateView.as_view(),
        name="sortdecision_create",
    ),
    path(
        "sortdecisions/<int:pk>/",
        views.SortDecisionDetailView.as_view(),
        name="sortdecision_detail",
    ),
    path(
        "sortdecisions/<int:pk>/update/",
        views.SortDecisionUpdateView.as_view(),
        name="sortdecision_update",
    ),
    path(
        "sortdecisions/<int:pk>/delete/",
        views.SortDecisionDeleteView.as_view(),
        name="sortdecision_delete",
    ),
    path("items/", views.ItemListView.as_view(), name="item_list"),
    path("items/create/", views.ItemCreateView.as_view(), name="item_create"),
    path("items/<int:pk>/", views.ItemDetailView.as_view(), name="item_detail"),
    path("items/<int:pk>/update/", views.ItemUpdateView.as_view(), name="item_update"),
    path("items/<int:pk>/delete/", views.ItemDeleteView.as_view(), name="item_delete"),
]
