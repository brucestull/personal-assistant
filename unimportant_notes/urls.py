from django.urls import path

from . import views

app_name = "unimportant_notes"
urlpatterns = [
    path("notes/", views.NoteListView.as_view(), name="note_list"),
    path("notes/create/", views.NoteCreateView.as_view(), name="note_create"),
]
