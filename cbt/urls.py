from django.urls import path

from cbt.views import home, CognitiveDistortionListView


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
]
