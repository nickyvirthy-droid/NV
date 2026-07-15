"""
OMEGA DRAKON • SYSTEMS

Teste:
Workflow Scheduler Cancel

Valida:

- cancelamento de schedules;
- disable automático;
- não execução após cancelamento.
"""

import asyncio

from datetime import (
    datetime,
    timedelta,
)

from core.workflows.models import (
    Workflow,
    WorkflowStep,
)

from core.workflows.manager import (
    WorkflowManager,
)

from core.workflows.scheduler_engine import (
    WorkflowSchedulerEngine,
)

from core.workflows.schedule_repository import (
    WorkflowScheduleRepository,
)


class MockEventBus:

    async def emit(
        self,
        event_name,
        payload
    ):
        print(
            event_name,
            payload
        )


class MockActions:

    async def execute(
        self,
        action_name,
        payload
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
            MockActions()
        )

        self.workflow_repo = (
            MockWorkflowRepo()
        )

        self.workflows = (
            WorkflowManager(
                self
            )
        )


async def test_scheduler_cancel():

    kernel = MockKernel()

    workflow = Workflow(
        workflow_id="cancel_test",
        name="Cancel Test",
        steps=[
            WorkflowStep(
                step_id="step1",
                action_name="action_1"
            )
        ]
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

    schedule = await scheduler.schedule(
        workflow_id="cancel_test",
        run_at=(
            datetime.utcnow()
            + timedelta(
                seconds=5
            )
        )
    )

    print(
        "\nschedule:",
        schedule.schedule_id
    )

    cancelled = (
        await scheduler.cancel(
            schedule.schedule_id
        )
    )

    print(
        "cancelled:",
        cancelled
    )

    schedule = (
        repository.get_schedule(
            schedule.schedule_id
        )
    )

    print(
        "enabled:",
        schedule.enabled
    )

    await scheduler.start()

    await asyncio.sleep(
        6
    )

    await scheduler.stop()

    print(
        "\nlast_run:",
        schedule.last_run
    )

    print(
        "next_run:",
        schedule.next_run
    )


if __name__ == "__main__":
    asyncio.run(
        test_scheduler_cancel()
    )
