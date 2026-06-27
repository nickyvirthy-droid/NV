import asyncio
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


class SlowAction(
    BaseAction
):

    name = "slow_action"

    description = (
        "Action lenta."
    )

    async def execute(
        self,
        context,
        payload
    ):

        await asyncio.sleep(2)

        return {
            "success": True
        }


@pytest.mark.anyio
async def test_workflow_timeout():

    kernel = RuntimeKernel()

    kernel.actions.registry.register(
        SlowAction()
    )

    workflow = Workflow(
        workflow_id="timeout_test",
        name="Timeout Test",
        steps=[
            WorkflowStep(
                step_id="slow",
                action_name="slow_action",
                timeout=0.5
            )
        ]
    )

    kernel.workflows.register(
        workflow
    )

    with pytest.raises(
        asyncio.TimeoutError
    ):

        await kernel.workflows.execute(
            "timeout_test"
        )
