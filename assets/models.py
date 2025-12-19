# assets/models.py

from django.db import models

from core.models import Workspace


class FormFactor(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class OS(models.Model):
    name = models.CharField(max_length=80)
    version = models.CharField(max_length=40, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Operating Systems"

    def __str__(self) -> str:
        # "Ubuntu 24.04", "Debian" (no trailing space if version is blank)
        if self.version:
            return f"{self.name} {self.version}"
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=120)
    version = models.CharField(max_length=60, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        if self.version:
            return f"{self.name} {self.version}"
        return self.name


class Project(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="projects"
    )  # noqa: E501

    STATUS = [
        ("inbox", "Inbox"),
        ("backlog", "Backlog"),
        ("active", "Active"),
        ("paused", "Paused"),
        ("done", "Done"),
        ("dropped", "Dropped"),
        ("archived", "Archived"),
    ]
    PRIORITY = [("low", "Low"), ("med", "Medium"), ("high", "High")]

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    slug = models.SlugField()

    status = models.CharField(max_length=12, choices=STATUS, default="inbox")
    priority = models.CharField(max_length=8, choices=PRIORITY, default="med")

    # optional but super useful
    outcome = models.TextField(blank=True, help_text="What 'done' looks like.")
    next_action = models.CharField(max_length=255, blank=True)
    target_date = models.DateField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    # nice for hierarchies (Homelab > Bird Cam > Classifier)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subprojects",  # noqa: E501
    )

    class Meta:
        unique_together = [("workspace", "slug")]


class Asset(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="assets"
    )

    # Rename from primary_project -> project
    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="primary_assets",  # keep or rename if you want
    )

    # Keep the M2M if you still want multi-project tagging (your other tests use it)
    projects = models.ManyToManyField(Project, blank=True, related_name="assets")

    # ... rest unchanged ...

    @property
    def primary_project(self):
        return self.project

    @primary_project.setter
    def primary_project(self, value):
        self.project = value