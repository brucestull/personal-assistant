# events/models.py

from django.db import models

from config.settings import AUTH_USER_MODEL


class GoogleCalendarCredentials(models.Model):
    """
    Stores per-user OAuth2 tokens for Google Calendar access.
    One record per user.
    """

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="google_calendar_credentials",
    )
    token = models.TextField(blank=True, default="")
    refresh_token = models.TextField(blank=True, default="")
    token_uri = models.TextField(blank=True, default="")
    client_id = models.TextField(blank=True, default="")
    client_secret = models.TextField(blank=True, default="")
    scopes = models.TextField(
        blank=True,
        default="",
        help_text="Space-separated list of granted OAuth2 scopes.",
    )
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Google Calendar Credentials"
        verbose_name_plural = "Google Calendar Credentials"

    def __str__(self):
        return f"Google Calendar credentials for {self.user.username}"


class CalendarEvent(models.Model):
    """
    Stores a Google Calendar event for a user.
    Events can be created locally and pushed to Google Calendar, or pulled from it.
    """

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="calendar_events",
    )
    google_event_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="The event ID assigned by Google Calendar.",
    )
    summary = models.CharField(
        max_length=255,
        help_text="The title/summary of the event (required by Google Calendar).",
    )
    start_datetime = models.DateTimeField(
        help_text="Start date and time of the event.",
    )
    end_datetime = models.DateTimeField(
        help_text="End date and time of the event.",
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Optional description/notes for the event.",
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_datetime"]
        verbose_name = "Calendar Event"
        verbose_name_plural = "Calendar Events"

    def __str__(self):
        return f"{self.summary} ({self.start_datetime.strftime('%Y-%m-%d %H:%M')})"
