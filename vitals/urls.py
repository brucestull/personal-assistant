from django.urls import path

from vitals.views import home, BloodPressureListView


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
    )
]
