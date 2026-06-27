import pytest

from core.runtime.kernel import (
    RuntimeKernel
)
from core.workflows.models import (
    Workflow,
    WorkflowStep
)


@pytest.mark.anyio
async def test_workflow_condition():

    kernel = RuntimeKernel()

    workflow = Workflow(
        workflow_id="condition_test",
        name="Condition Test",
        steps=[
            WorkflowStep(
                step_id="system",
                action_name="system_info"
            ),
            WorkflowStep(
                step_id="cpu",
                action_name="cpu_info",
                condition_path="True"
            )
        ]
    )

    kernel.workflows.register(
        workflow
    )

    execution = await (
        kernel.workflows.execute(
            "condition_test"
        )
    )

    assert (
        "system"
        in execution.results
    )

    assert (
        "cpu"
        in execution.results
    )
