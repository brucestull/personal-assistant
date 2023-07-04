from django.urls import path

from self_enquiry.views import JournalListView, JournalDetailView
from self_enquiry.views import JournalCreateView, JournalUpdateView
from self_enquiry.views import JournalDeleteView, JournalConfirmDeleteView


app_name = "self_enquiry"
urlpatterns = [
    path(
        "create/",
        JournalCreateView.as_view(),
        name="create",
    ),
    path(
        "list/",
        JournalListView.as_view(),
        name="list",
    ),
    path(
        "<int:pk>/detail/",
        JournalDetailView.as_view(),
        name="detail",
    ),
    path(
        "<int:pk>/update/",
        JournalUpdateView.as_view(),
        name="update",
    ),
    path(
        "<int:pk>/delete/",
        JournalDeleteView.as_view(),
        name="delete",
    ),
    path(
        "<int:pk>/confirm-delete/",
        JournalConfirmDeleteView.as_view(),
        name="confirm-delete",
    ),
]
