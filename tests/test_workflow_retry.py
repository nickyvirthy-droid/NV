import pytest

from core.runtime.kernel import (
    RuntimeKernel
)

from core.actions.base import (
    BaseAction
)

from core.workflows.models import (
    Workflow,
    WorkflowStep
)


class RetryAction(
    BaseAction
):

    name = "retry_action"

    description = (
        "Action que falha duas vezes."
    )

    def __init__(self):

        self.counter = 0

    async def execute(
        self,
        context,
        payload
    ):

        self.counter += 1

        if self.counter < 3:

            raise RuntimeError(
                "temporary failure"
            )

        return {
            "success": True
        }


@pytest.mark.anyio
async def test_workflow_retry():

    kernel = RuntimeKernel()

    action = RetryAction()

    kernel.actions.registry.register(
        action
    )

    workflow = Workflow(
        workflow_id="retry_test",
        name="Retry Test",
        steps=[
            WorkflowStep(
                step_id="retry",
                action_name="retry_action",
                retry_count=3,
                retry_delay=0
            )
        ]
    )

    kernel.workflows.register(
        workflow
    )

    execution = await (
        kernel.workflows.execute(
            "retry_test"
        )
    )

    assert (
        execution.status
        == "COMPLETED"
    )

    assert (
        execution.results[
            "retry"
        ]["success"]
        is True
    )

    assert (
        action.counter
        == 3
    )
