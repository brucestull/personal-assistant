# thoughts/admin.py

from django.contrib import admin

from .models import Thought


@admin.register(Thought)
class ThoughtAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "created", "updated")
    list_filter = ("user",)
    search_fields = ("text", "user__username")
    ordering = ("-created",)
    readonly_fields = ("created", "updated")
    autocomplete_fields = ("user",)
