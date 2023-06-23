from django.contrib import admin

from .models import ValuedGoal, CoreValue


@admin.register(ValuedGoal)
class ValuedGoalAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'target_date',
        'completed',
        'completed_date',
        'created',
        'updated',
    )
    list_filter = (
        'completed',
        'created',
        'updated',
    )
    search_fields = (
        'name',
        'description',
    )
    ordering = (
        'completed',
        '-target_date',
        '-created',
    )


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'created',
        'updated',
    )
    list_filter = (
        'created',
        'updated',
    )
    search_fields = (
        'name',
        'description',
    )
    ordering = (
        'name',
        'created',
    )
