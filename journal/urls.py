from django.urls import path
from . import views

app_name = "journal"
urlpatterns = [
    path("entry/create/", views.EntryCreateView.as_view(), name="entry_create"),
    path("entry/<int:pk>/", views.EntryDetailView.as_view(), name="entry_detail"),
    path(
        "entry/<int:pk>/update/", views.EntryUpdateView.as_view(), name="entry_update"
    ),
    path(
        "entry/<int:pk>/delete/", views.EntryDeleteView.as_view(), name="entry_delete"
    ),
    path("", views.EntryListView.as_view(), name="entry_list"),
]
