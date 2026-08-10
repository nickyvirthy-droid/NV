"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: core/workflows/templates.py

Descrição:
Catálogo de templates de Workflow.
Fornece templates prontos para uso e
registro no WorkflowManager.

Versão: v1.11.0

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

from typing import Dict, List, Optional

from core.workflows.models import Workflow, WorkflowStep


class WorkflowTemplates:
    """
    Catálogo estático de templates oficiais.

    Cada template retorna uma instância de Workflow
    pronta para registro ou exportação.
    """

    # ---------------------------------------------------------
    # Templates oficiais
    # ---------------------------------------------------------

    @staticmethod
    def system_diagnostics() -> Workflow:
        """Checagem básica de saúde do sistema."""
        return Workflow(
            workflow_id="template.system_diagnostics",
            name="System Diagnostics",
            description="Coleta datetime, CPU e memória do host.",
            version="1.0",
            enabled=True,
            steps=[
                WorkflowStep(
                    step_id="datetime",
                    step_type="action",
                    action_name="datetime",
                    arguments={},
                ),
                WorkflowStep(
                    step_id="cpu",
                    step_type="action",
                    action_name="cpu_info",
                    arguments={},
                ),
                WorkflowStep(
                    step_id="memory",
                    step_type="action",
                    action_name="memory_usage",
                    arguments={},
                ),
            ],
        )

    @staticmethod
    def filesystem_snapshot() -> Workflow:
        """Lista e informa caminhos permitidos."""
        return Workflow(
            workflow_id="template.filesystem_snapshot",
            name="Filesystem Snapshot",
            description="Lista conteúdo de diretórios e coleta info básica.",
            version="1.0",
            enabled=True,
            steps=[
                WorkflowStep(
                    step_id="list_home",
                    step_type="action",
                    action_name="filesystem_list",
                    arguments={"path": "/home/alex/NV"},
                ),
                WorkflowStep(
                    step_id="info_tmp",
                    step_type="action",
                    action_name="filesystem_info",
                    arguments={"path": "/tmp"},
                ),
            ],
        )

    @staticmethod
    def empty() -> Workflow:
        """Template vazio para construção manual."""
        return Workflow(
            workflow_id="template.empty",
            name="Empty Workflow",
            description="Template em branco para criação de novos fluxos.",
            version="1.0",
            enabled=True,
            steps=[],
        )

    # ---------------------------------------------------------
    # Catálogo
    # ---------------------------------------------------------

    @classmethod
    def catalog(cls) -> Dict[str, Workflow]:
        """Retorna todos os templates indexados por workflow_id."""
        templates = [
            cls.system_diagnostics(),
            cls.filesystem_snapshot(),
            cls.empty(),
        ]
        return {t.workflow_id: t for t in templates}

    @classmethod
    def list_ids(cls) -> List[str]:
        return list(cls.catalog().keys())

    @classmethod
    def get(cls, template_id: str) -> Optional[Workflow]:
        return cls.catalog().get(template_id)

    @classmethod
    def instantiate(
        cls,
        template_id: str,
        *,
        workflow_id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Workflow:
        """
        Cria uma cópia do template com IDs opcionalmente
        sobrescritos (útil para criar instâncias a partir
        de um template).
        """
        base = cls.get(template_id)
        if base is None:
            raise KeyError(f"Template não encontrado: {template_id}")

        data = base.model_dump(mode="python")
        if workflow_id:
            data["workflow_id"] = workflow_id
        if name:
            data["name"] = name

        return Workflow.model_validate(data)
