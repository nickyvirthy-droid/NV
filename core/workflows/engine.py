"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Workflow Engine

Descrição: Motor de execução de workflows.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

import asyncio

from core.workflows.context import (
    WorkflowContext
)


class WorkflowEngine:

    async def execute(
        self,
        workflow,
        execution,
        kernel
    ):

        context = WorkflowContext(
            execution.execution_id
        )

        execution.status = "RUNNING"

        await kernel.events.emit(
            "WORKFLOW_STARTED",
            {
                "execution_id":
                    execution.execution_id,
                "workflow_id":
                    workflow.workflow_id
            }
        )

        step_map = {
            step.step_id: step
            for step in workflow.steps
        }

        step_order = [
            step.step_id
            for step in workflow.steps
        ]

        stages = {}

        for step in workflow.steps:

            stages.setdefault(
                step.stage,
                []
            ).append(step)

        branch_targets = set()

        for step in workflow.steps:

            if step.if_true_next:

                branch_targets.add(
                    step.if_true_next
                )

            if step.if_false_next:

                branch_targets.add(
                    step.if_false_next
                )

        current = step_order[0]

        while current:

            step = step_map[current]

            execution.current_step = (
                step.step_id
            )

            #
            # SKIP
            #

            is_branch = (
                step.if_true_next is not None
                or step.if_false_next is not None
            )

            if (
                step.condition_path
                and not is_branch
                and not context.evaluate_condition(
                    step.condition_path
                )
            ):

                await kernel.events.emit(
                    "WORKFLOW_STEP_SKIPPED",
                    {
                        "execution_id":
                            execution.execution_id,
                        "step_id":
                            step.step_id,
                        "condition":
                            step.condition_path
                    }
                )

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

                continue

            await kernel.events.emit(
                "WORKFLOW_STEP_STARTED",
                {
                    "execution_id":
                        execution.execution_id,
                    "step_id":
                        step.step_id
                }
            )

            payload = {}

            if step.arguments:

                payload.update(
                    step.arguments
                )

            payload["_workflow"] = (
                context.data
            )

            result = None

            for attempt in range(
                step.retry_count + 1
            ):

                try:

                    if step.timeout:

                        result = (
                            await asyncio.wait_for(
                                kernel.actions.execute(
                                    action_name=step.action_name,
                                    payload=payload
                                ),
                                timeout=step.timeout
                            )
                        )

                    else:

                        result = (
                            await kernel.actions.execute(
                                action_name=step.action_name,
                                payload=payload
                            )
                        )

                    break

                except asyncio.TimeoutError:

                    execution.errors.append(
                        f"Step '{step.step_id}' timed out."
                    )

                    execution.status = (
                        "FAILED"
                    )

                    await kernel.events.emit(
                        "WORKFLOW_STEP_TIMEOUT",
                        {
                            "execution_id":
                                execution.execution_id,
                            "step_id":
                                step.step_id,
                            "timeout":
                                step.timeout
                        }
                    )

                    kernel.workflow_repo.save(
                        execution
                    )

                    raise

                except Exception as e:

                    execution.errors.append(
                        str(e)
                    )

                    await kernel.events.emit(
                        "WORKFLOW_STEP_RETRY",
                        {
                            "execution_id":
                                execution.execution_id,
                            "step_id":
                                step.step_id,
                            "attempt":
                                attempt + 1,
                            "error":
                                str(e)
                        }
                    )

                    if (
                        attempt
                        >= step.retry_count
                    ):

                        execution.status = (
                            "FAILED"
                        )

                        await kernel.events.emit(
                            "WORKFLOW_STEP_FAILED",
                            {
                                "execution_id":
                                    execution.execution_id,
                                "step_id":
                                    step.step_id,
                                "error":
                                    str(e)
                            }
                        )

                        kernel.workflow_repo.save(
                            execution
                        )

                        raise

                    await asyncio.sleep(
                        step.retry_delay
                    )

            context.set(
                step.step_id,
                result
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
                        step.step_id
                }
            )

            #
            # BRANCHING
            #

            if is_branch:

                condition = True

                if step.condition_path:

                    condition = (
                        context.evaluate_condition(
                            step.condition_path
                        )
                    )

                if condition:

                    current = (
                        step.if_true_next
                    )

                else:

                    current = (
                        step.if_false_next
                    )

                continue

            #
            # EXECUÇÃO LINEAR
            #

            index = step_order.index(
                step.step_id
            )

            if (
                index + 1
                < len(step_order)
            ):

                next_step = step_order[
                    index + 1
                ]

                if (
                    step.step_id
                    in branch_targets
                ):

                    current = None

                else:

                    current = next_step

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

async def _execute_step(
    self,
    step,
    context,
    execution,
    kernel
):

    execution.current_step = (
        step.step_id
    )

    await kernel.events.emit(
        "WORKFLOW_STEP_STARTED",
        {
            "execution_id":
                execution.execution_id,
            "step_id":
                step.step_id
        }
    )

    payload = {}

    if step.arguments:

        payload.update(
            step.arguments
        )

    payload["_workflow"] = (
        context.data
    )

    result = None

    for attempt in range(
        step.retry_count + 1
    ):

        try:

            if step.timeout:

                result = await asyncio.wait_for(
                    kernel.actions.execute(
                        action_name=step.action_name,
                        payload=payload
                    ),
                    timeout=step.timeout
                )

            else:

                result = await (
                    kernel.actions.execute(
                        action_name=step.action_name,
                        payload=payload
                    )
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
                    "execution_id":
                        execution.execution_id,
                    "step_id":
                        step.step_id,
                    "timeout":
                        step.timeout
                }
            )

            kernel.workflow_repo.save(
                execution
            )

            raise

        except Exception as e:

            execution.errors.append(
                str(e)
            )

            await kernel.events.emit(
                "WORKFLOW_STEP_RETRY",
                {
                    "execution_id":
                        execution.execution_id,
                    "step_id":
                        step.step_id,
                    "attempt":
                        attempt + 1,
                    "error":
                        str(e)
                }
            )

            if (
                attempt
                >= step.retry_count
            ):

                execution.status = (
                    "FAILED"
                )

                await kernel.events.emit(
                    "WORKFLOW_STEP_FAILED",
                    {
                        "execution_id":
                            execution.execution_id,
                        "step_id":
                            step.step_id,
                        "error":
                            str(e)
                    }
                )

                kernel.workflow_repo.save(
                    execution
                )

                raise

            await asyncio.sleep(
                step.retry_delay
            )

    context.set(
        step.step_id,
        result
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
                step.step_id
        }
    )

    return result
