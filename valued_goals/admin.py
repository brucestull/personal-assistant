from django.contrib import admin

from .models import ValuedGoal, CoreValue


@admin.register(ValuedGoal)
class ValuedGoalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created",
        "updated",
    )
    list_filter = (
        "created",
        "updated",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = (
        "created",
        "name",
    )


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created",
        "updated",
    )
    list_filter = (
        "created",
        "updated",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = (
        "name",
        "created",
    )
