"""
OMEGA DRAKON • SYSTEMS

Step Executor
"""

from .action_executor import ActionExecutor
from .workflow_executor import WorkflowExecutor


class StepExecutor:

    def __init__(self):

        self.action_executor = ActionExecutor()

        self.workflow_executor = WorkflowExecutor()

    async def execute_action(
        self,
        *,
        step,
        payload,
        kernel,
    ):

        return await self.action_executor.execute(
            step=step,
            payload=payload,
            kernel=kernel,
        )

    async def execute_workflow(
        self,
        *,
        manager,
        workflow_id,
        parent_execution,
        context,
    ):

        return await self.workflow_executor.execute(
            manager=manager,
            workflow_id=workflow_id,
            parent_execution=parent_execution,
            context=context,
        )
