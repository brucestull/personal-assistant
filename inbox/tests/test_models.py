# inbox/tests/test_models.py

import pytest

from inbox.models import InboxItem
from assets.models import Asset, Project


@pytest.mark.django_db
def test_inbox_item_defaults_and_optional_links(workspace, user):
    item = InboxItem.objects.create(workspace=workspace, created_by=user, title="Hello")
    assert item.kind == "idea"
    assert item.status == "new"
    assert item.detail == ""
    assert item.project is None
    assert item.asset is None

    project = Project.objects.create(
        workspace=workspace,
        name="Homelab",
        description="",
        slug="homelab",
    )
    asset = Asset.objects.create(workspace=workspace, name="PI-1", kind="PI")

    item2 = InboxItem.objects.create(
        workspace=workspace,
        title="Linky",
        kind="todo",
        status="triaged",
        project=project,
        asset=asset,
        detail="Details",
    )
    assert item2.kind == "todo"
    assert item2.status == "triaged"
    assert item2.project == project
    assert item2.asset == asset
    assert item2.detail == "Details"
