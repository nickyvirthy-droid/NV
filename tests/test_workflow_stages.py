"""
OMEGA DRAKON • SYSTEMS
Teste: Construção de estágios (topological stages)
"""

from core.workflows.models import Workflow, WorkflowStep
from core.workflows.scheduler import WorkflowScheduler


def test_build_stages_basic():
    workflow = Workflow(
        workflow_id="stage_test",
        name="Stage Test",
        steps=[
            WorkflowStep(step_id="extract", action_name="extract"),
            WorkflowStep(step_id="a", action_name="a", dependencies=["extract"]),
            WorkflowStep(step_id="b", action_name="b", dependencies=["extract"]),
            WorkflowStep(step_id="save", action_name="save", dependencies=["a", "b"]),
        ],
    )

    scheduler = WorkflowScheduler(workflow)
    stages = scheduler.build_stages()

    assert len(stages) == 3
    assert stages[0] == ["extract"]
    assert set(stages[1]) == {"a", "b"}
    assert stages[2] == ["save"]


def test_build_stages_linear():
    workflow = Workflow(
        workflow_id="linear",
        name="Linear",
        steps=[
            WorkflowStep(step_id="s1", action_name="s1"),
            WorkflowStep(step_id="s2", action_name="s2", dependencies=["s1"]),
            WorkflowStep(step_id="s3", action_name="s3", dependencies=["s2"]),
        ],
    )

    stages = WorkflowScheduler(workflow).build_stages()

    assert len(stages) == 3
    assert stages[0] == ["s1"]
    assert stages[1] == ["s2"]
    assert stages[2] == ["s3"]


def test_build_stages_no_dependencies():
    workflow = Workflow(
        workflow_id="parallel_only",
        name="Parallel Only",
        steps=[
            WorkflowStep(step_id="x", action_name="x"),
            WorkflowStep(step_id="y", action_name="y"),
            WorkflowStep(step_id="z", action_name="z"),
        ],
    )

    stages = WorkflowScheduler(workflow).build_stages()

    assert len(stages) == 1
    assert set(stages[0]) == {"x", "y", "z"}
