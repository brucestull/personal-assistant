# thoughts/urls.py

from django.urls import path

from thoughts import views

app_name = "thoughts"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("thoughts/", views.ThoughtListView.as_view(), name="thought-list"),
    path("thoughts/add/", views.ThoughtCreateView.as_view(), name="thought-create"),
    path(
        "thoughts/<int:pk>/edit/",
        views.ThoughtUpdateView.as_view(),
        name="thought-update",
    ),
    path(
        "thoughts/<int:pk>/delete/",
        views.ThoughtDeleteView.as_view(),
        name="thought-delete",
    ),
]
