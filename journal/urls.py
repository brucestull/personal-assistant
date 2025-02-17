from django.urls import path
from . import views

app_name = "journal"
urlpatterns = [
    path("", views.EntryListView.as_view(), name="entry_list"),
    path("entry/<int:pk>/", views.EntryDetailView.as_view(), name="entry_detail"),
]
