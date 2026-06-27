import pytest

from core.runtime.kernel import (
    RuntimeKernel
)


@pytest.mark.anyio
async def test_system_diagnostics_workflow():

    kernel = RuntimeKernel()

    workflow = kernel.workflows.get(
        "system_diagnostics"
    )

    assert workflow is not None

    execution = await kernel.workflows.execute(
        "system_diagnostics"
    )

    assert execution.status == "COMPLETED"

    assert "system" in execution.results

    assert "cpu" in execution.results

    assert "memory" in execution.results

    assert "disk" in execution.results

    assert "uptime" in execution.results
