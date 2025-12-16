# assets/tests/test_admin.py

from datetime import datetime, timedelta

import pytest
from django.contrib import admin as dj_admin
from django.test import RequestFactory
from django.utils import timezone

from assets.admin import (
    ApplicationAdmin,
    AssetAdmin,
    FormFactorAdmin,
    OSAdmin,
    ProjectAdmin,
)
from assets.models import Application, Asset, FormFactor, OS, Project
from work.admin import ActivityInstanceInline, WorkOrderInline
from work.models import MaintenanceTask, WorkOrder


@pytest.mark.parametrize("model", [FormFactor, OS, Application, Project, Asset])
def test_assets_models_are_registered_in_admin(model):
    # Registered via @admin.register(...) :contentReference[oaicite:4]{index=4}
    assert model in dj_admin.site._registry


def test_form_factor_admin_configuration():
    ma = FormFactorAdmin(FormFactor, dj_admin.site)
    assert ma.list_display == ("name", "slug")
    assert ma.search_fields == ("name",)
    assert ma.prepopulated_fields == {"slug": ("name",)}


def test_os_admin_configuration():
    ma = OSAdmin(OS, dj_admin.site)
    assert ma.list_display == ("name", "version", "slug")
    assert ma.search_fields == ("name", "version")
    assert ma.list_filter == ("name",)
    assert ma.prepopulated_fields == {"slug": ("name",)}


def test_application_admin_configuration():
    ma = ApplicationAdmin(Application, dj_admin.site)
    assert ma.list_display == ("name", "version", "slug")
    assert ma.search_fields == ("name", "version")
    assert ma.prepopulated_fields == {"slug": ("name",)}


def test_project_admin_configuration():
    ma = ProjectAdmin(Project, dj_admin.site)
    assert ma.list_display == ("name", "workspace", "slug")
    assert ma.search_fields == ("name", "description", "slug")
    assert ma.list_filter == ("workspace",)
    assert ma.prepopulated_fields == {"slug": ("name",)}
    assert ma.autocomplete_fields == ("workspace",)
    assert ma.ordering == ("workspace", "name")


def test_asset_admin_configuration_matches_current_code():
    ma = AssetAdmin(Asset, dj_admin.site)

    assert ma.list_display == (
        "name",
        "workspace",
        "primary_project",
        "projects_summary",
        "kind",
        "form_factor",
        "os",
        "location",
        "purchase_date",
        "warranty_expires",
        "warranty_status",
        "next_due_status",
    )  # :contentReference[oaicite:5]{index=5}

    # filters (including M2M projects + applications)
    for field in (
        "workspace",
        "kind",
        "form_factor",
        "os",
        "applications",
        "projects",
        "location",
        "purchase_date",
        "warranty_expires",
    ):
        assert field in ma.list_filter  # :contentReference[oaicite:6]{index=6}

    # search fields
    for field in (
        "name",
        "location",
        "notes",
        "workspace__name",
        "primary_project__name",
        "projects__name",
    ):
        assert field in ma.search_fields  # :contentReference[oaicite:7]{index=7}

    assert ma.autocomplete_fields == (
        "workspace",
        "primary_project",
        "projects",
        "form_factor",
        "os",
        "applications",
    )  # :contentReference[oaicite:8]{index=8}

    assert ma.date_hierarchy == "purchase_date"
    assert ma.list_select_related == (
        "workspace",
        "primary_project",
        "form_factor",
        "os",
    )  # noqa E501
    assert ma.ordering == ("workspace", "name")

    assert WorkOrderInline in ma.inlines
    assert ActivityInstanceInline in ma.inlines


@pytest.mark.django_db
def test_projects_summary_variants(workspace):
    ma = AssetAdmin(Asset, dj_admin.site)

    p1 = Project.objects.create(
        workspace=workspace, name="P1", description="", slug="p1"
    )  # noqa E501
    p2 = Project.objects.create(
        workspace=workspace, name="P2", description="", slug="p2"
    )  # noqa E501
    p3 = Project.objects.create(
        workspace=workspace, name="P3", description="", slug="p3"
    )  # noqa E501
    p4 = Project.objects.create(
        workspace=workspace, name="P4", description="", slug="p4"
    )  # noqa E501

    asset = Asset.objects.create(workspace=workspace, name="A", kind="PI")

    # none
    assert ma.projects_summary(asset) == "—"  # :contentReference[oaicite:9]{index=9}

    # 2 names
    asset.projects.add(p1, p2)
    assert ma.projects_summary(asset) == "P1, P2"

    # 4 names => only 3 shown + suffix
    asset.projects.add(p3, p4)
    summary = ma.projects_summary(asset)
    assert summary.startswith("P1, P2, P3")
    assert "(+1)" in summary


