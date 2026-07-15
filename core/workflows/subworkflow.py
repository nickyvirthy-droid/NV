"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo:
core/workflows/subworkflow.py

Descrição:
Executor de Nested Workflows.

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from core.workflows.models import (
    WorkflowExecution,
    WorkflowStep,
)


class SubWorkflowExecutor:

    def __init__(
        self,
        manager,
    ):

        self.manager = manager

    async def execute(
        self,
        *,
        step: WorkflowStep,
        execution: WorkflowExecution,
        context,
    ):

        child_execution = (
            await self.manager.execute_subworkflow(
                workflow_id=step.workflow_id,
                parent_execution=execution,
                parent_context=context,
                shared_context=step.shared_context,
            )
        )

        if step.propagate_results:

            child_context = (
                self.manager.contexts[
                    child_execution.execution_id
                ]
            )

            context.merge_results(
                child_context
            )

            if step.inherit_context:

                context.merge_data(
                    child_context
                )

        return {

            "execution_id":
                child_execution.execution_id,

            "workflow_id":
                child_execution.workflow_id,

            "status":
                child_execution.status,

            "results":
                child_execution.results,

        }
