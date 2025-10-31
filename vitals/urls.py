# vitals/urls.py

from django.urls import path

from vitals import views

app_name = "vitals"
urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),
    path(
        "bloodpressures/",
        views.BloodPressureListView.as_view(),
        name="bloodpressure-list",
    ),
    path(
        "bloodpressures/create/",
        views.BloodPressureCreateView.as_view(),
        name="bloodpressure-create",
    ),
    path("bloodpressures/report/", views.BloodPressureReportView.as_view(), name="bloodpressure-report"),
    path("bodyweights/", views.bodyweight_list, name="bodyweight_list"),
    path("bodyweights/create/", views.bodyweight_create, name="bodyweight_create"),
    path("bodyweights/<int:pk>/", views.bodyweight_detail, name="bodyweight_detail"),
    path(
        "bodyweights/<int:pk>/edit/", views.bodyweight_update, name="bodyweight_update"
    ),
    path(
        "bodyweights/<int:pk>/delete/",
        views.bodyweight_delete,
        name="bodyweight_delete",
    ),
]
