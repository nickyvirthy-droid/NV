"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Workflow Registry

Descrição: Registro central de workflows.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti
"""

from typing import Dict, Optional

from core.workflows.models import (
    Workflow
)


class WorkflowRegistry:

    def __init__(self):

        self._workflows: Dict[
            str,
            Workflow
        ] = {}

    def register(
        self,
        workflow: Workflow
    ) -> None:

        self._workflows[
            workflow.workflow_id
        ] = workflow

    def get(
        self,
        workflow_id: str
    ) -> Optional[Workflow]:

        return self._workflows.get(
            workflow_id
        )

    def list(self):

        return list(
            self._workflows.keys()
        )
