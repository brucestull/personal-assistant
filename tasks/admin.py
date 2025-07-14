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
        "tag",
        "created",
        "updated",
    )
    list_filter = ("priority", "tag", "user")
    search_fields = ("name", "information")
    raw_id_fields = ("tag", "priority", "user")
    list_select_related = ("priority", "tag", "user")
    ordering = ("priority__level", "-created")
