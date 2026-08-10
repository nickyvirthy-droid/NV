"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: core/workflows/serializer.py

Descrição:
Serialização e desserialização de Workflows.
Suporta exportação e importação em YAML e JSON.
Validação via modelos Pydantic oficiais.

Versão: v1.11.0

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from core.workflows.models import Workflow, WorkflowStep


class WorkflowSerializerError(Exception):
    """Erro de serialização / desserialização de Workflow."""


class WorkflowSerializer:
    """
    Responsável por converter Workflows entre
    objetos Pydantic e formatos YAML / JSON.
    """

    # ---------------------------------------------------------
    # Export
    # ---------------------------------------------------------

    @staticmethod
    def to_dict(workflow: Workflow) -> Dict[str, Any]:
        """Converte Workflow para dicionário puro."""
        return workflow.model_dump(mode="python")

    @staticmethod
    def to_json(
        workflow: Workflow,
        *,
        indent: int = 2,
        ensure_ascii: bool = False,
    ) -> str:
        """Exporta Workflow para string JSON."""
        data = WorkflowSerializer.to_dict(workflow)
        return json.dumps(
            data,
            indent=indent,
            ensure_ascii=ensure_ascii,
            default=str,
        )

    @staticmethod
    def to_yaml(workflow: Workflow) -> str:
        """Exporta Workflow para string YAML."""
        data = WorkflowSerializer.to_dict(workflow)
        return yaml.safe_dump(
            data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )

    @staticmethod
    def export_to_file(
        workflow: Workflow,
        path: Union[str, Path],
        *,
        format: str = "yaml",
    ) -> Path:
        """
        Exporta Workflow para arquivo.

        format: "yaml" | "json"
        """
        path = Path(path)
        fmt = format.lower().strip()

        if fmt in ("yaml", "yml"):
            content = WorkflowSerializer.to_yaml(workflow)
            if path.suffix not in (".yaml", ".yml"):
                path = path.with_suffix(".yaml")
        elif fmt == "json":
            content = WorkflowSerializer.to_json(workflow)
            if path.suffix != ".json":
                path = path.with_suffix(".json")
        else:
            raise WorkflowSerializerError(
                f"Formato não suportado: {format}. Use 'yaml' ou 'json'."
            )

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    # ---------------------------------------------------------
    # Import
    # ---------------------------------------------------------

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Workflow:
        """
        Cria Workflow a partir de dicionário.
        Valida via Pydantic.
        """
        if not isinstance(data, dict):
            raise WorkflowSerializerError(
                "Dados de importação devem ser um dicionário."
            )

        try:
            return Workflow.model_validate(data)
        except Exception as e:
            raise WorkflowSerializerError(
                f"Falha na validação do Workflow: {e}"
            ) from e

    @staticmethod
    def from_json(content: str) -> Workflow:
        """Importa Workflow a partir de string JSON."""
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise WorkflowSerializerError(
                f"JSON inválido: {e}"
            ) from e

        return WorkflowSerializer.from_dict(data)

    @staticmethod
    def from_yaml(content: str) -> Workflow:
        """Importa Workflow a partir de string YAML."""
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise WorkflowSerializerError(
                f"YAML inválido: {e}"
            ) from e

        if data is None:
            raise WorkflowSerializerError("YAML vazio.")

        return WorkflowSerializer.from_dict(data)

    @staticmethod
    def import_from_file(
        path: Union[str, Path],
    ) -> Workflow:
        """
        Importa Workflow a partir de arquivo.
        Detecta formato pela extensão (.yaml / .yml / .json).
        """
        path = Path(path)

        if not path.exists():
            raise WorkflowSerializerError(
                f"Arquivo não encontrado: {path}"
            )

        content = path.read_text(encoding="utf-8")
        suffix = path.suffix.lower()

        if suffix in (".yaml", ".yml"):
            return WorkflowSerializer.from_yaml(content)
        elif suffix == ".json":
            return WorkflowSerializer.from_json(content)
        else:
            raise WorkflowSerializerError(
                f"Extensão não suportada: {suffix}. "
                "Use .yaml, .yml ou .json."
            )

    # ---------------------------------------------------------
    # Batch helpers
    # ---------------------------------------------------------

    @staticmethod
    def export_many_to_dict(
        workflows: List[Workflow],
    ) -> List[Dict[str, Any]]:
        return [
            WorkflowSerializer.to_dict(w) for w in workflows
        ]

    @staticmethod
    def import_many_from_dict(
        items: List[Dict[str, Any]],
    ) -> List[Workflow]:
        return [
            WorkflowSerializer.from_dict(item) for item in items
        ]

    # ---------------------------------------------------------
    # Directory batch
    # ---------------------------------------------------------

    @staticmethod
    def export_directory(
        workflows: List[Workflow],
        directory: Union[str, Path],
        *,
        format: str = "yaml",
    ) -> List[Path]:
        """
        Exporta vários workflows para um diretório.
        Um arquivo por workflow (nome = workflow_id).
        """
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)

        written: List[Path] = []
        fmt = format.lower().strip()

        for workflow in workflows:
            safe_name = (
                workflow.workflow_id
                .replace("/", "_")
                .replace("\\", "_")
                .replace(" ", "_")
            )
            if fmt in ("yaml", "yml"):
                path = directory / f"{safe_name}.yaml"
            else:
                path = directory / f"{safe_name}.json"

            written.append(
                WorkflowSerializer.export_to_file(
                    workflow,
                    path,
                    format=fmt,
                )
            )

        return written

    @staticmethod
    def import_directory(
        directory: Union[str, Path],
    ) -> List[Workflow]:
        """
        Importa todos os arquivos .yaml / .yml / .json
        de um diretório.
        """
        directory = Path(directory)

        if not directory.exists() or not directory.is_dir():
            raise WorkflowSerializerError(
                f"Diretório não encontrado: {directory}"
            )

        results: List[Workflow] = []
        patterns = ("*.yaml", "*.yml", "*.json")

        for pattern in patterns:
            for path in sorted(directory.glob(pattern)):
                try:
                    results.append(
                        WorkflowSerializer.import_from_file(path)
                    )
                except WorkflowSerializerError:
                    # Continua com os demais arquivos
                    continue

        return results
