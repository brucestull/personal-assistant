from django.urls import path

from . import views


app_name = "valued_goals"
urlpatterns = [
    path(
        "html/",
        views.html_response,
        name="html-response",
    ),
    path(
        "goals/",
        views.goals,
        name="goals-list",
    ),
    path(
        "goals/create/",
        views.GoalsCreateView.as_view(),
        name="goals-create",
    ),
    path(
        "goals/update/<int:pk>/",
        views.GoalsUpdateView.as_view(),
        name="goals-update",
    ),
    path(
        "goals/<int:pk>/",
        views.GoalsDetailView.as_view(),
        name="goals-detail",
    ),
]
