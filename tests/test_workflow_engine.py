"""
OMEGA DRAKON • SYSTEMS

Teste:
Workflow Engine v1.9.x
"""

import asyncio
import pytest

from core.workflows.models import (
    Workflow,
    WorkflowStep
)
from core.workflows.manager import (
    WorkflowManager
)

pytestmark = pytest.mark.anyio


class MockEventBus:

    async def emit(
        self,
        event_name: str,
        payload: dict
    ):
        print(
            f"\n📢 {event_name}"
        )
        print(payload)


class MockActionManager:

    async def execute(
        self,
        action_name: str,
        payload: dict
    ):

        print(
            f"🎬 {action_name}"
        )

        return {
            "success": True,
            "action": action_name,
            "payload": payload
        }


class MockWorkflowRepo:

    def save(
        self,
        execution
    ):
        pass

    def get(
        self,
        execution_id
    ):
        return None

    def list(
        self,
        limit=50
    ):
        return []

    def count(self):
        return 0


class MockKernel:

    def __init__(self):

        self.events = (
            MockEventBus()
        )

        self.actions = (
            MockActionManager()
        )

        self.workflow_repo = (
            MockWorkflowRepo()
        )


async def test_linear():

    kernel = MockKernel()

    manager = WorkflowManager(
        kernel
    )

    workflow = Workflow(
        workflow_id="linear_test",
        name="Linear Test",
        steps=[
            WorkflowStep(
                step_id="step1",
                action_name="action_1"
            ),
            WorkflowStep(
                step_id="step2",
                action_name="action_2"
            )
        ]
    )

    manager.register(
        workflow
    )

    result = await manager.execute(
        "linear_test"
    )

    assert (
        result.status
        == "COMPLETED"
    )

    assert (
        "step1"
        in result.results
    )

    assert (
        "step2"
        in result.results
    )

    assert (
        result.results["step1"]["action"]
        == "action_1"
    )

    assert (
        result.results["step2"]["action"]
        == "action_2"
    )


async def test_dag():

    kernel = MockKernel()

    manager = WorkflowManager(
        kernel
    )

    workflow = Workflow(
        workflow_id="dag_test",
        name="DAG Test",
        steps=[
            WorkflowStep(
                step_id="extract",
                action_name="extract"
            ),
            WorkflowStep(
                step_id="transform_a",
                action_name="transform_a",
                dependencies=[
                    "extract"
                ]
            ),
            WorkflowStep(
                step_id="transform_b",
                action_name="transform_b",
                dependencies=[
                    "extract"
                ]
            ),
            WorkflowStep(
                step_id="save",
                action_name="save",
                dependencies=[
                    "transform_a",
                    "transform_b"
                ]
            ),
        ]
    )

    manager.register(
        workflow
    )

    result = await manager.execute(
        "dag_test"
    )

    assert (
        result.status
        == "COMPLETED"
    )

    assert list(
        result.results.keys()
    ) == [
        "extract",
        "transform_a",
        "transform_b",
        "save"
    ]

    assert (
        result.results["save"]
        ["payload"]["_inputs"]
        ["transform_a"]["action"]
        == "transform_a"
    )

    assert (
        result.results["save"]
        ["payload"]["_inputs"]
        ["transform_b"]["action"]
        == "transform_b"
    )


async def main():

    print(
        "\n========== LINEAR =========="
    )

    await test_linear()

    print(
        "\n========== DAG =========="
    )

    await test_dag()


if __name__ == "__main__":
    asyncio.run(
        main()
    )
