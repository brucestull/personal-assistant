from django.urls import path

from .views import WorkSearchActivityListView

app_name = "opportunity_search"
urlpatterns = [
    path(
        "work-search-activities/",
        WorkSearchActivityListView.as_view(),
        name="work_search_activity_list",
    ),
]
