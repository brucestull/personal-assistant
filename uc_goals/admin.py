from django.contrib import admin

from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_ultimate_concern", "user", "completed")
    search_fields = ("name",)
    list_filter = ("parent",)
    ordering = ("name",)
