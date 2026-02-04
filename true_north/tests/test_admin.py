# true_north/tests/test_admin.py

from __future__ import annotations

import pytest
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from true_north.admin import (
    CoreValueAdmin,
    GoalAdmin,
    MilestoneAdmin,
    TaskAdmin,
    GoalInline,
    MilestoneInline,
    TaskInline,
)
from true_north.models import CoreValue, Goal, Milestone, Task
from true_north.tests.factories import CustomUserFactory

pytestmark = pytest.mark.django_db


class StubAdminSite(AdminSite):
    site_header = "Stub Admin"


def _get_superuser():
    boss = CustomUserFactory(username="boss_person")
    boss.is_staff = True
    boss.is_superuser = True
    boss.save(update_fields=["is_staff", "is_superuser"])
    return boss


def test_models_are_registered_in_admin():
    assert CoreValue in admin.site._registry
    assert Goal in admin.site._registry
    assert Milestone in admin.site._registry
    assert Task in admin.site._registry


def test_corevalue_admin_configuration():
    site = StubAdminSite()
    model_admin = CoreValueAdmin(CoreValue, site)

    assert model_admin.list_display == (
        "name",
        "user",
        "is_active",
        "order",
        "created",
        "updated",
    )
    assert model_admin.list_filter == ("is_active", "user")
    assert model_admin.search_fields == ("name", "definition", "slug", "user__username")
    assert model_admin.ordering == ("order", "name")
    assert model_admin.readonly_fields == ("created", "updated")
    assert model_admin.prepopulated_fields == {"slug": ("name",)}
    assert model_admin.autocomplete_fields == ("user",)
    assert model_admin.inlines == [GoalInline]


def test_goal_admin_configuration():
    site = StubAdminSite()
    model_admin = GoalAdmin(Goal, site)

    assert model_admin.list_display == (
        "title",
        "user",
        "value",
        "status",
        "is_active",
        "order",
        "target_date",
        "created",
    )
    assert model_admin.list_filter == ("status", "is_active", "user", "value")
    assert model_admin.search_fields == (
        "title",
        "description",
        "slug",
        "value__name",
        "user__username",
    )
    assert model_admin.ordering == ("order", "title")
    assert model_admin.readonly_fields == ("created", "updated")
    assert model_admin.prepopulated_fields == {"slug": ("title",)}
    assert model_admin.autocomplete_fields == ("user", "value")
    assert model_admin.inlines == [MilestoneInline]


def test_milestone_admin_configuration():
    site = StubAdminSite()
    model_admin = MilestoneAdmin(Milestone, site)

    assert model_admin.list_display == (
        "description",
        "user",
        "goal",
        "due_date",
        "is_completed",
        "order",
        "created",
    )
    assert model_admin.list_filter == ("is_completed", "user", "goal")
    assert model_admin.search_fields == (
        "description",
        "slug",
        "notes",
        "goal__title",
        "user__username",
    )
    assert model_admin.ordering == ("order", "description")
    assert model_admin.readonly_fields == ("created", "updated")
    assert model_admin.prepopulated_fields == {"slug": ("description",)}
    assert model_admin.autocomplete_fields == ("user", "goal")
    assert model_admin.inlines == [TaskInline]


def test_task_admin_configuration():
    site = StubAdminSite()
    model_admin = TaskAdmin(Task, site)

    assert model_admin.list_display == (
        "__str__",
        "user",
        "milestone",
        "status",
        "is_completed",
        "due_date",
        "order",
        "created",
    )
    assert model_admin.list_filter == ("status", "is_completed", "user")
    assert model_admin.search_fields == (
        "content",
        "milestone__description",
        "milestone__goal__title",
        "user__username",
    )
    assert model_admin.ordering == ("order", "id")
    assert model_admin.readonly_fields == ("created", "updated")
    assert model_admin.autocomplete_fields == ("user", "milestone")


def test_inlines_point_to_expected_models_and_fields():
    assert GoalInline.model is Goal
    assert GoalInline.fields == (
        "order",
        "title",
        "slug",
        "status",
        "is_active",
        "target_date",
    )
    assert GoalInline.extra == 0
    assert GoalInline.show_change_link is True
    assert GoalInline.ordering == ("order", "title")

    assert MilestoneInline.model is Milestone
    assert MilestoneInline.fields == (
        "order",
        "description",
        "slug",
        "due_date",
        "is_completed",
    )
    assert MilestoneInline.extra == 0
    assert MilestoneInline.show_change_link is True
    assert MilestoneInline.ordering == ("order", "description")

    assert TaskInline.model is Task
    assert TaskInline.fields == (
        "order",
        "status",
        "is_completed",
        "due_date",
        "content",
    )
    assert TaskInline.extra == 0
    assert TaskInline.ordering == ("order", "id")


def test_admin_forms_build_without_error_for_superuser():
    boss = _get_superuser()
    rf = RequestFactory()
    request = rf.get("/admin/")
    request.user = boss

    site = StubAdminSite()

    corevalue_admin = CoreValueAdmin(CoreValue, site)
    goal_admin = GoalAdmin(Goal, site)
    milestone_admin = MilestoneAdmin(Milestone, site)
    task_admin = TaskAdmin(Task, site)

    assert corevalue_admin.get_form(request) is not None
    assert goal_admin.get_form(request) is not None
    assert milestone_admin.get_form(request) is not None
    assert task_admin.get_form(request) is not None
