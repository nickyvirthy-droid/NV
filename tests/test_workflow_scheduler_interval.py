"""
OMEGA DRAKON • SYSTEMS

Teste:
Workflow Scheduler Interval

Valida:

- execução recorrente;
- atualização de last_run;
- atualização de next_run;
- schedule permanece ativo.
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


class MockActionManager:

    async def execute(
        self,
        action_name,
        payload
    ):

        print(
            f"🎬 {action_name}"
        )

        return {
            "action":
                action_name,
            "success":
                True,
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

    def count(
        self
    ):
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

        self.workflows = (
            WorkflowManager(
                self
            )
        )


async def test_interval():

    kernel = MockKernel()

    workflow = Workflow(
        workflow_id="interval_test",
        name="Interval Test",
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
            kernel,
            repository
        )
    )

    schedule = await scheduler.schedule(
        workflow_id="interval_test",
        trigger_type="interval",
        interval_seconds=2,
    )

    await scheduler.start()

    await asyncio.sleep(5)

    await scheduler.stop()

    saved = (
        repository.get_schedule(
            schedule.schedule_id
        )
    )

    print()

    print(
        "enabled:",
        saved.enabled
    )

    print(
        "last_run:",
        saved.last_run
    )

    print(
        "next_run:",
        saved.next_run
    )

    assert saved.enabled is True
    assert saved.last_run is not None
    assert saved.next_run is not None
    assert (
        saved.next_run
        > saved.last_run
    )


if __name__ == "__main__":

    asyncio.run(
        test_interval()
    )
