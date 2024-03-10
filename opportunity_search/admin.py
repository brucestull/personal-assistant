from django.contrib import admin

from .models import WorkSearchActivity


@admin.register(WorkSearchActivity)
class WorkSearchActivityAdmin(admin.ModelAdmin):
    list_display = ("description",)
    search_fields = ("description",)
    fieldsets = (
        (
            "Work Search Activity",
            {"fields": ("description", "created_at", "updated_at")},
        ),
    )
