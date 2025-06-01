# story_line/urls.py

from django.urls import path
from . import views

app_name = "story_line"

urlpatterns = [
    path("notes/", views.StoryLineNoteListView.as_view(), name="note_list"),
    path("notes/create/", views.StoryLineNoteCreateView.as_view(), name="note_create"),
    path(
        "notes/<int:pk>/", views.StoryLineNoteDetailView.as_view(), name="note_detail"
    ),
    path(
        "notes/<int:pk>/update/",
        views.StoryLineNoteUpdateView.as_view(),
        name="note_update",
    ),
    path(
        "notes/<int:pk>/delete/",
        views.StoryLineNoteDeleteView.as_view(),
        name="note_delete",
    ),
]
