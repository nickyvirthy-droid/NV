"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo:
Workflow Schedule Repository

Descrição:
Persistência de schedules e execuções
agendadas de workflows.

Interface Viva:
Nicky Virthy

Arquiteto:
Alex Projeti
"""

from threading import (
    RLock
)

from core.workflows.schedule_models import (
    WorkflowSchedule,
    WorkflowScheduleExecution
)


class WorkflowScheduleRepository:

    def __init__(self):

        self._lock = RLock()

        self._schedules = {}

        self._executions = {}

    #
    # SCHEDULES
    #

    def save_schedule(
        self,
        schedule: WorkflowSchedule
    ):

        with self._lock:

            self._schedules[
                schedule.schedule_id
            ] = schedule

    def get_schedule(
        self,
        schedule_id: str
    ):

        with self._lock:

            return self._schedules.get(
                schedule_id
            )

    def delete_schedule(
        self,
        schedule_id: str
    ):

        with self._lock:

            self._schedules.pop(
                schedule_id,
                None
            )

    def list_schedules(
        self,
        enabled_only: bool = False
    ):

        with self._lock:

            schedules = list(
                self._schedules.values()
            )

            if enabled_only:

                schedules = [
                    s
                    for s in schedules
                    if s.enabled
                ]

            return schedules

    def count_schedules(
        self
    ):

        with self._lock:

            return len(
                self._schedules
            )

    def enable_schedule(
        self,
        schedule_id: str
    ):

        with self._lock:

            schedule = (
                self._schedules.get(
                    schedule_id
                )
            )

            if schedule:

                schedule.enabled = True

            return schedule

    def disable_schedule(
        self,
        schedule_id: str
    ):

        with self._lock:

            schedule = (
                self._schedules.get(
                    schedule_id
                )
            )

            if schedule:

                schedule.enabled = False

            return schedule

    #
    # EXECUTIONS
    #

    def save_execution(
        self,
        execution: WorkflowScheduleExecution
    ):

        with self._lock:

            self._executions[
                execution.execution_id
            ] = execution

    def get_execution(
        self,
        execution_id: str
    ):

        with self._lock:

            return self._executions.get(
                execution_id
            )

    def list_executions(
        self,
        schedule_id: str | None = None
    ):

        with self._lock:

            executions = list(
                self._executions.values()
            )

            if schedule_id:

                executions = [
                    e
                    for e in executions
                    if (
                        e.schedule_id
                        == schedule_id
                    )
                ]

            return executions

    def count_executions(
        self
    ):

        with self._lock:

            return len(
                self._executions
            )

    def clear(self):

        with self._lock:

            self._schedules.clear()
            self._executions.clear()
