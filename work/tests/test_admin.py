# work/tests/test_admin.py

from datetime import timedelta

import pytest
from django.contrib import admin as dj_admin
from django.test import RequestFactory
from django.utils import timezone

from assets.models import Asset
from work.admin import (
    ActivityInstanceAdmin,
    ActivityInstanceInline,
    DueWindowFilter,
    MaintenanceTaskAdmin,
    WorkOrderAdmin,
    WorkOrderInline,
)
from work.models import ActivityInstance, MaintenanceTask, WorkOrder


@pytest.mark.parametrize("model", [MaintenanceTask, WorkOrder, ActivityInstance])
def test_work_models_are_registered_in_admin(model):
    assert model in dj_admin.site._registry


def test_workorder_inline_configuration():
    inline = WorkOrderInline(MaintenanceTask, dj_admin.site)
    assert inline.model is WorkOrder
    assert inline.extra == 0
    assert inline.autocomplete_fields == ("asset", "assigned_to", "requested_by")
    assert inline.raw_id_fields == ()


def test_activityinstance_inline_configuration():
    inline = ActivityInstanceInline(WorkOrder, dj_admin.site)
    assert inline.model is ActivityInstance
    assert inline.extra == 0
    assert inline.raw_id_fields == ("asset", "performed_by")
    assert inline.autocomplete_fields == ("asset", "performed_by")
    assert inline.ordering == ("-occurred_at",)


def test_maintenance_task_admin_configuration():
    ma = MaintenanceTaskAdmin(MaintenanceTask, dj_admin.site)
    assert ma.list_display == ("name", "workspace", "cadence")
    assert ma.list_filter == ("workspace", "cadence")
    for field in ("name", "description", "workspace__name"):
        assert field in ma.search_fields
    assert ma.autocomplete_fields == ("workspace",)
    assert ma.raw_id_fields == ()
    assert ma.ordering == ("workspace", "name")
    assert WorkOrderInline in ma.inlines
    assert "id" in ma.readonly_fields
    assert "generate_preview" in set(ma.actions)


@pytest.mark.django_db
def test_generate_preview_action_noop(workspace):
    MaintenanceTask.objects.create(workspace=workspace, name="Task", cadence="monthly")
    ma = MaintenanceTaskAdmin(MaintenanceTask, dj_admin.site)
    ma.generate_preview(request=None, queryset=MaintenanceTask.objects.all())


def test_work_order_admin_configuration():
    ma = WorkOrderAdmin(WorkOrder, dj_admin.site)

    assert ma.date_hierarchy == "due"
    assert DueWindowFilter in ma.list_filter

    # second declaration wins in your admin file, so workspace is NOT included
    assert ma.autocomplete_fields == ("asset", "task", "assigned_to", "requested_by")
    assert ma.raw_id_fields == ()

    assert {"mark_open", "mark_done", "mark_cancelled"} <= set(ma.actions)
    assert "id" in ma.readonly_fields


@pytest.mark.django_db
def test_mark_actions(workspace, user):
    asset = Asset.objects.create(workspace=workspace, name="A", kind="PI")
    task = MaintenanceTask.objects.create(workspace=workspace, name="T", cadence="weekly")

    wo = WorkOrder.objects.create(
        workspace=workspace,
        asset=asset,
        task=task,
        due=timezone.now(),
        status="open",
    )

    ma = WorkOrderAdmin(WorkOrder, dj_admin.site)
    qs = WorkOrder.objects.filter(pk=wo.pk)

    ma.mark_done(request=None, queryset=qs)
    wo.refresh_from_db()
    assert wo.status == "done"

    ma.mark_cancelled(request=None, queryset=qs)
    wo.refresh_from_db()
    assert wo.status == "cancelled"

    ma.mark_open(request=None, queryset=qs)
    wo.refresh_from_db()
    assert wo.status == "open"


@pytest.mark.django_db
def test_due_window_filter_querysets(workspace):
    asset = Asset.objects.create(workspace=workspace, name="A", kind="PI")
    task = MaintenanceTask.objects.create(workspace=workspace, name="T", cadence="weekly")

    now = timezone.now()

    overdue = WorkOrder.objects.create(workspace=workspace, asset=asset, task=task, due=now - timedelta(days=1))
    next_7 = WorkOrder.objects.create(workspace=workspace, asset=asset, task=task, due=now + timedelta(days=3))
    next_30 = WorkOrder.objects.create(workspace=workspace, asset=asset, task=task, due=now + timedelta(days=15))
    future = WorkOrder.objects.create(workspace=workspace, asset=asset, task=task, due=now + timedelta(days=40))

    rf = RequestFactory()
    base_qs = WorkOrder.objects.all()
    model_admin = WorkOrderAdmin(WorkOrder, dj_admin.site)

    def run_filter(value):
        request = rf.get("/admin/work/workorder/", {"due_window": value})
        params = request.GET.copy()
        flt = DueWindowFilter(request, params, WorkOrder, model_admin)
        return flt.queryset(request, base_qs)

    assert list(run_filter("overdue")) == [overdue]
    assert list(run_filter("next_7_days")) == [next_7]
    assert list(run_filter("next_30_days")) == [next_30]
    assert list(run_filter("future")) == [future]

    # empty / unknown returns unfiltered queryset
    assert run_filter(None).count() == base_qs.count()
    assert list(run_filter("wat")) == list(base_qs)


def test_activity_instance_admin_configuration():
    ma = ActivityInstanceAdmin(ActivityInstance, dj_admin.site)
    assert "id" in ma.readonly_fields
    assert ma.autocomplete_fields == ("workspace", "asset", "work_order", "performed_by")
