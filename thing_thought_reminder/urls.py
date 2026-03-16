from django.urls import path

from . import views

app_name = "thing_thought_reminder"

urlpatterns = [
    # Dashboard
    path("", views.DashboardView.as_view(), name="dashboard"),
    # Thing CRUD
    path("things/", views.ThingListView.as_view(), name="thing-list"),
    path("things/add/", views.ThingCreateView.as_view(), name="thing-create"),
    path("things/<int:pk>/", views.ThingDetailView.as_view(), name="thing-detail"),
    path(
        "things/<int:pk>/edit/", views.ThingUpdateView.as_view(), name="thing-update"
    ),
    path(
        "things/<int:pk>/delete/",
        views.ThingDeleteView.as_view(),
        name="thing-delete",
    ),
    # Thought CRUD
    path("thoughts/", views.ThoughtListView.as_view(), name="thought-list"),
    path("thoughts/add/", views.ThoughtCreateView.as_view(), name="thought-create"),
    path(
        "thoughts/<int:pk>/", views.ThoughtDetailView.as_view(), name="thought-detail"
    ),
    path(
        "thoughts/<int:pk>/edit/",
        views.ThoughtUpdateView.as_view(),
        name="thought-update",
    ),
    path(
        "thoughts/<int:pk>/delete/",
        views.ThoughtDeleteView.as_view(),
        name="thought-delete",
    ),
    # ReminderSchedule CRUD
    path(
        "reminders/",
        views.ReminderScheduleListView.as_view(),
        name="reminder-list",
    ),
    path(
        "reminders/add/",
        views.ReminderScheduleCreateView.as_view(),
        name="reminder-create",
    ),
    path(
        "reminders/<int:pk>/",
        views.ReminderScheduleDetailView.as_view(),
        name="reminder-detail",
    ),
    path(
        "reminders/<int:pk>/edit/",
        views.ReminderScheduleUpdateView.as_view(),
        name="reminder-update",
    ),
    path(
        "reminders/<int:pk>/delete/",
        views.ReminderScheduleDeleteView.as_view(),
        name="reminder-delete",
    ),
    path(
        "reminders/<int:pk>/send-now/",
        views.ReminderScheduleSendNowView.as_view(),
        name="reminder-send-now",
    ),
]
