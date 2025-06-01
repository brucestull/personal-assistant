# story_line/admin.py

from django.contrib import admin
from .models import StoryLineNote


@admin.register(StoryLineNote)
class StoryLineNoteAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    list_filter = ("user", "created")
    search_fields = ("title", "content", "user__username")
