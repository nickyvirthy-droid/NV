"""
OMEGA DRAKON • SYSTEMS

Workflow Stack

Controle de execução hierárquica de Workflows.
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

    def push(
        self,
        workflow_id: str
    ):

        if workflow_id in self.stack:

            raise WorkflowRecursionError(
                f"Recursive workflow detected: {workflow_id}"
            )

        if len(self.stack) >= self.max_depth:

            raise WorkflowMaxDepthError(
                f"Maximum workflow depth ({self.max_depth}) exceeded."
            )

        self.stack.append(
            workflow_id
        )

    def pop(self):

        if self.stack:

            self.stack.pop()

    @property
    def depth(self):

        return len(self.stack)

    @property
    def parent(self):

        if len(self.stack) < 2:

            return None

        return self.stack[-2]

    @property
    def current(self):

        if not self.stack:

            return None

        return self.stack[-1]

    def clone(self):

        other = WorkflowStack()

        other.stack = self.stack.copy()

        other.max_depth = self.max_depth

        return other
