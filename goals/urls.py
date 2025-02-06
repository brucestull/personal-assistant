from django.urls import path

from . import views

app_name = "goals"
urlpatterns = [
    path("", views.GoalListView.as_view(), name="goal_list"),
    # path("create/", views.GoalCreateView.as_view(), name="goal_create"),
    # path(
    #     "<int:pk>/",
    #     views.GoalDetailView.as_view(),
    #     name="goal_detail",
    # ),
    # path(
    #     "<int:pk>/update/",
    #     views.GoalUpdateView.as_view(),
    #     name="goal_update",
    # ),
    # path(
    #     "tags/",
    #     views.GoalTagListView.as_view(),
    #     name="tag_list",
    # ),
    # path(
    #     "tag/<int:pk>/",
    #     views.GoalTagDetailView.as_view(),
    #     name="tag_detail",
    # ),
]
