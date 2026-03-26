# true_north/urls.py

from django.urls import path

from true_north import views

app_name = "true_north"
urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    # CoreValue CRUD
    path(
        "core-values/",
        views.CoreValueListView.as_view(),
        name="core-value-list",
    ),
    path(
        "core-values/create/",
        views.CoreValueCreateView.as_view(),
        name="core-value-create",
    ),
    path(
        "core-values/<int:pk>/update/",
        views.CoreValueUpdateView.as_view(),
        name="core-value-update",
    ),
    path(
        "core-values/<int:pk>/delete/",
        views.CoreValueDeleteView.as_view(),
        name="core-value-delete",
    ),
    # Goal CRUD
    path(
        "goals/",
        views.GoalListView.as_view(),
        name="goal-list",
    ),
    path(
        "goals/create/",
        views.GoalCreateView.as_view(),
        name="goal-create",
    ),
    path(
        "goals/<int:pk>/update/",
        views.GoalUpdateView.as_view(),
        name="goal-update",
    ),
    path(
        "goals/<int:pk>/delete/",
        views.GoalDeleteView.as_view(),
        name="goal-delete",
    ),
    # Milestone CRUD
    path(
        "milestones/",
        views.MilestoneListView.as_view(),
        name="milestone-list",
    ),
    path(
        "milestones/create/",
        views.MilestoneCreateView.as_view(),
        name="milestone-create",
    ),
    path(
        "milestones/<int:pk>/update/",
        views.MilestoneUpdateView.as_view(),
        name="milestone-update",
    ),
    path(
        "milestones/<int:pk>/delete/",
        views.MilestoneDeleteView.as_view(),
        name="milestone-delete",
    ),
    # ValueAction CRUD
    path(
        "value-actions/",
        views.ValueActionListView.as_view(),
        name="value-action-list",
    ),
    path(
        "value-actions/create/",
        views.ValueActionCreateView.as_view(),
        name="value-action-create",
    ),
    path(
        "value-actions/<int:pk>/update/",
        views.ValueActionUpdateView.as_view(),
        name="value-action-update",
    ),
    path(
        "value-actions/<int:pk>/delete/",
        views.ValueActionDeleteView.as_view(),
        name="value-action-delete",
    ),
    # Send-email actions
    path(
        "core-values/<int:pk>/send-email/",
        views.CoreValueSendEmailView.as_view(),
        name="core-value-send-email",
    ),
    path(
        "goals/<int:pk>/send-email/",
        views.GoalSendEmailView.as_view(),
        name="goal-send-email",
    ),
    path(
        "milestones/<int:pk>/send-email/",
        views.MilestoneSendEmailView.as_view(),
        name="milestone-send-email",
    ),
    path(
        "value-actions/<int:pk>/send-email/",
        views.ValueActionSendEmailView.as_view(),
        name="value-action-send-email",
    ),
]
