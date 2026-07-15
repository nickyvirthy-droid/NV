"""
OMEGA DRAKON • SYSTEMS

Teste:
Workflow Scheduler Persistence

Valida:

- save_schedule()
- get_schedule()
- list_schedules()
- count_schedules()
- to_dict()
- from_dict()
"""

from datetime import (
    datetime,
    timedelta,
)

from core.workflows.schedule_models import (
    WorkflowSchedule,
)

from core.workflows.schedule_repository import (
    WorkflowScheduleRepository,
)


def test_scheduler_persistence():

    repository = (
        WorkflowScheduleRepository()
    )

    #
    # cria schedule
    #

    schedule = WorkflowSchedule(
        schedule_id="test-001",
        workflow_id="workflow_test",
        trigger_type="interval",
        interval_seconds=60,
        run_at=datetime.utcnow(),
        next_run=(
            datetime.utcnow()
            + timedelta(
                seconds=60
            )
        ),
        metadata={
            "source": "test"
        }
    )

    #
    # save
    #

    repository.save_schedule(
        schedule
    )

    #
    # get
    #

    loaded = (
        repository.get_schedule(
            "test-001"
        )
    )

    print(
        "\nGET:"
    )

    print(
        loaded.to_dict()
    )

    #
    # list
    #

    schedules = (
        repository.list_schedules()
    )

    print(
        "\nLIST:"
    )

    for item in schedules:

        print(
            item.schedule_id,
            item.workflow_id
        )

    #
    # count
    #

    print(
        "\nCOUNT:"
    )

    print(
        repository.count_schedules()
    )

    #
    # serialization
    #

    data = (
        loaded.to_dict()
    )

    restored = (
        WorkflowSchedule.from_dict(
            data
        )
    )

    print(
        "\nRESTORED:"
    )

    print(
        restored.to_dict()
    )

    #
    # assertions
    #

    assert loaded is not None

    assert (
        loaded.schedule_id
        == "test-001"
    )

    assert (
        repository.count_schedules()
        == 1
    )

    assert (
        restored.schedule_id
        == loaded.schedule_id
    )

    assert (
        restored.workflow_id
        == loaded.workflow_id
    )

    assert (
        restored.interval_seconds
        == loaded.interval_seconds
    )

    assert (
        restored.metadata
        == loaded.metadata
    )

    print(
        "\nPersistence OK"
    )


if __name__ == "__main__":

    test_scheduler_persistence()
