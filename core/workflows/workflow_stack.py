"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: core/workflows/workflow_stack.py

Descrição:
Controle de execução hierárquica de Workflows.
Proteção contra recursão e profundidade máxima.

Versão: v1.9.2

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

from dataclasses import dataclass, field


MAX_WORKFLOW_DEPTH = 10


class WorkflowRecursionError(RuntimeError):
    """Workflow chamado recursivamente."""


class WorkflowMaxDepthError(RuntimeError):
    """Profundidade máxima atingida."""


@dataclass
class WorkflowStack:

    stack: list[str] = field(default_factory=list)
    max_depth: int = MAX_WORKFLOW_DEPTH

    # ---------------------------------------------------------
    # API usada pelo WorkflowManager
    # ---------------------------------------------------------

    def enter(self, workflow_id: str) -> None:
        """Entra em um workflow (equivalente a push)."""
        if workflow_id in self.stack:
            raise WorkflowRecursionError(
                f"Recursive workflow detected: {workflow_id}"
            )

        if len(self.stack) >= self.max_depth:
            raise WorkflowMaxDepthError(
                f"Maximum workflow depth ({self.max_depth}) exceeded."
            )

        self.stack.append(workflow_id)

    def leave(self) -> None:
        """Sai do workflow atual (equivalente a pop)."""
        if self.stack:
            self.stack.pop()

    def contains(self, workflow_id: str) -> bool:
        """Verifica se o workflow já está na pilha."""
        return workflow_id in self.stack

    def clear(self) -> None:
        """Limpa toda a pilha."""
        self.stack.clear()

    # ---------------------------------------------------------
    # API legada / utilitários
    # ---------------------------------------------------------

    def push(self, workflow_id: str) -> None:
        self.enter(workflow_id)

    def pop(self) -> None:
        self.leave()

    @property
    def depth(self) -> int:
        return len(self.stack)

    @property
    def parent(self) -> str | None:
        if len(self.stack) < 2:
            return None
        return self.stack[-2]

    @property
    def current(self) -> str | None:
        if not self.stack:
            return None
        return self.stack[-1]

    def clone(self) -> "WorkflowStack":
        other = WorkflowStack()
        other.stack = self.stack.copy()
        other.max_depth = self.max_depth
        return other
