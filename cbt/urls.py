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
        "cognative-distortions/",
        CognitiveDistortionListView.as_view(),
        name="cognative-distortion-list",
    ),
]
