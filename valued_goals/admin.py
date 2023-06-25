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
    def get_queryset(self, request):
        print("get_queryset called")
        return super().get_queryset(request)


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
    def get_queryset(self, request):
        print("get_queryset called")
        return super().get_queryset(request)
