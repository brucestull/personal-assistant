from django.urls import path
from .views import (
    AudioFileListView,
    AudioFileDetailView,
    AudioFileCreateView,
    AudioFileUpdateView,
    AudioFileDeleteView,
)

app_name = "sonic_text"
urlpatterns = [
    path("audio/", AudioFileListView.as_view(), name="audiofile_list"),
    path("audio/<int:pk>/", AudioFileDetailView.as_view(), name="audiofile_detail"),
    path("audio/new/", AudioFileCreateView.as_view(), name="audiofile_create"),
    path(
        "audio/<int:pk>/edit/", AudioFileUpdateView.as_view(), name="audiofile_update"
    ),
    path(
        "audio/<int:pk>/delete/", AudioFileDeleteView.as_view(), name="audiofile_delete"
    ),
]
