from django.urls import path

from self_enquiry.views import JournalListView


app_name = "self_enquiry"
urlpatterns = [
    path(
        "list/",
        JournalListView.as_view(),
        name="list",
    ),
]
