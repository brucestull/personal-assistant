# events/views.py

import logging

from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from config.settings import THE_SITE_NAME
from events.forms import EventForm
from events.models import CalendarEvent
from events.utils.google_calendar import (
    create_google_calendar_event,
    get_credentials_for_user,
    get_oauth_flow,
    save_credentials_for_user,
    sync_events_from_google,
)

logger = logging.getLogger(__name__)


@login_required
def today_events(request):
    """
    Display today's events for the logged-in user and provide a form to add a
    new event.  A "Sync with Google Calendar" button is also rendered here.
    """
    user = request.user
    today = timezone.localdate()

    # Fetch today's events for this user
    events = CalendarEvent.objects.filter(
        user=user,
        start_datetime__date=today,
    ).order_by("start_datetime")

    # Check if user has linked their Google account
    has_google_credentials = get_credentials_for_user(user) is not None

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = user
            event.save()

            # Attempt to create the event in Google Calendar as well
            if has_google_credentials:
                try:
                    google_id = create_google_calendar_event(user, event)
                    if google_id:
                        event.google_event_id = google_id
                        event.save(update_fields=["google_event_id"])
                    messages.success(
                        request,
                        f'Event "{event.summary}" saved and added to Google Calendar.',
                    )
                except Exception as exc:
                    logger.exception("Failed to push event to Google Calendar: %s", exc)
                    messages.warning(
                        request,
                        f'Event "{event.summary}" saved locally, but could not be '
                        "added to Google Calendar. Check your connection and try again.",  # noqa: E501
                    )
            else:
                messages.success(
                    request,
                    f'Event "{event.summary}" saved.',
                )
            return redirect("events:today")
    else:
        # Pre-fill start time with the current time rounded to the nearest hour
        now = timezone.localtime()
        initial_start = now.replace(minute=0, second=0, microsecond=0)
        initial_end = initial_start + timedelta(hours=1)
        form = EventForm(
            initial={
                "start_datetime": initial_start,
                "end_datetime": initial_end,
            }
        )

    return render(
        request,
        "events/today_events.html",
        {
            "the_site_name": THE_SITE_NAME,
            "page_title": "Today's Events",
            "events": events,
            "form": form,
            "today": today,
            "has_google_credentials": has_google_credentials,
        },
    )


@login_required
@require_POST
def sync_google_calendar(request):
    """
    Trigger a manual sync from the user's primary Google Calendar.
    Upserts fetched events into the local database and shows a status message.
    """
    user = request.user
    try:
        created, updated = sync_events_from_google(user)
        messages.success(
            request,
            f"Sync complete! {created} new event(s) added, {updated} event(s) updated.",
        )
    except ValueError as exc:
        messages.error(request, str(exc))
    except Exception as exc:
        logger.exception("Google Calendar sync failed: %s", exc)
        messages.error(
            request,
            "Sync failed. Please reconnect your Google Calendar and try again.",
        )
    return redirect("events:today")


@login_required
def google_oauth_connect(request):
    """
    Start the Google OAuth2 authorisation flow.  Redirects the user to Google's
    consent screen.
    """
    redirect_uri = request.build_absolute_uri("/events/google/callback/")
    flow = get_oauth_flow(redirect_uri)
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    request.session["google_oauth_state"] = state
    return redirect(authorization_url)


@login_required
def google_oauth_callback(request):
    """
    Handle the OAuth2 callback from Google.  Exchanges the authorisation code
    for access/refresh tokens and persists them for the user.
    """
    state = request.session.get("google_oauth_state", "")
    redirect_uri = request.build_absolute_uri("/events/google/callback/")
    flow = get_oauth_flow(redirect_uri)
    flow.fetch_token(
        authorization_response=request.build_absolute_uri(),
        state=state,
    )
    save_credentials_for_user(request.user, flow.credentials)
    messages.success(
        request,
        "Google Calendar connected successfully! You can now sync your events.",
    )
    return redirect("events:today")
