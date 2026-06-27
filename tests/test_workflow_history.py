import pytest

from core.runtime.kernel import (
    RuntimeKernel
)


@pytest.mark.anyio
async def test_workflow_history():

    kernel = RuntimeKernel()

    execution = await (
        kernel.workflows.execute(
            "system_diagnostics"
        )
    )

    stored = (
        kernel.workflows.get_execution(
            execution.execution_id
        )
    )

    assert stored is not None

    history = (
        kernel.workflows.list_executions()
    )

    assert len(history) > 0

    total = (
        kernel.workflows.execution_count()
    )

    assert total >= 1
