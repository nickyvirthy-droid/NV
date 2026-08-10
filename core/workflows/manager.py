"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: core/workflows/manager.py

Descrição:
Orquestrador central do Workflow Runtime.

Responsável por:

- Registro de Workflows
- Execução Linear
- Execução DAG
- Nested Workflows
- Execution Tree
- Context Tree
- Workflow Stack
- Proteção contra Recursão
- Controle de Profundidade
- Métricas
- Import / Export (YAML + JSON)

Versão: v1.11.0

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import List, Optional, Union

from core.workflows.registry import WorkflowRegistry
from core.workflows.context import WorkflowContext
from core.workflows.models import Workflow, WorkflowExecution
from core.workflows.engine import WorkflowEngine
from core.workflows.dag_engine import WorkflowDAGEngine
from core.workflows.workflow_stack import WorkflowStack
from core.workflows.metrics import WorkflowMetrics
from core.workflows.serializer import WorkflowSerializer
from core.workflows.templates import WorkflowTemplates


class WorkflowManager:

    MAX_WORKFLOW_DEPTH = 10

    def __init__(
        self,
        kernel=None,
    ):

        self.kernel = kernel

        #
        # Registry
        #

        self.registry = WorkflowRegistry()

        #
        # Runtime State
        #

        self.executions = {}

        self.contexts = {}

        self.workflow_stack = WorkflowStack()

        #
        # Engines
        #

        self.engine = WorkflowEngine()

        self.dag_engine = WorkflowDAGEngine()

        #
        # Metrics
        #

        self.metrics = WorkflowMetrics()

    # ==========================================================
    # Registry
    # ==========================================================

    def register(
        self,
        workflow,
    ):

        self.registry.register(
            workflow
        )

    def unregister(
        self,
        workflow_id: str,
    ):

        self.registry.unregister(
            workflow_id
        )

    def get(
        self,
        workflow_id: str,
    ):

        return self.registry.get(
            workflow_id
        )

    def list(self):

        return self.registry.list()

    # ==========================================================
    # Engine Resolver
    # ==========================================================

    def _resolve_engine(
        self,
        workflow,
    ):

        has_dag = any(

            step.dependencies

            for step in workflow.steps

        )

        if has_dag:

            return self.dag_engine

        return self.engine

    # ==========================================================
    # Execution Factory
    # ==========================================================

    def _create_execution(
        self,
        workflow_id: str,
        parent_execution: WorkflowExecution | None = None,
    ) -> WorkflowExecution:

        execution_id = str(
            uuid.uuid4()
        )

        if parent_execution is None:

            execution = WorkflowExecution(

                execution_id=execution_id,

                workflow_id=workflow_id,

                root_execution_id=execution_id,

                depth=0,

            )

        else:

            execution = WorkflowExecution(

                execution_id=execution_id,

                workflow_id=workflow_id,

                parent_execution_id=parent_execution.execution_id,

                root_execution_id=parent_execution.root_execution_id,

                depth=parent_execution.depth + 1,

            )

            parent_execution.child_executions.append(
                execution.execution_id
            )

        self.executions[
            execution.execution_id
        ] = execution

        return execution

    # ==========================================================
    # Context Factory
    # ==========================================================

    def _create_context(
        self,
        execution: WorkflowExecution,
        parent_context: WorkflowContext | None = None,
        shared: bool = False,
        inherit: bool = True,
    ) -> WorkflowContext:

        #
        # Workflow Raiz
        #

        if parent_context is None:

            context = WorkflowContext(
                execution_id=execution.execution_id,
            )

        #
        # SubWorkflow
        #

        else:

            if inherit:

                context = parent_context.create_child_context(
                    execution_id=execution.execution_id,
                    shared=shared,
                )

            else:

                context = WorkflowContext(
                    execution_id=execution.execution_id,
                )

        self.contexts[
            execution.execution_id
        ] = context

        return context

    # ==========================================================
    # Runtime Lookup
    # ==========================================================

    def get_execution_runtime(
        self,
        execution_id: str,
    ) -> tuple[WorkflowExecution, WorkflowContext]:

        execution = self.executions.get(
            execution_id
        )

        if execution is None:

            raise RuntimeError(
                f"Execution not found: {execution_id}"
            )

        context = self.contexts.get(
            execution_id
        )

        if context is None:

            raise RuntimeError(
                f"Context not found: {execution_id}"
            )

        return (
            execution,
            context,
        )

    def get_context(
        self,
        execution_id: str,
    ) -> WorkflowContext:

        context = self.contexts.get(
            execution_id
        )

        if context is None:

            raise RuntimeError(
                f"Context not found: {execution_id}"
            )

        return context

    # ==========================================================
    # Execution Tree
    # ==========================================================

    def get_root_execution(
        self,
        execution: WorkflowExecution,
    ) -> WorkflowExecution:

        return self.executions[
            execution.root_execution_id
        ]

    def get_children(
        self,
        execution: WorkflowExecution,
    ) -> list[WorkflowExecution]:

        children = []

        for child_id in execution.child_executions:

            child = self.executions.get(
                child_id
            )

            if child is not None:

                children.append(
                    child
                )

        return children

    def execution_tree(
        self,
        execution_id: str,
    ):

        execution = self.executions[
            execution_id
        ]

        return {

            "execution_id":
                execution.execution_id,

            "workflow_id":
                execution.workflow_id,

            "depth":
                execution.depth,

            "children": [

                self.execution_tree(
                    child.execution_id
                )

                for child in self.get_children(
                    execution
                )

            ],

        }

    # ==========================================================
    # Execute Root Workflow
    # ==========================================================

    async def execute(
        self,
        workflow_id: str,
    ):

        return await self.execute_workflow(
            workflow_id=workflow_id,
        )

    async def execute_workflow(
        self,
        workflow_id: str,
    ):

        workflow = self.get(
            workflow_id
        )

        if workflow is None:

            raise ValueError(
                f"Workflow not found: {workflow_id}"
            )

        execution = self._create_execution(
            workflow_id=workflow_id,
        )

        context = self._create_context(
            execution=execution,
        )

        self.workflow_stack.enter(
            workflow_id
        )

        await self.kernel.events.emit(
            "WORKFLOW_TREE_STARTED",
            {
                "execution_id":
                    execution.execution_id,
                "workflow_id":
                    workflow.workflow_id,
            },
        )

        try:

            engine = self._resolve_engine(
                workflow
            )

            result = await engine.execute(

                workflow=workflow,

                execution=execution,

                context=context,

                kernel=self.kernel,

                manager=self,

            )

            await self.kernel.events.emit(
                "WORKFLOW_TREE_FINISHED",
                {
                    "execution_id":
                        execution.execution_id,
                    "workflow_id":
                        workflow.workflow_id,
                },
            )

            return result

        finally:

            self.workflow_stack.leave()

    # ==========================================================
    # Execute SubWorkflow
    # ==========================================================

    async def execute_subworkflow(
        self,
        workflow_id: str,
        parent_execution: WorkflowExecution,
        parent_context: WorkflowContext,
        shared_context: bool = False,
        inherit_context: bool = True,
        propagate_results: bool = True,
    ):

        if (
            parent_execution.depth
            >= self.MAX_WORKFLOW_DEPTH
        ):

            await self.kernel.events.emit(
                "WORKFLOW_MAX_DEPTH_REACHED",
                {
                    "execution_id":
                        parent_execution.execution_id,
                    "workflow_id":
                        workflow_id,
                },
            )

            raise RuntimeError(
                "Maximum workflow depth reached."
            )

        if self.workflow_stack.contains(
            workflow_id
        ):

            await self.kernel.events.emit(
                "WORKFLOW_RECURSION_DETECTED",
                {
                    "execution_id":
                        parent_execution.execution_id,
                    "workflow_id":
                        workflow_id,
                },
            )

            raise RuntimeError(
                f"Recursive workflow detected: {workflow_id}"
            )

        workflow = self.get(
            workflow_id
        )

        if workflow is None:

            raise ValueError(
                f"Workflow not found: {workflow_id}"
            )

        execution = self._create_execution(
            workflow_id=workflow_id,
            parent_execution=parent_execution,
        )

        context = self._create_context(
            execution=execution,
            parent_context=parent_context,
            shared=shared_context,
            inherit=inherit_context,
        )

        self.workflow_stack.enter(
            workflow_id
        )

        await self.kernel.events.emit(
            "WORKFLOW_CHILD_STARTED",
            {
                "parent_execution_id":
                    parent_execution.execution_id,
                "execution_id":
                    execution.execution_id,
                "workflow_id":
                    workflow.workflow_id,
            },
        )

        try:

            engine = self._resolve_engine(
                workflow
            )

            result = await engine.execute(

                workflow=workflow,

                execution=execution,

                context=context,

                kernel=self.kernel,

                manager=self,

            )

            if propagate_results:

                parent_context.merge_results(
                    context
                )

                parent_context.merge_data(
                    context
                )

            await self.kernel.events.emit(
                "WORKFLOW_CHILD_FINISHED",
                {
                    "parent_execution_id":
                        parent_execution.execution_id,
                    "execution_id":
                        execution.execution_id,
                    "workflow_id":
                        workflow.workflow_id,
                },
            )

            return result

        except Exception:

            await self.kernel.events.emit(
                "WORKFLOW_CHILD_FAILED",
                {
                    "parent_execution_id":
                        parent_execution.execution_id,
                    "execution_id":
                        execution.execution_id,
                    "workflow_id":
                        workflow.workflow_id,
                },
            )

            raise

        finally:

            self.workflow_stack.leave()

    # ==========================================================
    # Resume Execution Tree
    # ==========================================================

    async def resume_execution_tree(
        self,
        execution_id: str,
    ):

        execution = self.executions.get(
            execution_id
        )

        if execution is None:

            raise RuntimeError(
                f"Execution not found: {execution_id}"
            )

        workflow = self.get(
            execution.workflow_id
        )

        if workflow is None:

            raise RuntimeError(
                f"Workflow not found: {execution.workflow_id}"
            )

        context = self.contexts.get(
            execution.execution_id
        )

        if context is None:

            context = WorkflowContext(
                execution.execution_id
            )

            self.contexts[
                execution.execution_id
            ] = context

        engine = self._resolve_engine(
            workflow
        )

        return await engine.execute(

            workflow=workflow,

            execution=execution,

            context=context,

            kernel=self.kernel,

            manager=self,

        )

    # ==========================================================
    # Repository API
    # ==========================================================

    def get_execution(
        self,
        execution_id: str,
    ):

        if (
            self.kernel is not None
            and hasattr(
                self.kernel,
                "workflow_repo",
            )
        ):

            execution = (
                self.kernel.workflow_repo.get(
                    execution_id
                )
            )

            if execution is not None:

                return execution

        return self.executions.get(
            execution_id
        )

    def list_executions(
        self,
        limit: int = 50,
    ):

        if (
            self.kernel is not None
            and hasattr(
                self.kernel,
                "workflow_repo",
            )
        ):

            return self.kernel.workflow_repo.list(
                limit
            )

        values = list(
            self.executions.values()
        )

        return values[-limit:]

    def execution_count(
        self,
    ):

        if (
            self.kernel is not None
            and hasattr(
                self.kernel,
                "workflow_repo",
            )
        ):

            return self.kernel.workflow_repo.count()

        return len(
            self.executions
        )

    # ==========================================================
    # Runtime API
    # ==========================================================

    def has_execution(
        self,
        execution_id: str,
    ) -> bool:

        return (
            execution_id
            in self.executions
        )

    def has_context(
        self,
        execution_id: str,
    ) -> bool:

        return (
            execution_id
            in self.contexts
        )

    def clear_runtime(
        self,
    ):

        self.executions.clear()

        self.contexts.clear()

        self.workflow_stack.clear()

    # ==========================================================
    # Metrics API
    # ==========================================================

    def _finalize_execution(
        self,
        execution: WorkflowExecution,
    ) -> None:
        """
        Garante finished_at e registra métricas.
        Chamado após o término de uma execução.
        """
        from datetime import datetime, timezone

        if execution.finished_at is None:
            execution.finished_at = datetime.now(timezone.utc)

        if execution.started_at is None:
            execution.started_at = execution.created_at

        self.metrics.record(execution)

    def get_metrics_summary(self) -> dict:
        return self.metrics.summary()

    def get_workflow_metrics(
        self,
        workflow_id: str,
    ) -> dict:
        return self.metrics.workflow_stats(workflow_id)

    def get_recent_executions(
        self,
        limit: int = 20,
    ) -> list:
        return self.metrics.recent(limit)

    def reset_metrics(self) -> None:
        self.metrics.reset()

    # ==========================================================
    # Import / Export API
    # ==========================================================

    def export_workflow(
        self,
        workflow_id: str,
        *,
        format: str = "yaml",
    ) -> str:
        """
        Exporta um workflow registrado para string YAML ou JSON.
        """
        workflow = self.get(workflow_id)
        if workflow is None:
            raise ValueError(f"Workflow not found: {workflow_id}")

        fmt = format.lower().strip()
        if fmt in ("yaml", "yml"):
            return WorkflowSerializer.to_yaml(workflow)
        if fmt == "json":
            return WorkflowSerializer.to_json(workflow)

        raise ValueError(f"Formato não suportado: {format}")

    def export_workflow_to_file(
        self,
        workflow_id: str,
        path: Union[str, Path],
        *,
        format: str = "yaml",
    ) -> Path:
        """Exporta um workflow registrado para arquivo."""
        workflow = self.get(workflow_id)
        if workflow is None:
            raise ValueError(f"Workflow not found: {workflow_id}")

        return WorkflowSerializer.export_to_file(
            workflow,
            path,
            format=format,
        )

    def import_workflow(
        self,
        source: Union[str, Path, dict],
        *,
        register: bool = True,
        format: Optional[str] = None,
    ) -> Workflow:
        """
        Importa um workflow a partir de:
        - caminho de arquivo (.yaml / .yml / .json)
        - string YAML ou JSON
        - dicionário já carregado

        Se register=True, registra automaticamente no Manager.
        """
        if isinstance(source, dict):
            workflow = WorkflowSerializer.from_dict(source)
        elif isinstance(source, (str, Path)):
            path = Path(source)
            if path.exists() and path.is_file():
                workflow = WorkflowSerializer.import_from_file(path)
            else:
                # Trata como conteúdo textual
                content = str(source)
                fmt = (format or "").lower().strip()
                if fmt in ("yaml", "yml") or content.lstrip().startswith(
                    ("workflow_id:", "name:", "-")
                ):
                    workflow = WorkflowSerializer.from_yaml(content)
                else:
                    workflow = WorkflowSerializer.from_json(content)
        else:
            raise TypeError(
                "source deve ser Path, str ou dict"
            )

        if register:
            self.register(workflow)

        return workflow

    def export_all(
        self,
        *,
        format: str = "yaml",
    ) -> List[str]:
        """
        Exporta todos os workflows registrados.
        Retorna lista de strings (YAML ou JSON).
        """
        results = []
        for workflow_id in self.list():
            results.append(
                self.export_workflow(workflow_id, format=format)
            )
        return results

    def export_all_to_directory(
        self,
        directory: Union[str, Path],
        *,
        format: str = "yaml",
    ) -> List[Path]:
        """
        Exporta todos os workflows registrados para um diretório.
        Um arquivo por workflow.
        """
        workflows = []
        for workflow_id in self.list():
            wf = self.get(workflow_id)
            if wf is not None:
                workflows.append(wf)

        return WorkflowSerializer.export_directory(
            workflows,
            directory,
            format=format,
        )

    def import_directory(
        self,
        directory: Union[str, Path],
        *,
        register: bool = True,
    ) -> List[Workflow]:
        """
        Importa todos os workflows de um diretório
        (.yaml / .yml / .json) e opcionalmente registra.
        """
        workflows = WorkflowSerializer.import_directory(directory)

        if register:
            for wf in workflows:
                self.register(wf)

        return workflows

    # ==========================================================
    # Templates API
    # ==========================================================

    def list_templates(self) -> List[str]:
        """Lista os IDs dos templates oficiais disponíveis."""
        return WorkflowTemplates.list_ids()

    def get_template(
        self,
        template_id: str,
    ) -> Optional[Workflow]:
        """Retorna um template pelo ID (sem registrar)."""
        return WorkflowTemplates.get(template_id)

    def instantiate_template(
        self,
        template_id: str,
        *,
        workflow_id: Optional[str] = None,
        name: Optional[str] = None,
        register: bool = True,
    ) -> Workflow:
        """
        Cria uma instância a partir de um template.
        Se register=True, registra no Manager.
        """
        workflow = WorkflowTemplates.instantiate(
            template_id,
            workflow_id=workflow_id,
            name=name,
        )

        if register:
            self.register(workflow)

        return workflow

    def load_all_templates(
        self,
        *,
        register: bool = True,
    ) -> List[Workflow]:
        """
        Carrega todos os templates oficiais.
        Se register=True, registra no Manager.
        """
        templates = list(WorkflowTemplates.catalog().values())

        if register:
            for t in templates:
                self.register(t)

        return templates
