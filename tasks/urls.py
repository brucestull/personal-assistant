# tasks/urls.py
"""URL configuration for the tasks app."""

from django.urls import path
from tasks import views

app_name = "tasks"
urlpatterns = [
    # Tags
    path("tags/", views.TagListView.as_view(), name="tag_list"),
    path("tags/add/", views.TagCreateView.as_view(), name="tag_create"),
    path("tags/<int:pk>/", views.TagDetailView.as_view(), name="tag_detail"),
    path("tags/<int:pk>/edit/", views.TagUpdateView.as_view(), name="tag_update"),
    path("tags/<int:pk>/delete/", views.TagDeleteView.as_view(), name="tag_delete"),
    # Priorities
    path("priorities/", views.PriorityListView.as_view(), name="priority_list"),
    path("priorities/add/", views.PriorityCreateView.as_view(), name="priority_create"),
    path(
        "priorities/<int:pk>/",
        views.PriorityDetailView.as_view(),
        name="priority_detail",
    ),
    path(
        "priorities/<int:pk>/edit/",
        views.PriorityUpdateView.as_view(),
        name="priority_update",
    ),
    path(
        "priorities/<int:pk>/delete/",
        views.PriorityDeleteView.as_view(),
        name="priority_delete",
    ),
    # Tasks
    path("tasks/", views.TaskListView.as_view(), name="task_list"),
    path("tasks/add/", views.TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/complete/", views.complete_task, name="task_complete"),
]
