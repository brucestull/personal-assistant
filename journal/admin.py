from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("title", "date_created")
    search_fields = ("title", "content")
    ordering = ("-date_created",)
    date_hierarchy = "date_created"
    list_per_page = 10
