from django.contrib import admin

from .models import AudioFile


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "file", "file_type", "user")
    search_fields = ("name", "description")
    list_filter = ("file_type",)
