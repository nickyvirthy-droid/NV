"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo:
Workflow Schedule Models

Descrição:
Modelos de dados para agendamento de workflows.

Interface Viva:
Nicky Virthy

Arquiteto:
Alex Projeti
"""

from dataclasses import (
    dataclass,
    field
)

from datetime import datetime, timezone

from typing import (
    Optional,
    Any
)


@dataclass
class WorkflowSchedule:

    schedule_id: str
    workflow_id: str

    trigger_type: str = "once"

    cron: Optional[str] = None

    interval_seconds: Optional[
        int
    ] = None

    run_at: Optional[
        datetime
    ] = None

    enabled: bool = True

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    last_run: Optional[
        datetime
    ] = None

    next_run: Optional[
        datetime
    ] = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self):

        return {
            "schedule_id":
                self.schedule_id,
            "workflow_id":
                self.workflow_id,
            "trigger_type":
                self.trigger_type,
            "cron":
                self.cron,
            "interval_seconds":
                self.interval_seconds,
            "run_at":
                self.run_at.isoformat()
                if self.run_at
                else None,
            "enabled":
                self.enabled,
            "created_at":
                self.created_at.isoformat(),
            "last_run":
                self.last_run.isoformat()
                if self.last_run
                else None,
            "next_run":
                self.next_run.isoformat()
                if self.next_run
                else None,
            "metadata":
                self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ):

        def parse_dt(
            value
        ):
            if value is None:
                return None

            if isinstance(
                value,
                datetime
            ):
                return value

            return datetime.fromisoformat(
                value
            )

        return cls(
            schedule_id=data[
                "schedule_id"
            ],
            workflow_id=data[
                "workflow_id"
            ],
            trigger_type=data.get(
                "trigger_type",
                "once"
            ),
            cron=data.get(
                "cron"
            ),
            interval_seconds=data.get(
                "interval_seconds"
            ),
            run_at=parse_dt(
                data.get(
                    "run_at"
                )
            ),
            enabled=data.get(
                "enabled",
                True
            ),
            created_at=parse_dt(
                data.get(
                    "created_at"
                )
            )
            or datetime.now(timezone.utc),
            last_run=parse_dt(
                data.get(
                    "last_run"
                )
            ),
            next_run=parse_dt(
                data.get(
                    "next_run"
                )
            ),
            metadata=data.get(
                "metadata",
                {}
            ),
        )


@dataclass
class WorkflowScheduleExecution:

    execution_id: str
    schedule_id: str
    workflow_id: str

    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    finished_at: Optional[
        datetime
    ] = None

    status: str = "PENDING"

    error: Optional[
        str
    ] = None

    def to_dict(self):

        return {
            "execution_id":
                self.execution_id,
            "schedule_id":
                self.schedule_id,
            "workflow_id":
                self.workflow_id,
            "started_at":
                self.started_at.isoformat(),
            "finished_at":
                self.finished_at.isoformat()
                if self.finished_at
                else None,
            "status":
                self.status,
            "error":
                self.error,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict
    ):

        def parse_dt(
            value
        ):
            if value is None:
                return None

            if isinstance(
                value,
                datetime
            ):
                return value

            return datetime.fromisoformat(
                value
            )

        return cls(
            execution_id=data[
                "execution_id"
            ],
            schedule_id=data[
                "schedule_id"
            ],
            workflow_id=data[
                "workflow_id"
            ],
            started_at=parse_dt(
                data.get(
                    "started_at"
                )
            )
            or datetime.now(timezone.utc),
            finished_at=parse_dt(
                data.get(
                    "finished_at"
                )
            ),
            status=data.get(
                "status",
                "PENDING"
            ),
            error=data.get(
                "error"
            ),
        )
