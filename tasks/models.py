# tasks/models.py
"""Models for the tasks app."""

from django.db import models

from base.models import CreatedUpdatedBase
from config.settings import AUTH_USER_MODEL


class Tag(CreatedUpdatedBase):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tags"
    )

    def __str__(self):
        return f"#{self.name}"


class Priority(CreatedUpdatedBase):
    name = models.CharField(max_length=50)
    level = models.PositiveIntegerField(unique=True)
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="priorities"
    )

    class Meta:
        ordering = ["level"]
        verbose_name_plural = "priorities"

    def __str__(self):
        return f"{self.name} (Level {self.level})"


class Task(CreatedUpdatedBase):
    name = models.CharField(max_length=100)
    information = models.TextField(blank=True)
    tag = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="tasks",
        help_text="Tags associated with this task (optional).",
    )
    priority = models.ForeignKey(
        Priority, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks"
    )

    class Meta:
        ordering = ["priority__level", "name", "created"]

    def __str__(self):
        return self.name
