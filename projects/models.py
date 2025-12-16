# projects/models.py
from django.conf import settings
from django.db import models


class Milestone(models.Model):
    workspace = models.ForeignKey("core.Workspace", on_delete=models.CASCADE)
    project = models.ForeignKey(
        "assets.Project", on_delete=models.CASCADE, related_name="milestones"
    )  # noqa: E501

    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    due = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)


class ProjectTask(models.Model):
    workspace = models.ForeignKey("core.Workspace", on_delete=models.CASCADE)
    project = models.ForeignKey(
        "assets.Project", on_delete=models.CASCADE, related_name="project_tasks"
    )  # noqa: E501
    milestone = models.ForeignKey(
        Milestone,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks",
    )  # noqa: E501

    STATUS = [
        ("backlog", "Backlog"),
        ("doing", "Doing"),
        ("blocked", "Blocked"),
        ("done", "Done"),
        ("dropped", "Dropped"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="backlog")

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )  # noqa: E501
    due = models.DateField(null=True, blank=True)
    effort_points = models.PositiveIntegerField(
        null=True, blank=True
    )  # tiny 1–5 scale works great


class ProjectLog(models.Model):
    workspace = models.ForeignKey("core.Workspace", on_delete=models.CASCADE)
    project = models.ForeignKey(
        "assets.Project", on_delete=models.CASCADE, related_name="logs"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )  # noqa: E501

    happened_at = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=255)
    detail = models.TextField(blank=True)
