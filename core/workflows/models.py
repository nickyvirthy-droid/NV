"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: core/workflows/models.py

Descrição: Definição de modelos para Workflows.

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class WorkflowStep(BaseModel):

    step_id: str

    action_name: str

    arguments: Dict[str, Any] = Field(
        default_factory=dict
    )

    #
    # Resiliência
    #

    retry_count: int = 0

    retry_delay: float = 1.0

    timeout: Optional[float] = None

    #
    # Controle de fluxo
    #

    condition_path: Optional[str] = None

    if_true_next: Optional[str] = None

    if_false_next: Optional[str] = None

    #
    # Pipeline
    #

    stage: int = 0


class Workflow(BaseModel):

    workflow_id: str

    name: str

    description: Optional[str] = None

    steps: List[WorkflowStep]


class WorkflowExecution(BaseModel):

    execution_id: str

    workflow_id: str

    status: str = "PENDING"

    current_step: Optional[str] = None

    results: Dict[str, Any] = Field(
        default_factory=dict
    )

    errors: List[str] = Field(
        default_factory=list
    )
