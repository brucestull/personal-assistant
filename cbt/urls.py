from django.urls import path

from cbt.views import (
    CognitiveDistortionListView,
    ThoughtDetailView,
    ThoughtListView,
    ThoughtCreateView,
    home,
)

app_name = "cbt"
urlpatterns = [
    path(
        "",
        home,
        name="home",
    ),
    path(
        "cognitive-distortions/",
        CognitiveDistortionListView.as_view(),
        name="cognitive-distortion-list",
    ),
    path(
        "thoughts/",
        ThoughtListView.as_view(),
        name="thought-list",
    ),
    path(
        "thoughts/create/",
        ThoughtCreateView.as_view(),
        name="thought-create",
    ),
    path(
        "thoughts/create/<int:cognitive_distortion_id>/",
        ThoughtCreateView.as_view(),
        name="thought-create",
    ),
    path(
        "thoughts/<int:pk>/",
        ThoughtDetailView.as_view(),
        name="thought-detail",
    ),
]
