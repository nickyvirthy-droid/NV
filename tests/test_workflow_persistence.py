import pytest

from core.runtime.kernel import (
    RuntimeKernel
)


@pytest.mark.anyio
async def test_workflow_execution_persistence():

    kernel = RuntimeKernel()

    execution = await (
        kernel.workflows.execute(
            "system_diagnostics"
        )
    )

    row = (
        kernel.workflow_repo.get(
            execution.execution_id
        )
    )

    assert row is not None

    assert (
        row["execution_id"]
        == execution.execution_id
    )

    assert (
        row["workflow_id"]
        == "system_diagnostics"
    )

    assert (
        row["status"]
        == "COMPLETED"
    )
