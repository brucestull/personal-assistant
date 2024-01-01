from django.urls import path

from . import views

app_name = "value_centric"
urlpatterns = [
    path(
        "create/", views.PersonalValueCreateView.as_view(), name="personal-value-create"
    ),
    path(
        "<int:pk>/",
        views.PersonalValueDetailView.as_view(),
        name="personal-value-detail",
    ),
    path(
        "<int:pk>/update/",
        views.PersonalValueUpdateView.as_view(),
        name="personal-value-update",
    ),
    path(
        "<int:pk>/delete/",
        views.PersonalValueDeleteView.as_view(),
        name="personal-value-delete",
    ),
    path("", views.PersonalValueListView.as_view(), name="personal-value-list"),
]
