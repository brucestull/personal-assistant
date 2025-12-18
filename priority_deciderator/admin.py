from django.contrib import admin
from .models import Reminder, ReminderSchedule


class ReminderScheduleInline(admin.TabularInline):
    """Inline for managing schedules within a Reminder."""
    model = ReminderSchedule
    extra = 0
    fields = ("frequency", "time", "day_of_week", "day_of_month", "is_active")
    readonly_fields = ("created", "updated")


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    """Admin for Reminder model."""
    
    list_display = ("name", "user", "is_active", "created", "updated")
    list_filter = ("is_active", "created", "user")
    search_fields = ("name", "description", "user__username", "user__email")
    readonly_fields = ("created", "updated")
    inlines = [ReminderScheduleInline]
    
    fieldsets = (
        (None, {
            "fields": ("name", "description", "user", "is_active")
        }),
        ("Timestamps", {
            "fields": ("created", "updated"),
            "classes": ("collapse",),
        }),
    )


@admin.register(ReminderSchedule)
class ReminderScheduleAdmin(admin.ModelAdmin):
    """Admin for ReminderSchedule model."""
    
    list_display = (
        "reminder",
        "frequency",
        "time",
        "day_of_week",
        "day_of_month",
        "is_active",
        "created",
    )
    list_filter = ("frequency", "is_active", "created")
    search_fields = ("reminder__name", "reminder__user__username")
    readonly_fields = ("created", "updated", "periodic_task")
    
    fieldsets = (
        (None, {
            "fields": ("reminder", "frequency", "time", "is_active")
        }),
        ("Schedule Details", {
            "fields": ("day_of_week", "day_of_month"),
        }),
        ("Celery Beat Integration", {
            "fields": ("periodic_task",),
            "classes": ("collapse",),
        }),
        ("Timestamps", {
            "fields": ("created", "updated"),
            "classes": ("collapse",),
        }),
    )
