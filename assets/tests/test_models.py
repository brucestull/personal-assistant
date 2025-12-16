# assets/tests/test_models.py

from datetime import date, timedelta

import pytest
from django.db import IntegrityError, transaction

from assets.models import Application, Asset, FormFactor, OS, Project


@pytest.mark.django_db
def test_form_factor_str_and_uniqueness():
    ff = FormFactor.objects.create(name="Mini PC", slug="mini-pc")
    assert str(ff) == "Mini PC"

    # name unique
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            FormFactor.objects.create(name="Mini PC", slug="mini-pc-2")

    # slug unique
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            FormFactor.objects.create(name="Mini PC 2", slug="mini-pc")


@pytest.mark.django_db
def test_os_str_variants_and_slug_unique():
    os1 = OS.objects.create(name="Ubuntu", version="24.04", slug="ubuntu-24-04")
    assert str(os1) == "Ubuntu 24.04"

    os2 = OS.objects.create(name="Debian", version="", slug="debian")
    assert str(os2) == "Debian"

    # slug unique
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            OS.objects.create(name="Ubuntu", version="22.04", slug="ubuntu-24-04")

    # plural name exists (sanity)
    assert OS._meta.verbose_name_plural == "Operating Systems"


@pytest.mark.django_db
def test_application_str_variants_and_slug_unique():
    a1 = Application.objects.create(name="Docker", version="27", slug="docker-27")
    assert str(a1) == "Docker 27"

    a2 = Application.objects.create(name="Prometheus", version="", slug="prometheus")
    assert str(a2) == "Prometheus"

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Application.objects.create(name="Docker", version="28", slug="docker-27")


@pytest.mark.django_db
def test_project_defaults_and_unique_per_workspace(workspace, another_workspace):
    p1 = Project.objects.create(
        workspace=workspace,
        name="Homelab",
        description="Infra",
        slug="homelab",
    )

    # defaults
    assert p1.status == "inbox"
    assert p1.priority == "med"
    assert p1.parent is None
    assert p1.outcome == ""
    assert p1.next_action == ""
    assert p1.target_date is None
    assert p1.archived_at is None

    # unique_together (workspace, slug)
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Project.objects.create(
                workspace=workspace,
                name="Homelab duplicate",
                description="Dup",
                slug="homelab",
            )

    # same slug allowed in different workspace
    p2 = Project.objects.create(
        workspace=another_workspace,
        name="Homelab (other ws)",
        description="OK",
        slug="homelab",
    )
    assert p2.pk is not None

    # parent hierarchy allowed
    child = Project.objects.create(
        workspace=workspace,
        name="Bird Cam",
        description="Subproject",
        slug="bird-cam",
        parent=p1,
    )
    assert child.parent_id == p1.id


@pytest.mark.django_db
def test_asset_str_uses_kind_display_and_workspace(workspace):
    """
    Asset.__str__ uses KIND_CHOICES display name when possible and falls back
    to raw value otherwise. :contentReference[oaicite:3]{index=3}
    """
    asset = Asset.objects.create(workspace=workspace, name="Remote Lamp", kind="PI")
    assert str(asset) == f"Remote Lamp (Raspberry Pi) @ {workspace}"

    # fallback: DB doesn't enforce choices, so an unknown kind still renders
    weird = Asset.objects.create(workspace=workspace, name="Mystery", kind="ZZZ")
    assert str(weird) == f"Mystery (ZZZ) @ {workspace}"


@pytest.mark.django_db
def test_asset_relations_primary_project_projects_and_applications(workspace):
    ff = FormFactor.objects.create(name="Pi 4", slug="pi-4")
    os_obj = OS.objects.create(name="Raspberry Pi OS", version="11", slug="rpi-os-11")
    app1 = Application.objects.create(name="Docker", version="", slug="docker")
    app2 = Application.objects.create(name="Node", version="20", slug="node-20")

    p_primary = Project.objects.create(
        workspace=workspace,
        name="Homelab",
        description="Infra",
        slug="homelab",
    )
    p2 = Project.objects.create(
        workspace=workspace,
        name="Monitoring",
        description="Stack",
        slug="monitoring",
    )

    asset = Asset.objects.create(
        workspace=workspace,
        primary_project=p_primary,
        name="PI-SERVER",
        kind="PI",
        form_factor=ff,
        os=os_obj,
        location="Rack 1",
        notes="Hello",
        purchase_date=date.today(),
        warranty_expires=date.today() + timedelta(days=90),
    )

    # M2M
    asset.projects.add(p_primary, p2)
    asset.applications.add(app1, app2)

    asset.refresh_from_db()
    assert asset.primary_project == p_primary
    assert set(asset.projects.all()) == {p_primary, p2}
    assert set(asset.applications.all()) == {app1, app2}


@pytest.mark.django_db
def test_asset_optional_fields_can_be_null_or_blank(workspace):
    asset = Asset.objects.create(
        workspace=workspace,
        primary_project=None,
        name="Bare Asset",
        kind="SRV",
        form_factor=None,
        os=None,
        location="",
        purchase_date=None,
        warranty_expires=None,
        notes="",
    )

    assert asset.primary_project is None
    assert asset.form_factor is None
    assert asset.os is None
    assert asset.location == ""
    assert asset.purchase_date is None
    assert asset.warranty_expires is None
    assert asset.notes == ""
