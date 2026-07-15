"""
OMEGA DRAKON • SYSTEMS

Teste:
Validação de ciclos em DAG.
"""

import pytest

from core.workflows.models import (
    Workflow,
    WorkflowStep,
)
from core.workflows.scheduler import (
    WorkflowScheduler,
)


def test_graph_cycle_detection():

    workflow = Workflow(
        workflow_id="cycle_test",
        name="Cycle Test",
        steps=[
            WorkflowStep(
                step_id="a",
                action_name="a",
                dependencies=["c"],
            ),
            WorkflowStep(
                step_id="b",
                action_name="b",
                dependencies=["a"],
            ),
            WorkflowStep(
                step_id="c",
                action_name="c",
                dependencies=["b"],
            ),
        ],
    )

    scheduler = WorkflowScheduler(
        workflow
    )

    with pytest.raises(
        ValueError,
        match="Workflow DAG possui ciclos"
    ):
        scheduler.validate()
