"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo:
core/workflows/dag_engine.py

Descrição:
Motor de execução DAG do Workflow Runtime.

Responsável por:

- Validação do DAG
- Construção dos estágios
- Execução paralela
- Delegação ao StepExecutor

Versão:
v1.9.2

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

import asyncio

from core.workflows.scheduler import (
    WorkflowScheduler,
)


class WorkflowDAGEngine:

    async def execute(
        self,
        workflow,
        execution,
        context,
        kernel,
        manager,
    ):

        execution.status = "RUNNING"

        await kernel.events.emit(
            "WORKFLOW_STARTED",
            {
                "execution_id":
                    execution.execution_id,
                "workflow_id":
                    workflow.workflow_id,
            },
        )

        scheduler = WorkflowScheduler(
            workflow
        )

        scheduler.validate()

        stages = (
            scheduler.build_stages()
        )

        await kernel.events.emit(
            "WORKFLOW_GRAPH_BUILT",
            {
                "execution_id":
                    execution.execution_id,
                "workflow_id":
                    workflow.workflow_id,
                "stages":
                    len(stages),
            },
        )

        step_map = {

            step.step_id: step

            for step in workflow.steps

        }

        try:

            for stage in stages:

                await self._execute_stage(

                    stage,

                    step_map,

                    context,

                    execution,

                    kernel,

                    manager,

                )

            execution.status = "COMPLETED"

        except Exception:

            execution.status = "FAILED"

            await kernel.events.emit(

                "WORKFLOW_GRAPH_FAILED",

                {

                    "execution_id":
                        execution.execution_id,

                    "workflow_id":
                        workflow.workflow_id,

                    "errors":
                        execution.errors,

                },

            )

            raise

        finally:

            kernel.workflow_repo.save(
                execution
            )

            await kernel.events.emit(

                "WORKFLOW_FINISHED",

                {

                    "execution_id":
                        execution.execution_id,

                    "status":
                        execution.status,

                },

            )

        return execution

        current = step_order[0]

        while current:

            step = step_map[current]

            execution.current_step = (
                step.step_id
            )

            result = await self._execute_step(
                step=step,
                context=context,
                execution=execution,
                kernel=kernel,
                manager=manager,
            )

            if (
                step.step_type
                == "subworkflow"
            ):

                context.set_result(
                    step.step_id,
                    result,
                )

                execution.results[
                    step.step_id
                ] = result

            index = step_order.index(
                step.step_id
            )

            if (
                index + 1
                < len(step_order)
            ):

                current = step_order[
                    index + 1
                ]

            else:

                current = None

        execution.status = (
            "COMPLETED"
        )

        kernel.workflow_repo.save(
            execution
        )

        await kernel.events.emit(
            "WORKFLOW_FINISHED",
            {
                "execution_id":
                    execution.execution_id,
                "status":
                    execution.status
            }
        )

        return execution

    async def _execute_stage(
        self,
        stage_nodes,
        step_map,
        context,
        execution,
        kernel,
        manager,
    ):

        await kernel.events.emit(
            "WORKFLOW_STAGE_STARTED",
            {
                "execution_id":
                    execution.execution_id,
                "nodes":
                    stage_nodes
            }
        )

        tasks = [

            self._execute_step(

                step=step_map[node],

                context=context,

                execution=execution,

                kernel=kernel,

                manager=manager,

            )

            for node in stage_nodes

        ]

        await asyncio.gather(
            *tasks
        )

        await kernel.events.emit(
            "WORKFLOW_STAGE_FINISHED",
            {
                "execution_id":
                    execution.execution_id,
                "nodes":
                    stage_nodes
            }
        )

    async def _execute_step(
        self,
        step,
        context,
        execution,
        kernel,
        manager,
    ):

        #
        # Nested Workflow
        #

        if step.step_type == "subworkflow":

            from core.workflows.subworkflow import (
                SubWorkflowExecutor,
            )

            executor = SubWorkflowExecutor(
                manager
            )

            return await executor.execute(

                step=step,

                execution=execution,

                context=context,

            )

        #
        # Action
        #

        execution.current_step = (
            step.step_id
        )

        await kernel.events.emit(
            "WORKFLOW_STEP_STARTED",
            {
                "execution_id":
                    execution.execution_id,
                "step_id":
                    step.step_id,
            }
        )

        payload = dict(
            step.arguments
        )

        payload["_inputs"] = {

            dep: context.get_result(dep)

            for dep in step.dependencies

        }

        result = await StepExecutor.execute(

            step=step,

            payload=payload,

            context=context,

            execution=execution,

            kernel=kernel,

        )

        context.set_result(
            step.step_id,
            result,
        )

        execution.results[
            step.step_id
        ] = result

        await kernel.events.emit(
            "WORKFLOW_STEP_FINISHED",
            {
                "execution_id":
                    execution.execution_id,
                "step_id":
                    step.step_id,
            }
        )

        return result

    async def _execute_parallel_stage(
        self,
        stage_nodes,
        step_map,
        context,
        execution,
        kernel,
        manager,
    ):

        await kernel.events.emit(
            "WORKFLOW_PARALLEL_STARTED",
            {
                "execution_id":
                    execution.execution_id,
                "nodes":
                    stage_nodes,
            }
        )

        tasks = [

            self._execute_step(

                step=step_map[node],

                context=context,

                execution=execution,

                kernel=kernel,

                manager=manager,

            )

            for node in stage_nodes

        ]

        await asyncio.gather(
            *tasks
        )

        await kernel.events.emit(
            "WORKFLOW_PARALLEL_FINISHED",
            {
                "execution_id":
                    execution.execution_id,
                "nodes":
                    stage_nodes,
            }
        )
