# projects/tests/test_models.py

import pytest

from assets.models import Project
from projects.models import Milestone, ProjectLog, ProjectTask


@pytest.mark.django_db
def test_milestone_projecttask_projectlog_smoke(workspace, user):
    proj = Project.objects.create(
        workspace=workspace,
        name="Bird Cam",
        description="",
        slug="bird-cam",
    )

    ms = Milestone.objects.create(
        workspace=workspace,
        project=proj,
        name="M1",
        description="",
        order=1,
    )
    assert ms.project == proj
    assert ms.workspace == workspace

    t = ProjectTask.objects.create(
        workspace=workspace,
        project=proj,
        milestone=ms,
        title="T1",
        description="",
        status="backlog",
        assigned_to=user,
        effort_points=3,
    )
    assert t.status == "backlog"
    assert t.milestone == ms

    t2 = ProjectTask.objects.create(
        workspace=workspace,
        project=proj,
        milestone=None,
        title="No milestone",
        description="",
    )
    assert t2.status == "backlog"
    assert t2.milestone is None

    log = ProjectLog.objects.create(
        workspace=workspace,
        project=proj,
        created_by=user,
        summary="Did a thing",
        detail="More details",
    )
    assert log.happened_at is not None
    assert log.summary == "Did a thing"
