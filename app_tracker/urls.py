from django.urls import path

from app_tracker.views import OrganizationalConceptListView, home

app_name = "app_tracker"
urlpatterns = [
    path(
        "",
        home,
        name="home",
    ),
    path(
        "organizational-concepts/",
        OrganizationalConceptListView.as_view(),
        name="organizational-concepts",
    ),
]
