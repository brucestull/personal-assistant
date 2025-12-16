# inbox/models.py
from django.conf import settings
from django.db import models

class InboxItem(models.Model):
    workspace = models.ForeignKey("core.Workspace", on_delete=models.CASCADE, related_name="inbox_items")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    KIND = [
        ("idea", "Idea"),
        ("todo", "To-Do"),
        ("question", "Question"),
        ("bug", "Bug/Issue"),
        ("note", "Note"),
    ]
    kind = models.CharField(max_length=12, choices=KIND, default="idea")

    title = models.CharField(max_length=255)
    detail = models.TextField(blank=True)

    # optional links to your world
    project = models.ForeignKey("assets.Project", null=True, blank=True, on_delete=models.SET_NULL)
    asset = models.ForeignKey("assets.Asset", null=True, blank=True, on_delete=models.SET_NULL)

    STATUS = [("new", "New"), ("triaged", "Triaged"), ("done", "Done"), ("dropped", "Dropped")]
    status = models.CharField(max_length=10, choices=STATUS, default="new")
