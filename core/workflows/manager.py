"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo:
core/workflows/manager.py

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

Versão:
v1.9.2

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

import uuid

from core.workflows.registry import WorkflowRegistry
from core.workflows.context import WorkflowContext
from core.workflows.models import WorkflowExecution
from core.workflows.engine import WorkflowEngine
from core.workflows.dag_engine import WorkflowDAGEngine
from core.workflows.workflow_stack import WorkflowStack


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
