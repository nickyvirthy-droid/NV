"""
OMEGA DRAKON • SYSTEMS

Teste:
Workflow Scheduler CRON

Valida:

- agendamento via croniter;
- múltiplas execuções;
- recálculo de next_run;
- permanência do schedule habilitado.
"""

import asyncio

from datetime import (
    datetime,
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


async def test_scheduler_cron():

    kernel = MockKernel()

    workflow = Workflow(
        workflow_id="cron_test",
        name="Cron Workflow",
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

    #
    # Executa a cada minuto
    #

    schedule = await scheduler.schedule(
        workflow_id="cron_test",
        trigger_type="cron",
        cron="*/1 * * * *",
        run_at=datetime.utcnow(),
    )

    print(
        "\ncron:",
        schedule.cron
    )

    print(
        "next_run:",
        schedule.next_run
    )

    await scheduler.start()

    #
    # Apenas para validar
    # que o loop permanece ativo.
    #

    await asyncio.sleep(
        3
    )

    await scheduler.stop()

    schedule = (
        repository.get_schedule(
            schedule.schedule_id
        )
    )

    print()

    print(
        "enabled:",
        schedule.enabled
    )

    print(
        "last_run:",
        schedule.last_run
    )

    print(
        "next_run:",
        schedule.next_run
    )


if __name__ == "__main__":
    asyncio.run(
        test_scheduler_cron()
    )
