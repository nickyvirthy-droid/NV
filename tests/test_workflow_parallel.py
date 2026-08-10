"""
OMEGA DRAKON • SYSTEMS
Teste: Execução paralela de estágios no DAG Engine
"""

import asyncio
import pytest

from core.workflows.models import Workflow, WorkflowStep
from core.workflows.manager import WorkflowManager


class MockEvents:
    def __init__(self):
        self.events = []

    async def emit(self, event, payload):
        self.events.append((event, payload))


class MockActions:
    def __init__(self):
        self.calls = []

    async def execute(self, action_name, payload):
        self.calls.append((action_name, payload))
        await asyncio.sleep(0.05)
        return {
            "action": action_name,
            "ok": True,
            "inputs": payload.get("_inputs", {}),
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
async def test_parallel_execution():
    manager = WorkflowManager()
    kernel = MockKernel()
    manager.kernel = kernel

    workflow = Workflow(
        workflow_id="parallel_test",
        name="Parallel Test",
        steps=[
            WorkflowStep(step_id="a", action_name="action_a"),
            WorkflowStep(step_id="b", action_name="action_b", dependencies=["a"]),
            WorkflowStep(step_id="c", action_name="action_c", dependencies=["a"]),
            WorkflowStep(step_id="d", action_name="action_d", dependencies=["b", "c"]),
        ],
    )

    manager.register(workflow)
    result = await manager.execute("parallel_test")

    assert result.status == "COMPLETED"
    assert set(result.results.keys()) == {"a", "b", "c", "d"}

    # Verificar que _inputs foram injetados corretamente
    calls = {name: payload for name, payload in kernel.actions.calls}

    assert "_inputs" in calls["action_b"]
    assert "a" in calls["action_b"]["_inputs"]

    assert "_inputs" in calls["action_c"]
    assert "a" in calls["action_c"]["_inputs"]

    assert "_inputs" in calls["action_d"]
    assert "b" in calls["action_d"]["_inputs"]
    assert "c" in calls["action_d"]["_inputs"]


@pytest.mark.anyio
async def test_stage_events_emitted():
    manager = WorkflowManager()
    kernel = MockKernel()
    manager.kernel = kernel

    workflow = Workflow(
        workflow_id="events_test",
        name="Events Test",
        steps=[
            WorkflowStep(step_id="s1", action_name="s1"),
            WorkflowStep(step_id="s2", action_name="s2", dependencies=["s1"]),
        ],
    )

    manager.register(workflow)
    await manager.execute("events_test")

    event_names = [e[0] for e in kernel.events.events]

    assert "WORKFLOW_GRAPH_BUILT" in event_names
    assert "WORKFLOW_STAGE_STARTED" in event_names
    assert "WORKFLOW_STAGE_FINISHED" in event_names
    assert "WORKFLOW_FINISHED" in event_names
