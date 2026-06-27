import pytest

from core.runtime.kernel import (
    RuntimeKernel
)
from core.workflows.models import (
    Workflow,
    WorkflowStep
)


@pytest.mark.anyio
async def test_workflow_branching():

    kernel = RuntimeKernel()

    workflow = Workflow(
        workflow_id="branch_test",
        name="Branch Test",
        steps=[
            WorkflowStep(
                step_id="start",
                action_name="system_info",
                condition_path="True",
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
            "branch_test"
        )
    )

    assert (
        "start"
        in execution.results
    )

    assert (
        "cpu"
        in execution.results
    )

    assert (
        "memory"
        not in execution.results
    )
