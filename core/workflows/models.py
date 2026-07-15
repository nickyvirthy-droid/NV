"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: core/workflows/models.py

Descrição:
Modelos oficiais do Workflow Runtime.

Versão:
v1.9.2 - Nested Workflows Foundation

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


# ==========================================================
# Workflow Step
# ==========================================================


class WorkflowStep(BaseModel):

    #
    # Identificação
    #

    step_id: str

    #
    # Tipo
    #
    # action
    # workflow
    #

    step_type: str = "action"

    #
    # Action
    #

    action_name: Optional[str] = None

    arguments: Dict[str, Any] = Field(
        default_factory=dict
    )

    #
    # SubWorkflow
    #

    workflow_id: Optional[str] = None

    #
    # Contexto
    #

    inherit_context: bool = True

    shared_context: bool = False

    propagate_results: bool = True

    #
    # Resiliência
    #

    retry_count: int = 0

    retry_delay: float = 1.0

    timeout: Optional[float] = None

    #
    # Controle de Fluxo
    #

    condition_path: Optional[str] = None

    if_true_next: Optional[str] = None

    if_false_next: Optional[str] = None

    #
    # Pipeline
    #

    stage: int = 0

    #
    # DAG
    #

    dependencies: List[str] = Field(
        default_factory=list
    )

    parallel_group: Optional[str] = None

    #
    # Metadados
    #

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )


# ==========================================================
# Workflow
# ==========================================================


class Workflow(BaseModel):

    workflow_id: str

    name: str

    description: Optional[str] = None

    version: str = "1.0"

    enabled: bool = True

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    steps: List[WorkflowStep] = Field(
        default_factory=list
    )


# ==========================================================
# Workflow Execution
# ==========================================================


class WorkflowExecution(BaseModel):

    #
    # Identificação
    #

    execution_id: str

    workflow_id: str

    #
    # Execution Tree
    #

    parent_execution_id: Optional[str] = None

    root_execution_id: Optional[str] = None

    depth: int = 0

    child_executions: List[str] = Field(
        default_factory=list
    )

    #
    # Estado
    #

    status: str = "PENDING"

    current_step: Optional[str] = None

    #
    # Resultado
    #

    results: Dict[str, Any] = Field(
        default_factory=dict
    )

    errors: List[str] = Field(
        default_factory=list
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    #
    # Auditoria
    #

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    started_at: Optional[datetime] = None

    finished_at: Optional[datetime] = None

    #
    # Utilitários
    #

    @property
    def is_root(self) -> bool:

        return self.parent_execution_id is None

    @property
    def has_children(self) -> bool:

        return len(self.child_executions) > 0

    def add_child(
        self,
        execution_id: str,
    ) -> None:

        if execution_id not in self.child_executions:

            self.child_executions.append(
                execution_id
            )
