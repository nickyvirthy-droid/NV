"""
OMEGA DRAKON • SYSTEMS
Teste: Detecção de recursão em Nested Workflows
"""

import pytest
from core.workflows.workflow_stack import (
    WorkflowStack,
    WorkflowRecursionError,
)


def test_recursion_detected():
    stack = WorkflowStack()

    stack.enter("wf_a")
    stack.enter("wf_b")

    with pytest.raises(WorkflowRecursionError):
        stack.enter("wf_a")


def test_contains():
    stack = WorkflowStack()
    stack.enter("wf_x")

    assert stack.contains("wf_x") is True
    assert stack.contains("wf_y") is False