@pytest.mark.django_db
def test_get_search_results_forces_distinct(workspace):
    """
    AssetAdmin.get_search_results always returns use_distinct=True. :contentReference[oaicite:10]{index=10}  # noqa E501
    """
    ma = AssetAdmin(Asset, dj_admin.site)
    rf = RequestFactory()
    request = rf.get("/admin/assets/asset/")

    # Minimal data so queryset isn't empty
    Asset.objects.create(workspace=workspace, name="SearchMe", kind="PI")

    qs, use_distinct = ma.get_search_results(request, Asset.objects.all(), "SearchMe")
    assert use_distinct is True
    assert qs.exists()


@pytest.mark.django_db
def test_warranty_status_variants(monkeypatch, workspace):
    """
    warranty_status branches: n/a, Expired, Expiring soon, Active. :contentReference[oaicite:11]{index=11}  # noqa E501
    """
    fixed_now = datetime(2025, 1, 1, 10, 0, tzinfo=timezone.get_current_timezone())
    monkeypatch.setattr("assets.admin.timezone.now", lambda: fixed_now)

    ma = AssetAdmin(Asset, dj_admin.site)

    no_warranty = Asset.objects.create(workspace=workspace, name="NW", kind="PI")
    assert ma.warranty_status(no_warranty) == "n/a"

    expired = Asset.objects.create(
        workspace=workspace,
        name="E",
        kind="PI",
        warranty_expires=fixed_now.date() - timedelta(days=1),
    )
    assert ma.warranty_status(expired) == "Expired"

    soon = Asset.objects.create(
        workspace=workspace,
        name="S",
        kind="PI",
        warranty_expires=fixed_now.date() + timedelta(days=7),
    )
    assert ma.warranty_status(soon) == "Expiring soon"

    active = Asset.objects.create(
        workspace=workspace,
        name="A",
        kind="PI",
        warranty_expires=fixed_now.date() + timedelta(days=60),
    )
    assert ma.warranty_status(active) == "Active"


@pytest.mark.django_db
def test_next_due_status_variants(monkeypatch, workspace):
    """
    next_due_status branches: No open work, Overdue, Due today, Due soon, Scheduled. :contentReference[oaicite:12]{index=12}  # noqa E501
    """
    fixed_now = datetime(2025, 1, 1, 10, 0, tzinfo=timezone.get_current_timezone())
    monkeypatch.setattr("assets.admin.timezone.now", lambda: fixed_now)

    ma = AssetAdmin(Asset, dj_admin.site)
    asset = Asset.objects.create(workspace=workspace, name="Asset", kind="PI")
    task = MaintenanceTask.objects.create(
        workspace=workspace, name="Task", cadence="monthly"
    )  # noqa E501

    assert ma.next_due_status(asset) == "No open work"

    # Overdue
    wo1 = WorkOrder.objects.create(
        workspace=workspace,
        asset=asset,
        task=task,
        due=fixed_now - timedelta(days=1),
        status="open",
    )
    assert ma.next_due_status(asset) == "Overdue"

    # Due today (open one is today)
    wo1.status = "done"
    wo1.save()
    wo2 = WorkOrder.objects.create(
        workspace=workspace,
        asset=asset,
        task=task,
        due=fixed_now + timedelta(hours=2),
        status="open",
    )
    assert ma.next_due_status(asset) == "Due today"

    # Due soon (<= 7 days)
    wo2.status = "done"
    wo2.save()
    wo3 = WorkOrder.objects.create(
        workspace=workspace,
        asset=asset,
        task=task,
        due=fixed_now + timedelta(days=3),
        status="open",
    )
    assert ma.next_due_status(asset) == "Due soon"

    # Scheduled (> 7 days)
    wo3.status = "done"
    wo3.save()
    WorkOrder.objects.create(
        workspace=workspace,
        asset=asset,
        task=task,
        due=fixed_now + timedelta(days=10),
        status="open",
    )
    assert ma.next_due_status(asset) == "Scheduled"
