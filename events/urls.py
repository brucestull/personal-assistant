# events/urls.py

from django.urls import path

from events import views

app_name = "events"

urlpatterns = [
    path("", views.today_events, name="today"),
    path("sync/", views.sync_google_calendar, name="sync"),
    path("google/connect/", views.google_oauth_connect, name="google-connect"),
    path("google/callback/", views.google_oauth_callback, name="google-callback"),
]
