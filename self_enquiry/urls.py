from django.urls import path

from self_enquiry.views import JournalListView, JournalCreateView


app_name = "self_enquiry"
urlpatterns = [
    path(
        "list/",
        JournalListView.as_view(),
        name="list",
    ),
    path(
        "create/",
        JournalCreateView.as_view(),
        name="create",
    ),
]
