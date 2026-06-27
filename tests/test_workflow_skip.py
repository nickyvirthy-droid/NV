import pytest

from core.runtime.kernel import (
    RuntimeKernel
)
from core.workflows.models import (
    Workflow,
    WorkflowStep
)


@pytest.mark.anyio
async def test_workflow_skip():

    kernel = RuntimeKernel()

    workflow = Workflow(
        workflow_id="skip_test",
        name="Skip Test",
        steps=[
            WorkflowStep(
                step_id="system",
                action_name="system_info"
            ),
            WorkflowStep(
                step_id="cpu",
                action_name="cpu_info",
                condition_path="False"
            )
        ]
    )

    kernel.workflows.register(
        workflow
    )

    execution = await (
        kernel.workflows.execute(
            "skip_test"
        )
    )

    assert (
        "system"
        in execution.results
    )

    assert (
        "cpu"
        not in execution.results
    )
