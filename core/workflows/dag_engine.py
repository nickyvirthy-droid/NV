"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: core/workflows/dag_engine.py

Descrição:
Motor de execução DAG do Workflow Runtime.

Responsável por:
- Validação do DAG
- Construção dos estágios
- Execução paralela por estágio
- Nested Workflows
- Compatibilidade com ActionManager

Versão: v1.9.2

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

import asyncio

from core.workflows.scheduler import WorkflowScheduler


class WorkflowDAGEngine:

    async def execute(
        self,
        workflow,
        execution,
        context,
        kernel,
        manager,
    ):
        from datetime import datetime, timezone

        execution.status = "RUNNING"

        if execution.started_at is None:
            execution.started_at = datetime.now(timezone.utc)

        await kernel.events.emit(
            "WORKFLOW_STARTED",
            {
                "execution_id": execution.execution_id,
                "workflow_id": workflow.workflow_id,
            },
        )

        scheduler = WorkflowScheduler(workflow)
        scheduler.validate()
        stages = scheduler.build_stages()

        await kernel.events.emit(
            "WORKFLOW_GRAPH_BUILT",
            {
                "execution_id": execution.execution_id,
                "workflow_id": workflow.workflow_id,
                "stages": len(stages),
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

            from datetime import datetime, timezone

            execution.status = "COMPLETED"
            execution.finished_at = datetime.now(timezone.utc)

        except Exception as e:
            from datetime import datetime, timezone

            execution.status = "FAILED"
            execution.finished_at = datetime.now(timezone.utc)
            execution.errors.append(str(e))

            await kernel.events.emit(
                "WORKFLOW_GRAPH_FAILED",
                {
                    "execution_id": execution.execution_id,
                    "workflow_id": workflow.workflow_id,
                    "errors": execution.errors,
                },
            )
            raise

        finally:
            if hasattr(manager, "_finalize_execution"):
                manager._finalize_execution(execution)

            if hasattr(kernel, "workflow_repo") and kernel.workflow_repo:
                kernel.workflow_repo.save(execution)

            await kernel.events.emit(
                "WORKFLOW_FINISHED",
                {
                    "execution_id": execution.execution_id,
                    "status": execution.status,
                },
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
                "execution_id": execution.execution_id,
                "nodes": stage_nodes,
            },
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

        await asyncio.gather(*tasks)

        await kernel.events.emit(
            "WORKFLOW_STAGE_FINISHED",
            {
                "execution_id": execution.execution_id,
                "nodes": stage_nodes,
            },
        )

    async def _execute_step(
        self,
        step,
        context,
        execution,
        kernel,
        manager,
    ):
        # --------------------------------------------------
        # Nested Workflow
        # --------------------------------------------------
        if step.step_type in ("workflow", "subworkflow"):
            from core.workflows.subworkflow import SubWorkflowExecutor

            executor = SubWorkflowExecutor(manager)
            result = await executor.execute(
                step=step,
                execution=execution,
                context=context,
            )

            context.set_result(step.step_id, result)
            execution.results[step.step_id] = result
            return result

        # --------------------------------------------------
        # Action (mesmo caminho do engine linear)
        # --------------------------------------------------
        execution.current_step = step.step_id

        await kernel.events.emit(
            "WORKFLOW_STEP_STARTED",
            {
                "execution_id": execution.execution_id,
                "step_id": step.step_id,
            },
        )

        payload = dict(step.arguments)
        payload["_inputs"] = {
            dep: context.get_result(dep)
            for dep in step.dependencies
        }

        result = None

        for attempt in range(step.retry_count + 1):
            try:
                if step.timeout:
                    result = await asyncio.wait_for(
                        kernel.actions.execute(
                            action_name=step.action_name,
                            payload=payload,
                        ),
                        timeout=step.timeout,
                    )
                else:
                    result = await kernel.actions.execute(
                        action_name=step.action_name,
                        payload=payload,
                    )
                break

            except asyncio.TimeoutError:
                execution.errors.append(
                    f"Step '{step.step_id}' timed out."
                )
                execution.status = "FAILED"

                await kernel.events.emit(
                    "WORKFLOW_STEP_TIMEOUT",
                    {
                        "execution_id": execution.execution_id,
                        "step_id": step.step_id,
                        "timeout": step.timeout,
                    },
                )
                raise

            except Exception as e:
                execution.errors.append(str(e))

                await kernel.events.emit(
                    "WORKFLOW_STEP_RETRY",
                    {
                        "execution_id": execution.execution_id,
                        "step_id": step.step_id,
                        "attempt": attempt + 1,
                        "error": str(e),
                    },
                )

                if attempt >= step.retry_count:
                    execution.status = "FAILED"

                    await kernel.events.emit(
                        "WORKFLOW_STEP_FAILED",
                        {
                            "execution_id": execution.execution_id,
                            "step_id": step.step_id,
                            "error": str(e),
                        },
                    )
                    raise

                await asyncio.sleep(step.retry_delay)

        context.set_result(step.step_id, result)
        execution.results[step.step_id] = result

        await kernel.events.emit(
            "WORKFLOW_STEP_FINISHED",
            {
                "execution_id": execution.execution_id,
                "step_id": step.step_id,
            },
        )

        return result
