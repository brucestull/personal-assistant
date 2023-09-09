from django.urls import path

from app_tracker.views import (
    home,
    OrganizationalConceptListView,
)


app_name = "app_tracker"
urlpatterns = [
    path(
        "",
        home,
        name="home",
    ),
]
