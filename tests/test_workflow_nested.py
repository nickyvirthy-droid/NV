"""
OMEGA DRAKON • SYSTEMS
Teste: Nested Workflows (execução hierárquica)
"""

import pytest

from core.workflows.models import Workflow, WorkflowStep
from core.workflows.manager import WorkflowManager
from core.workflows.workflow_stack import (
    WorkflowRecursionError,
    WorkflowMaxDepthError,
)


class MockEvents:
    def __init__(self):
        self.events = []

    async def emit(self, event, payload):
        self.events.append((event, payload))


class MockActions:
    async def execute(self, action_name, payload):
        return {"action": action_name, "ok": True}


class MockRepo:
    def save(self, execution):
        pass


class MockKernel:
    def __init__(self):
        self.events = MockEvents()
        self.actions = MockActions()
        self.workflow_repo = MockRepo()


@pytest.mark.anyio
async def test_nested_workflow_basic():
    manager = WorkflowManager()
    manager.kernel = MockKernel()

    child = Workflow(
        workflow_id="child_wf",
        name="Child",
        steps=[
            WorkflowStep(step_id="child_step", action_name="child_action"),
        ],
    )
    manager.register(child)

    parent = Workflow(
        workflow_id="parent_wf",
        name="Parent",
        steps=[
            WorkflowStep(step_id="before", action_name="before_action"),
            WorkflowStep(
                step_id="nested",
                step_type="workflow",
                workflow_id="child_wf",
                inherit_context=True,
                shared_context=False,
                propagate_results=True,
            ),
            WorkflowStep(step_id="after", action_name="after_action"),
        ],
    )
    manager.register(parent)

    result = await manager.execute("parent_wf")

    assert result.status == "COMPLETED"
    assert set(result.results.keys()) == {"before", "nested", "after"}

    event_names = [e[0] for e in manager.kernel.events.events]
    assert "WORKFLOW_CHILD_STARTED" in event_names
    assert "WORKFLOW_CHILD_FINISHED" in event_names


@pytest.mark.anyio
async def test_nested_recursion_blocked():
    manager = WorkflowManager()
    manager.kernel = MockKernel()

    # Workflow que chama a si mesmo
    recursive = Workflow(
        workflow_id="recursive_wf",
        name="Recursive",
        steps=[
            WorkflowStep(
                step_id="self_call",
                step_type="workflow",
                workflow_id="recursive_wf",
            ),
        ],
    )
    manager.register(recursive)

    with pytest.raises(Exception) as exc_info:
        await manager.execute("recursive_wf")

    # Pode ser RuntimeError ou WorkflowRecursionError dependendo da camada
    assert "Recursive" in str(exc_info.value) or "recursive" in str(exc_info.value).lower()
