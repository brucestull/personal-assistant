from django.contrib import admin

from .models import Activity, CareCraftNote


@admin.register(CareCraftNote)
class CareCraftNoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created", "updated")
    search_fields = ("user__username", "content")
    list_filter = ("created", "updated")
    date_hierarchy = "created"
    ordering = ("-created",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "description")
    search_fields = ("description",)
