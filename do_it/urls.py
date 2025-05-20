# do_it/urls.py

from django.urls import path, include  # noqa: F401

from rest_framework import routers
from . import views

app_name = "do_it"
# REST router
router = routers.DefaultRouter()
router.register(r"tags", views.TagViewSet)
router.register(r"cycles", views.CycleViewSet)
router.register(r"tasks", views.TaskViewSet)
# router.register(r"completions", views.TaskCompletedViewSet)

urlpatterns = [
    # vanilla CRUD for Tag
    path("tags/", views.TagListView.as_view(), name="tag_list"),
    path("tags/create/", views.TagCreateView.as_view(), name="tag_create"),
    path("tags/<int:pk>/", views.TagDetailView.as_view(), name="tag_detail"),
    path("tags/<int:pk>/update/", views.TagUpdateView.as_view(), name="tag_update"),
    path("tags/<int:pk>/delete/", views.TagDeleteView.as_view(), name="tag_delete"),
    # vanilla CRUD for Cycle
    path("cycles/", views.CycleListView.as_view(), name="cycle_list"),
    path("cycles/create/", views.CycleCreateView.as_view(), name="cycle_create"),
    path("cycles/<int:pk>/", views.CycleDetailView.as_view(), name="cycle_detail"),
    path(
        "cycles/<int:pk>/update/", views.CycleUpdateView.as_view(), name="cycle_update"
    ),
    path(
        "cycles/<int:pk>/delete/", views.CycleDeleteView.as_view(), name="cycle_delete"
    ),
    # vanilla CRUD for Task
    path("tasks/", views.TaskListView.as_view(), name="task_list"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    # vanilla CRUD for TaskCompleted
    # path(
    #     "completions/",
    #     views.TaskCompletedListView.as_view(),
    #     name="task_completed_list",
    # ),
    # path(
    #     "completions/create/",
    #     views.TaskCompletedCreateView.as_view(),
    #     name="task_completed_create",
    # ),
    # path(
    #     "completions/<int:pk>/",
    #     views.TaskCompletedDetailView.as_view(),
    #     name="task_completed_detail",
    # ),
    # path(
    #     "completions/<int:pk>/update/",
    #     views.TaskCompletedUpdateView.as_view(),
    #     name="task_completed_update",
    # ),
    # path(
    #     "completions/<int:pk>/delete/",
    #     views.TaskCompletedDeleteView.as_view(),
    #     name="task_completed_delete",
    # ),
    # REST API endpoints
    path("api/", include(router.urls)),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
