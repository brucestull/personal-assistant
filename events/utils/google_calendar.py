# events/utils/google_calendar.py
"""
Utility functions for interacting with the Google Calendar API.

Requires environment variables:
    GOOGLE_CLIENT_ID      – OAuth2 client ID from Google Cloud Console
    GOOGLE_CLIENT_SECRET  – OAuth2 client secret from Google Cloud Console

Each user's OAuth2 tokens are persisted in GoogleCalendarCredentials.
"""

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from events.models import CalendarEvent, GoogleCalendarCredentials

SCOPES = ["https://www.googleapis.com/auth/calendar"]

_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
_TOKEN_URI = "https://oauth2.googleapis.com/token"


def get_oauth_flow(redirect_uri: str) -> Flow:
    """Return a configured OAuth2 Flow for the Google Calendar scope."""
    client_config = {
        "web": {
            "client_id": _CLIENT_ID,
            "client_secret": _CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": _TOKEN_URI,
        }
    }
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=redirect_uri,
    )
    return flow


def get_credentials_for_user(user) -> Credentials | None:
    """
    Load stored OAuth2 credentials for *user* from the database.
    Refreshes the access token automatically if it has expired.
    Returns None if no credentials are stored.
    """
    try:
        stored = GoogleCalendarCredentials.objects.get(user=user)
    except GoogleCalendarCredentials.DoesNotExist:
        return None

    if not stored.refresh_token:
        return None

    creds = Credentials(
        token=stored.token or None,
        refresh_token=stored.refresh_token,
        token_uri=stored.token_uri or _TOKEN_URI,
        client_id=stored.client_id or _CLIENT_ID,
        client_secret=stored.client_secret or _CLIENT_SECRET,
        scopes=stored.scopes.split() if stored.scopes else SCOPES,
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        _persist_credentials(user, creds)

    return creds


def save_credentials_for_user(user, creds: Credentials) -> None:
    """Persist (or update) Google OAuth2 credentials for *user*."""
    _persist_credentials(user, creds)


def _persist_credentials(user, creds: Credentials) -> None:
    GoogleCalendarCredentials.objects.update_or_create(
        user=user,
        defaults={
            "token": creds.token or "",
            "refresh_token": creds.refresh_token or "",
            "token_uri": creds.token_uri or _TOKEN_URI,
            "client_id": creds.client_id or _CLIENT_ID,
            "client_secret": creds.client_secret or _CLIENT_SECRET,
            "scopes": " ".join(creds.scopes) if creds.scopes else "",
        },
    )


def sync_events_from_google(user) -> tuple[int, int]:
    """
    Fetch upcoming events from the user's primary Google Calendar and
    upsert them into the local CalendarEvent table.

    Returns (created_count, updated_count).
    """
    creds = get_credentials_for_user(user)
    if creds is None:
        raise ValueError("No Google Calendar credentials found for this user.")

    service = build("calendar", "v3", credentials=creds)

    result = (
        service.events()
        .list(
            calendarId="primary",
            maxResults=250,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    items = result.get("items", [])
    created_count = 0
    updated_count = 0

    for item in items:
        google_event_id = item.get("id", "")
        summary = item.get("summary", "(no title)")
        description = item.get("description", "")

        start = item.get("start", {})
        end = item.get("end", {})

        start_str = start.get("dateTime") or start.get("date")
        end_str = end.get("dateTime") or end.get("date")

        if not start_str or not end_str:
            continue

        from django.utils.dateparse import parse_datetime, parse_date
        from django.utils import timezone

        start_dt = parse_datetime(start_str) or _date_to_datetime(
            parse_date(start_str)
        )
        end_dt = parse_datetime(end_str) or _date_to_datetime(parse_date(end_str))

        if start_dt is None or end_dt is None:
            continue

        # Make timezone-aware if naive
        if timezone.is_naive(start_dt):
            start_dt = timezone.make_aware(start_dt)
        if timezone.is_naive(end_dt):
            end_dt = timezone.make_aware(end_dt)

        event, created = CalendarEvent.objects.update_or_create(
            user=user,
            google_event_id=google_event_id,
            defaults={
                "summary": summary,
                "description": description,
                "start_datetime": start_dt,
                "end_datetime": end_dt,
            },
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

    return created_count, updated_count


def create_google_calendar_event(user, event: "CalendarEvent") -> str:
    """
    Create a new event on the user's primary Google Calendar.
    Returns the Google event ID assigned by Google, or an empty string on failure.
    """
    creds = get_credentials_for_user(user)
    if creds is None:
        raise ValueError("No Google Calendar credentials found for this user.")

    service = build("calendar", "v3", credentials=creds)

    from django.utils import timezone

    def _format_dt(dt):
        # Google Calendar expects RFC 3339 strings
        if timezone.is_aware(dt):
            return dt.isoformat()
        return timezone.make_aware(dt).isoformat()

    body = {
        "summary": event.summary,
        "start": {"dateTime": _format_dt(event.start_datetime)},
        "end": {"dateTime": _format_dt(event.end_datetime)},
    }
    if event.description:
        body["description"] = event.description

    created = (
        service.events().insert(calendarId="primary", body=body).execute()
    )
    return created.get("id", "")


def _date_to_datetime(d):
    """Convert a date to a datetime at midnight."""
    if d is None:
        return None
    from datetime import datetime

    return datetime(d.year, d.month, d.day)
