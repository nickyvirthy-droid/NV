"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Workflow Loader

Descrição: Registro de workflows do runtime.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from core.workflows.models import (
    Workflow,
    WorkflowStep
)


def register_workflows(
    manager
):

    diagnostics = Workflow(
        workflow_id="system_diagnostics",
        name="System Diagnostics",
        description="Diagnóstico básico do runtime",
        steps=[
            WorkflowStep(
                step_id="system",
                action_name="system_info"
            ),
            WorkflowStep(
                step_id="cpu",
                action_name="cpu_info"
            ),
            WorkflowStep(
                step_id="memory",
                action_name="memory_usage"
            ),
            WorkflowStep(
                step_id="disk",
                action_name="disk_usage"
            ),
            WorkflowStep(
                step_id="uptime",
                action_name="uptime"
            )
        ]
    )

    manager.register(
        diagnostics
    )
