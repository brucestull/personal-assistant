from django.urls import path

from . import views

app_name = "activity_tracker"
urlpatterns = [
    path("jsr/", views.json_response, name="json-response"),
    path("activities/", views.ActivityListView.as_view(), name="activity-list"),
    path(
        "activities/<int:pk>/",
        views.ActivityDetailView.as_view(),
        name="activity-detail",
    ),
    path(
        "activities/<int:pk>/complete/",
        views.complete_an_activity_view,
        name="complete-the-activity",
    ),
]
