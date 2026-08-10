"""
OMEGA DRAKON • SYSTEMS
Teste: Injeção de resultados de dependências via _inputs
"""

import asyncio
import pytest

from core.workflows.models import Workflow, WorkflowStep
from core.workflows.manager import WorkflowManager


class MockEvents:
    async def emit(self, event, payload):
        pass


class MockActions:
    async def execute(self, action_name, payload):
        # Simula uma action que devolve o próprio nome + inputs recebidos
        return {
            "produced_by": action_name,
            "received_inputs": payload.get("_inputs", {}),
        }


class MockRepo:
    def save(self, execution):
        pass


class MockKernel:
    def __init__(self):
        self.events = MockEvents()
        self.actions = MockActions()
        self.workflow_repo = MockRepo()


@pytest.mark.anyio
async def test_dependency_inputs_injection():
    manager = WorkflowManager()
    manager.kernel = MockKernel()

    workflow = Workflow(
        workflow_id="inputs_test",
        name="Inputs Test",
        steps=[
            WorkflowStep(step_id="source", action_name="source_action"),
            WorkflowStep(
                step_id="consumer",
                action_name="consumer_action",
                dependencies=["source"],
            ),
        ],
    )

    manager.register(workflow)
    result = await manager.execute("inputs_test")

    assert result.status == "COMPLETED"

    consumer_result = result.results["consumer"]
    assert "received_inputs" in consumer_result
    assert "source" in consumer_result["received_inputs"]

    # O valor injetado deve ser o resultado da step "source"
    source_result = result.results["source"]
    assert consumer_result["received_inputs"]["source"] == source_result
