from django.urls import path

from . import views

app_name = "unimportant_notes"
urlpatterns = [
    path("notes/", views.NoteListView.as_view(), name="note_list"),
]
