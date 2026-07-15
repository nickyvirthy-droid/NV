"""
OMEGA DRAKON • SYSTEMS

Workflow Executor
"""


class WorkflowExecutor:

    async def execute(
        self,
        *,
        manager,
        workflow_id,
        parent_execution,
        context,
    ):

        return await manager.execute_subworkflow(
            workflow_id=workflow_id,
            parent_execution=parent_execution,
            parent_context=context,
        )
