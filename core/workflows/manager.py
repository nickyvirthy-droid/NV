"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Workflow Manager

Descrição: Gerenciador central de workflows.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti
"""

import uuid

from core.workflows.registry import (
    WorkflowRegistry
)
from core.workflows.models import (
    WorkflowExecution
)
from core.workflows.engine import (
    WorkflowEngine
)

class WorkflowManager:

    def __init__(
        self,
        kernel=None
    ):

        self.kernel = kernel

        self.registry = WorkflowRegistry()

        self.executions = {}

        self.engine = WorkflowEngine()

    def register(
        self,
        workflow
    ):

        self.registry.register(
            workflow
        )

    def get(
        self,
        workflow_id: str
    ):

        return self.registry.get(
            workflow_id
        )

    def list(self):

        return self.registry.list()

    async def execute(
        self,
        workflow_id: str
    ):

        workflow = self.get(
            workflow_id
        )

        if not workflow:

            raise ValueError(
                f"Workflow not found: {workflow_id}"
            )

        execution = WorkflowExecution(
            execution_id=str(
                uuid.uuid4()
            ),
            workflow_id=workflow_id
        )

        self.executions[
            execution.execution_id
        ] = execution

        return await self.engine.execute(
            workflow=workflow,
            execution=execution,
            kernel=self.kernel
        )

    def get_execution(
        self,
        execution_id: str
    ):

        return self.kernel.workflow_repo.get(
            execution_id
        )

    def list_executions(
        self,
        limit: int = 50
    ):

        return self.kernel.workflow_repo.list(
            limit
        )

    def execution_count(self):

        return self.kernel.workflow_repo.count()
