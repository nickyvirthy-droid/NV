import asyncio

from core.workflows.models import (
    Workflow,
    WorkflowStep
)
from core.workflows.manager import (
    WorkflowManager
)


class MockEvents:

    async def emit(
        self,
        event,
        payload
    ):
        print(event, payload)


class MockActions:

    async def execute(
        self,
        action_name,
        payload
    ):

        await asyncio.sleep(1)

        return {
            "action": action_name,
            "success": True
        }


class MockRepo:

    def save(
        self,
        execution
    ):
        pass


class MockKernel:

    def __init__(self):

        self.events = MockEvents()
        self.actions = MockActions()
        self.workflow_repo = MockRepo()


async def main():

    manager = WorkflowManager()

    manager.kernel = MockKernel()

    workflow = Workflow(
        workflow_id="parallel_test",
        name="Parallel Test",
        steps=[
            WorkflowStep(
                step_id="a",
                action_name="a"
            ),
            WorkflowStep(
                step_id="b",
                action_name="b",
                dependencies=["a"]
            ),
            WorkflowStep(
                step_id="c",
                action_name="c",
                dependencies=["a"]
            ),
            WorkflowStep(
                step_id="d",
                action_name="d",
                dependencies=["b", "c"]
            )
        ]
    )

    manager.register(
        workflow
    )

    result = await manager.execute(
        "parallel_test"
    )

    print(
        result.results
    )


if __name__ == "__main__":
    asyncio.run(main())
