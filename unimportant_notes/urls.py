from django.urls import path

from . import views

app_name = "unimportant_notes"
urlpatterns = [
    path("", views.UnimportantNoteListView.as_view(), name="note_list"),
    path("create/", views.UnimportantNoteCreateView.as_view(), name="note_create"),
    path(
        "<int:pk>/",
        views.UnimportantNoteDetailView.as_view(),
        name="note_detail",
    ),
    path(
        "<int:pk>/update/",
        views.UnimportantNoteUpdateView.as_view(),
        name="note_update",
    ),
    path(
        "tags/",
        views.NoteTagListView.as_view(),
        name="tag_list",
    ),
    path(
        "tag/<int:pk>/",
        views.NoteTagDetailView.as_view(),
        name="tag_detail",
    ),
]
