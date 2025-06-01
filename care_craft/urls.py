from django.urls import path

from . import views

app_name = "care_craft"
urlpatterns = [
    # Note URLs
    path("notes/", views.CareCraftNoteListView.as_view(), name="note_list"),
    path("notes/create/", views.CareCraftNoteCreateView.as_view(), name="note_create"),
    path(
        "notes/<int:pk>/", views.CareCraftNoteDetailView.as_view(), name="note_detail"
    ),
    path(
        "notes/<int:pk>/update/",
        views.CareCraftNoteUpdateView.as_view(),
        name="note_update",
    ),
    path(
        "notes/<int:pk>/delete/",
        views.CareCraftNoteDeleteView.as_view(),
        name="note_delete",
    ),
    # Activity URLs
    path("activities/", views.activity_list, name="activity_list"),
    path("activities/<int:pk>/", views.activity_detail, name="activity_detail"),
    path("activities/create/", views.activity_create, name="activity_create"),
    path("activities/<int:pk>/edit/", views.activity_update, name="activity_update"),
    path("activities/<int:pk>/delete/", views.activity_delete, name="activity_delete"),
]
