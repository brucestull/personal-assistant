from django.urls import path

from vitals.views import BloodPressureCreateView, BloodPressureListView, home

app_name = "vitals"
urlpatterns = [
    path(
        "",
        home,
        name="home",
    ),
    path(
        "bloodpressures/",
        BloodPressureListView.as_view(),
        name="bloodpressure-list",
    ),
    path(
        "bloodpressures/create/",
        BloodPressureCreateView.as_view(),
        name="bloodpressure-create")
]
