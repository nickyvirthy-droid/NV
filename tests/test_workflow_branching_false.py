import pytest

from core.runtime.kernel import (
    RuntimeKernel
)
from core.workflows.models import (
    Workflow,
    WorkflowStep
)


@pytest.mark.anyio
async def test_workflow_branching_false():

    kernel = RuntimeKernel()

    workflow = Workflow(
        workflow_id="branch_test_false",
        name="Branch Test False",
        steps=[
            WorkflowStep(
                step_id="start",
                action_name="system_info",
                condition_path="False",
                if_true_next="cpu",
                if_false_next="memory"
            ),
            WorkflowStep(
                step_id="cpu",
                action_name="cpu_info"
            ),
            WorkflowStep(
                step_id="memory",
                action_name="memory_usage"
            )
        ]
    )

    kernel.workflows.register(
        workflow
    )

    execution = await (
        kernel.workflows.execute(
            "branch_test_false"
        )
    )

    assert (
        "start"
        in execution.results
    )

    assert (
        "cpu"
        not in execution.results
    )

    assert (
        "memory"
        in execution.results
    )
