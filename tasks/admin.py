# tasks/admin.py
from django.contrib import admin
from .models import Tag, Priority, Task


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "created",
        "updated",
    )
    list_filter = ("user",)
    search_fields = ("name", "description")
    ordering = ("-created",)


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
        "user",
        "created",
        "updated",
    )
    list_filter = ("level", "user")
    search_fields = ("name",)
    ordering = ("level",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "priority",
        "display_tags",  # New method for displaying tags
    )
    list_filter = ("priority", "tag", "user")
    list_select_related = ("priority", "user")
    filter_horizontal = ("tag",)
    search_fields = ("name", "information")
    ordering = ("priority__level", "-created")

    def display_tags(self, obj):
        return ", ".join(str(tag.name) for tag in obj.tag.all())

    display_tags.short_description = "Tags"
