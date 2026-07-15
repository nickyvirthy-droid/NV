"""
OMEGA DRAKON • SYSTEMS

Teste:
Workflow Scheduler Engine
"""

import asyncio

from datetime import datetime
from datetime import timedelta

from core.workflows.manager import (
    WorkflowManager,
)
from core.workflows.models import (
    Workflow,
    WorkflowStep,
)
from core.workflows.schedule_repository import (
    WorkflowScheduleRepository,
)
from core.workflows.scheduler_engine import (
    WorkflowSchedulerEngine,
)


class MockEventBus:

    async def emit(
        self,
        event_name,
        payload,
    ):
        print(
            event_name,
            payload
        )


class MockActionManager:

    async def execute(
        self,
        action_name,
        payload,
    ):

        print(
            f"🎬 {action_name}"
        )

        return {
            "action": action_name,
            "success": True,
        }


class MockWorkflowRepo:

    def save(
        self,
        execution,
    ):
        pass

    def get(
        self,
        execution_id,
    ):
        return None

    def list(
        self,
        limit=50,
    ):
        return []

    def count(
        self,
    ):
        return 0


class MockKernel:

    def __init__(
        self,
    ):

        self.events = (
            MockEventBus()
        )

        self.actions = (
            MockActionManager()
        )

        self.workflow_repo = (
            MockWorkflowRepo()
        )

        self.workflows = (
            WorkflowManager(
                self
            )
        )


async def test_scheduler():

    kernel = MockKernel()

    workflow = Workflow(
        workflow_id="scheduled_test",
        name="Scheduled Test",
        steps=[
            WorkflowStep(
                step_id="step1",
                action_name="action_1",
            )
        ],
    )

    kernel.workflows.register(
        workflow
    )

    repository = (
        WorkflowScheduleRepository()
    )

    scheduler = (
        WorkflowSchedulerEngine(
            kernel=kernel,
            repository=repository,
        )
    )

    await scheduler.schedule(
        workflow_id="scheduled_test",
        run_at=(
            datetime.utcnow()
            + timedelta(
                seconds=2
            )
        ),
    )

    await scheduler.start()

    await asyncio.sleep(5)

    await scheduler.stop()


if __name__ == "__main__":
    asyncio.run(
        test_scheduler()
    )
