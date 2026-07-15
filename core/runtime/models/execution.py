"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo:
Execution Runtime Model

Descrição:
Modelo base que representa uma execução dentro do
Execution Runtime.

Toda execução (Workflow, SubWorkflow, Template,
Plugin, Agent etc.) deverá utilizar esta estrutura.

Interface Viva:
Nicky Virthy

Arquiteto:
Alex Projeti
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class RuntimeExecution(BaseModel):
    """
    Identidade única de uma execução.

    Esta classe será utilizada por todo o Runtime.
    """

    #
    # Identificação
    #

    execution_id: str

    workflow_id: str

    #
    # Árvore de execução
    #

    parent_execution_id: Optional[str] = None

    root_execution_id: Optional[str] = None

    depth: int = 0

    path: List[str] = Field(
        default_factory=list
    )

    #
    # Estado
    #

    status: str = "PENDING"

    current_step: Optional[str] = None

    #
    # Dados produzidos
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
