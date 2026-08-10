"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo:
Workflow Scheduler Engine

Descrição:
Motor responsável pelo agendamento
e execução futura de workflows.

Interface Viva:
Nicky Virthy

Arquiteto:
Alex Projeti
"""

from __future__ import annotations

import asyncio
import uuid

from datetime import datetime, timedelta, timezone

from croniter import (
    croniter,
)

from core.workflows.schedule_models import (
    WorkflowSchedule,
)

from core.workflows.schedule_repository import (
    WorkflowScheduleRepository,
)


class WorkflowSchedulerEngine:

    def __init__(
        self,
        kernel,
        repository: WorkflowScheduleRepository
    ):

        self.kernel = kernel
        self.repository = repository

        self._running = False
        self._task = None

    #
    # LIFECYCLE
    #

    async def start(self):

        if self._running:
            return

        self._running = True

        self._task = asyncio.create_task(
            self._loop()
        )

        await self.kernel.events.emit(
            "WORKFLOW_SCHEDULER_STARTED",
            {}
        )

    async def stop(self):

        if not self._running:
            return

        self._running = False

        if self._task:

            self._task.cancel()

            try:
                await self._task
            except asyncio.CancelledError:
                pass

            self._task = None

        await self.kernel.events.emit(
            "WORKFLOW_SCHEDULER_STOPPED",
            {}
        )

    #
    # SCHEDULE API
    #

    async def schedule(
        self,
        workflow_id: str,
        run_at: datetime | None = None,
        metadata: dict | None = None,
        interval_seconds: int | None = None,
        trigger_type: str = "once",
        cron: str | None = None,
    ):

        schedule = WorkflowSchedule(
            schedule_id=str(
                uuid.uuid4()
            ),
            workflow_id=workflow_id,
            trigger_type=trigger_type,
            interval_seconds=interval_seconds,
            cron=cron,
            run_at=run_at,
            metadata=metadata or {},
        )

        schedule.next_run = (
            self._compute_next_run(
                schedule
            )
        )

        self.repository.save_schedule(
            schedule
        )

        await self.kernel.events.emit(
            "WORKFLOW_SCHEDULE_CREATED",
            {
                "schedule_id":
                    schedule.schedule_id,
                "workflow_id":
                    schedule.workflow_id,
                "trigger_type":
                    schedule.trigger_type,
                "next_run":
                    str(schedule.next_run),
            }
        )

        return schedule

    async def cancel(
        self,
        schedule_id: str
    ):

        schedule = (
            self.repository.disable_schedule(
                schedule_id
            )
        )

        if schedule is None:
            return False

        await self.kernel.events.emit(
            "WORKFLOW_SCHEDULE_CANCELLED",
            {
                "schedule_id":
                    schedule.schedule_id
            }
        )

        return True

    #
    # LOOP
    #

    async def _loop(self):

        while self._running:

            try:

                await self.execute_due()

            except Exception as e:

                await self.kernel.events.emit(
                    "WORKFLOW_SCHEDULER_ERROR",
                    {
                        "error":
                            str(e)
                    }
                )

            await asyncio.sleep(1)

    #
    # EXECUTION
    #

    async def execute_due(self):

        schedules = (
            self.repository.list_schedules(
                enabled_only=True
            )
        )

        for schedule in schedules:

            if not self._is_due(
                schedule
            ):
                continue

            await self._execute_schedule(
                schedule
            )

    async def _execute_schedule(
        self,
        schedule: WorkflowSchedule
    ):

        await self.kernel.events.emit(
            "WORKFLOW_SCHEDULE_TRIGGERED",
            {
                "schedule_id":
                    schedule.schedule_id,
                "workflow_id":
                    schedule.workflow_id,
            }
        )

        try:

            await self.kernel.workflows.execute(
                schedule.workflow_id
            )

            schedule.last_run = (
                datetime.now(timezone.utc)
            )

            await self.kernel.events.emit(
                "WORKFLOW_SCHEDULE_FINISHED",
                {
                    "schedule_id":
                        schedule.schedule_id,
                    "workflow_id":
                        schedule.workflow_id,
                }
            )

        except Exception as e:

            await self.kernel.events.emit(
                "WORKFLOW_SCHEDULE_FAILED",
                {
                    "schedule_id":
                        schedule.schedule_id,
                    "workflow_id":
                        schedule.workflow_id,
                    "error":
                        str(e),
                }
            )

            return

        self._update_after_execution(
            schedule )

    #
    # INTERNALS
    #

    def _is_due(
        self,
        schedule: WorkflowSchedule
    ):

        if not schedule.enabled:
            return False

        next_run = (
            schedule.next_run
            or schedule.run_at
        )

        if next_run is None:
            return False

        return (
            datetime.now(timezone.utc)
            >= next_run
        )

    def _compute_next_run(
        self,
        schedule: WorkflowSchedule
    ):

        now = datetime.now(timezone.utc)

        #
        # ONCE
        #

        if (
            schedule.trigger_type
            == "once"
        ):
            return schedule.run_at

        #
        # INTERVAL
        #

        if (
            schedule.trigger_type
            == "interval"
        ):

            if (
                schedule.interval_seconds
                is None
            ):
                return None

            if schedule.last_run:

                return (
                    schedule.last_run
                    + timedelta(
                        seconds=
                        schedule.interval_seconds
                    )
                )

            return (
                now
                + timedelta(
                    seconds=
                    schedule.interval_seconds
                )
            )

        #
        # CRON
        #

        if (
            schedule.trigger_type
            == "cron"
        ):

            if not schedule.cron:
                return None

            base = (
                schedule.last_run
                or now
            )

            return croniter(
                schedule.cron,
                base
            ).get_next(
                datetime
            )

        return None

    def _update_after_execution(
        self,
        schedule: WorkflowSchedule
    ):

        #
        # EXECUÇÃO ÚNICA
        #

        if (
            schedule.trigger_type
            == "once"
        ):

            schedule.enabled = False
            schedule.next_run = None

            self.repository.save_schedule(
                schedule
            )

            return

        #
        # RECORRENTE
        #

        schedule.next_run = (
            self._compute_next_run(
                schedule
            )
        )

        self.repository.save_schedule(
            schedule
        )
