from core.workflows.models import (
    Workflow,
    WorkflowStep
)
from core.workflows.scheduler import (
    WorkflowScheduler
)

workflow = Workflow(
    workflow_id="stage_test",
    name="Stage Test",
    steps=[
        WorkflowStep(
            step_id="extract",
            action_name="extract"
        ),
        WorkflowStep(
            step_id="a",
            action_name="a",
            dependencies=["extract"]
        ),
        WorkflowStep(
            step_id="b",
            action_name="b",
            dependencies=["extract"]
        ),
        WorkflowStep(
            step_id="save",
            action_name="save",
            dependencies=["a", "b"]
        )
    ]
)

scheduler = WorkflowScheduler(
    workflow
)

stages = scheduler.build_stages()

for stage in stages:
    print(stage)
