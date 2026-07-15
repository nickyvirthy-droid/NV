"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo:
core/workflows/context.py

Descrição:
Contexto oficial do Workflow Runtime.

Suporta:

- Contexto isolado
- Herança de contexto
- Contexto compartilhado
- Propagação de resultados
- Árvore de contexto
- Nested Workflows

Versão:
v1.9.2

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import Optional


class WorkflowContext:

    def __init__(
        self,
        execution_id: str,
        parent: Optional["WorkflowContext"] = None,
        shared: bool = False,
    ):

        self.execution_id = execution_id

        self.parent = parent

        self.shared = shared

        self.children: Dict[str, WorkflowContext] = {}

        #
        # Contexto compartilhado
        #

        if shared and parent is not None:

            self.data = parent.data

            self.results = parent.results

        else:

            self.data: Dict[str, Any] = {}

            self.results: Dict[str, Any] = {}

            if parent is not None:

                self.data.update(parent.data)

                self.results.update(parent.results)

    # ---------------------------------------------------------
    # Contexto
    # ---------------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.data[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.data.get(
            key,
            default,
        )

    def has(
        self,
        key: str,
    ) -> bool:

        return key in self.data

    def remove(
        self,
        key: str,
    ) -> None:

        self.data.pop(
            key,
            None,
        )

    def clear(self) -> None:

        self.data.clear()

    # ---------------------------------------------------------
    # Resultados
    # ---------------------------------------------------------

    def set_result(
        self,
        step_id: str,
        result: Any,
    ) -> None:

        self.results[step_id] = result

    def get_result(
        self,
        step_id: str,
        default: Any = None,
    ) -> Any:

        return self.results.get(
            step_id,
            default,
        )

    def has_result(
        self,
        step_id: str,
    ) -> bool:

        return step_id in self.results

    def get_dependency_output(
        self,
        step_id: str,
    ) -> Any:

        return self.results.get(
            step_id
        )

    # ---------------------------------------------------------
    # Nested Workflows
    # ---------------------------------------------------------

    def create_child_context(
        self,
        execution_id: str,
        shared: bool = False,
    ) -> "WorkflowContext":

        child = WorkflowContext(
            execution_id=execution_id,
            parent=self,
            shared=shared,
        )

        self.children[
            execution_id
        ] = child

        return child

    def get_child(
        self,
        execution_id: str,
    ) -> Optional["WorkflowContext"]:

        return self.children.get(
            execution_id
        )

    def merge_results(
        self,
        child: "WorkflowContext",
    ) -> None:

        self.results.update(
            child.results
        )

    def merge_data(
        self,
        child: "WorkflowContext",
    ) -> None:

        self.data.update(
            child.data
        )

    def propagate(
        self,
        child: "WorkflowContext",
    ) -> None:

        self.merge_data(child)

        self.merge_results(child)

    # ---------------------------------------------------------
    # Condições
    # ---------------------------------------------------------

    def evaluate_condition(
        self,
        expression: str,
    ) -> bool:

        try:

            return bool(

                eval(

                    expression,

                    {
                        "__builtins__": None
                    },

                    {

                        "context": self.data,

                        "results": self.results,

                    },

                )

            )

        except Exception:

            return False
