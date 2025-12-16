# work/tests/test_models.py

import pytest
from django.db.models.deletion import ProtectedError
from django.db import IntegrityError, transaction
from django.utils import timezone

from assets.models import Application, Asset, FormFactor, OS, Project
from work.models import ActivityInstance, MaintenanceTask, WorkOrder


def _create_asset(workspace):
    ff = FormFactor.objects.create(name="Pi 4", slug="pi-4")
    os_obj = OS.objects.create(name="Raspberry Pi OS", version="11", slug="rpi-os-11")
    app = Application.objects.create(name="Docker", version="", slug="docker")

    project = Project.objects.create(
        workspace=workspace,
        name="Monitoring",
        description="Monitoring stack",
        slug="monitoring",
    )

    asset = Asset.objects.create(
        workspace=workspace,
        primary_project=project,
        name="PI-001",
        kind="PI",
        form_factor=ff,
        os=os_obj,
        location="Rack 1",
    )
    asset.projects.add(project)
    asset.applications.add(app)
    return asset


@pytest.mark.django_db
def test_maintenance_task_unique_per_workspace(workspace, another_workspace):
    MaintenanceTask.objects.create(
        workspace=workspace,
        name="Patch OS",
        cadence="monthly",
        description="Monthly OS patching",
    )

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            MaintenanceTask.objects.create(
                workspace=workspace,
                name="Patch OS",
                cadence="weekly",
                description="Dup name in same workspace",
            )

    ok = MaintenanceTask.objects.create(
        workspace=another_workspace,
        name="Patch OS",
        cadence="monthly",
        description="Same name, different workspace",
    )
    assert ok.pk is not None


@pytest.mark.django_db
def test_maintenance_task_threshold_json_optional_and_persisted(workspace):
    task = MaintenanceTask.objects.create(
        workspace=workspace,
        name="Backup verify",
        cadence="weekly",
        description="Verify backups",
    )
    assert task.threshold_json == {} or task.threshold_json is None

    thresholds = {"max_days_overdue": 7, "window": "30d"}
    task2 = MaintenanceTask.objects.create(
        workspace=workspace,
        name="Patch OS thresholds",
        cadence="monthly",
        description="Has thresholds",
        threshold_json=thresholds,
    )
    task2.refresh_from_db()
    assert task2.threshold_json == thresholds


@pytest.mark.django_db
def test_str_methods(workspace, user):
    asset = _create_asset(workspace)
    task = MaintenanceTask.objects.create(
        workspace=workspace,
        name="Reboot",
        cadence="monthly",
        description="Monthly reboot",
    )
    assert str(task) == f"Reboot ({workspace}, monthly)"

    wo = WorkOrder.objects.create(
        workspace=workspace,
        asset=asset,
        task=task,
        due=timezone.now(),
        status="open",
        assigned_to=user,
    )
    s = str(wo)
    assert "Reboot" in s
    assert "→" in s
    assert "[open]" in s

    act = ActivityInstance.objects.create(
        workspace=workspace,
        work_order=wo,
        asset=asset,
        kind="checked",
        note="Checked",
        occurred_at=timezone.now(),
        performed_by=user,
    )
    act_str = str(act)
    assert "Checked" in act_str
    assert asset.name in act_str  # includes asset.__str__ in formatting


@pytest.mark.django_db
def test_workorder_default_status_open(workspace, user):
    asset = _create_asset(workspace)
    task = MaintenanceTask.objects.create(
        workspace=workspace,
        name="Backup verify",
        cadence="weekly",
        description="Verify backups",
    )

    wo = WorkOrder.objects.create(
        workspace=workspace,
        asset=asset,
        task=task,
        due=timezone.now(),
        assigned_to=user,
    )
    assert wo.status == "open"
    assert wo.requested_by is None


@pytest.mark.django_db
def test_workorder_cascade_on_asset_delete(workspace):
    asset = _create_asset(workspace)
    task = MaintenanceTask.objects.create(
        workspace=workspace,
        name="Test Task",
        cadence="weekly",
        description="Just a test",
    )
    wo = WorkOrder.objects.create(
        workspace=workspace,
        asset=asset,
        task=task,
        due=timezone.now(),
    )
    assert WorkOrder.objects.filter(pk=wo.pk).exists()
    asset.delete()
    assert not WorkOrder.objects.filter(pk=wo.pk).exists()


@pytest.mark.django_db
def test_activityinstance_set_null_on_workorder_delete(workspace):
    asset = _create_asset(workspace)
    task = MaintenanceTask.objects.create(
        workspace=workspace,
        name="Test Task",
        cadence="weekly",
        description="Just a test",
    )
    wo = WorkOrder.objects.create(
        workspace=workspace,
        asset=asset,
        task=task,
        due=timezone.now(),
    )
    act = ActivityInstance.objects.create(
        workspace=workspace,
        work_order=wo,
        asset=asset,
        kind="patched",
        note="Patched",
        occurred_at=timezone.now(),
    )

    wo.delete()
    act.refresh_from_db()
    assert act.work_order is None


@pytest.mark.django_db
def test_task_is_protected_if_workorder_exists(workspace):
    asset = _create_asset(workspace)
    task = MaintenanceTask.objects.create(
        workspace=workspace,
        name="Protected Task",
        cadence="weekly",
        description="",
    )
    WorkOrder.objects.create(
        workspace=workspace,
        asset=asset,
        task=task,
        due=timezone.now(),
    )

    with pytest.raises(ProtectedError):
        task.delete()
