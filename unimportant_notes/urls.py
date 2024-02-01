from django.urls import path

from . import views

app_name = "unimportant_notes"
urlpatterns = [
    path("", views.UnimportantNoteListView.as_view(), name="note_list"),
    path("create/", views.UnimportantNoteCreateView.as_view(), name="note_create"),
    path(
        "<int:pk>/update/",
        views.UnimportantNoteUpdateView.as_view(),
        name="note_update",
    ),
]
