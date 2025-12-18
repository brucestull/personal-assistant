from django.urls import path

from . import views

app_name = "priority_deciderator"

urlpatterns = [
    # Dashboard
    path("", views.ReminderDashboardView.as_view(), name="dashboard"),
    # Reminder CRUD
    path("reminders/", views.ReminderListView.as_view(), name="reminder_list"),
    path("reminders/new/", views.ReminderCreateView.as_view(), name="reminder_create"),
    path(
        "reminders/<int:pk>/",
        views.ReminderDetailView.as_view(),
        name="reminder_detail",
    ),
    path(
        "reminders/<int:pk>/edit/",
        views.ReminderUpdateView.as_view(),
        name="reminder_update",
    ),
    path(
        "reminders/<int:pk>/delete/",
        views.ReminderDeleteView.as_view(),
        name="reminder_delete",
    ),
    # Schedule management
    path(
        "reminders/<int:reminder_pk>/schedule/new/",
        views.schedule_create,
        name="schedule_create",
    ),
    path("schedules/<int:pk>/edit/", views.schedule_update, name="schedule_update"),
    path("schedules/<int:pk>/delete/", views.schedule_delete, name="schedule_delete"),
]
