# ideas/admin.py

from django.contrib import admin

from .models import Idea


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ("author",)
    search_fields = ("name", "concept")
