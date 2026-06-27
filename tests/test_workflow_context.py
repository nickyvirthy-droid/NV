import pytest

from core.runtime.kernel import (
    RuntimeKernel
)

from core.workflows.models import (
    Workflow,
    WorkflowStep
)


@pytest.mark.anyio
async def test_workflow_context():

    kernel = RuntimeKernel()

    workflow = Workflow(
        workflow_id="context_test",
        name="Context Test",
        description="Teste de contexto",
        steps=[
            WorkflowStep(
                step_id="system",
                action_name="system_info"
            ),
            WorkflowStep(
                step_id="cpu",
                action_name="cpu_info"
            )
        ]
    )

    kernel.workflows.register(
        workflow
    )

    execution = await (
        kernel.workflows.execute(
            "context_test"
        )
    )

    assert "system" in execution.results

    assert "cpu" in execution.results

    assert len(
        execution.results
    ) == 2
