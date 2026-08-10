"""
OMEGA DRAKON • SYSTEMS
Teste: Limite de profundidade de Nested Workflows
"""

import pytest
from core.workflows.workflow_stack import (
    WorkflowStack,
    WorkflowMaxDepthError,
)


def test_max_depth_exceeded():
    stack = WorkflowStack(max_depth=3)

    stack.enter("wf_1")
    stack.enter("wf_2")
    stack.enter("wf_3")

    with pytest.raises(WorkflowMaxDepthError):
        stack.enter("wf_4")


def test_max_depth_ok():
    stack = WorkflowStack(max_depth=3)

    stack.enter("wf_1")
    stack.enter("wf_2")
    stack.enter("wf_3")

    assert stack.depth == 3
    stack.leave()
    assert stack.depth == 2
