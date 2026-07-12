# events/admin.py

from django.contrib import admin

from events.models import CalendarEvent, GoogleCalendarCredentials


@admin.register(GoogleCalendarCredentials)
class GoogleCalendarCredentialsAdmin(admin.ModelAdmin):
    list_display = ("user", "updated")
    readonly_fields = ("updated",)
    list_filter = ("user",)


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = (
        "summary",
        "user",
        "start_datetime",
        "end_datetime",
        "google_event_id",
        "created",
    )
    list_filter = ("user",)
    search_fields = ("summary", "description", "google_event_id")
    readonly_fields = ("created", "updated", "google_event_id")
    date_hierarchy = "start_datetime"
