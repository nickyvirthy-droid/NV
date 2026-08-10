"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: core/workflows/metrics.py

Descrição:
Coletor de métricas do Workflow Runtime.
Fornece estatísticas operacionais em memória
com suporte a consulta agregada.

Versão: v1.11.0

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class WorkflowMetrics:
    """
    Coletor de métricas do Workflow Runtime.

    Responsabilidades:
    - Contagem total / sucesso / falha
    - Duração média e por execução
    - Profundidade máxima observada
    - Estatísticas por workflow_id
    - Histórico recente
    """

    def __init__(self, max_history: int = 200):
        self.max_history = max_history

        self.total: int = 0
        self.success: int = 0
        self.failed: int = 0

        self.max_depth_observed: int = 0

        # workflow_id -> counters
        self.by_workflow: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "total": 0,
                "success": 0,
                "failed": 0,
                "durations": [],
                "max_depth": 0,
            }
        )

        # Histórico recente (mais novo no final)
        self.history: List[Dict[str, Any]] = []

    # ---------------------------------------------------------
    # Registro
    # ---------------------------------------------------------

    def record(
        self,
        execution,
    ) -> None:
        """
        Registra uma execução finalizada.

        Espera um objeto WorkflowExecution (ou compatível)
        com os campos: execution_id, workflow_id, status,
        depth, started_at, finished_at, errors.
        """

        status = getattr(execution, "status", "UNKNOWN")
        workflow_id = getattr(execution, "workflow_id", "unknown")
        depth = int(getattr(execution, "depth", 0) or 0)
        execution_id = getattr(execution, "execution_id", None)

        started_at = getattr(execution, "started_at", None)
        finished_at = getattr(execution, "finished_at", None)

        duration_seconds: Optional[float] = None
        if started_at is not None and finished_at is not None:
            try:
                duration_seconds = (
                    finished_at - started_at
                ).total_seconds()
            except Exception:
                duration_seconds = None

        is_success = status in ("COMPLETED", "SUCCESS")
        is_failed = status in ("FAILED", "ERROR")

        # Globais
        self.total += 1
        if is_success:
            self.success += 1
        elif is_failed:
            self.failed += 1

        if depth > self.max_depth_observed:
            self.max_depth_observed = depth

        # Por workflow
        stats = self.by_workflow[workflow_id]
        stats["total"] += 1
        if is_success:
            stats["success"] += 1
        elif is_failed:
            stats["failed"] += 1
        if duration_seconds is not None:
            stats["durations"].append(duration_seconds)
        if depth > stats["max_depth"]:
            stats["max_depth"] = depth

        # Histórico
        entry = {
            "execution_id": execution_id,
            "workflow_id": workflow_id,
            "status": status,
            "depth": depth,
            "duration_seconds": duration_seconds,
            "errors": list(getattr(execution, "errors", []) or []),
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
        self.history.append(entry)

        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    # ---------------------------------------------------------
    # Consultas
    # ---------------------------------------------------------

    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return round(self.success / self.total * 100.0, 2)

    def average_duration(self) -> Optional[float]:
        all_durations: List[float] = []
        for stats in self.by_workflow.values():
            all_durations.extend(stats["durations"])
        if not all_durations:
            return None
        return round(sum(all_durations) / len(all_durations), 4)

    def summary(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "success": self.success,
            "failed": self.failed,
            "success_rate_pct": self.success_rate(),
            "average_duration_seconds": self.average_duration(),
            "max_depth_observed": self.max_depth_observed,
            "workflows_tracked": len(self.by_workflow),
        }

    def workflow_stats(
        self,
        workflow_id: str,
    ) -> Dict[str, Any]:
        stats = self.by_workflow.get(workflow_id)
        if not stats:
            return {
                "workflow_id": workflow_id,
                "total": 0,
                "success": 0,
                "failed": 0,
                "success_rate_pct": 0.0,
                "average_duration_seconds": None,
                "max_depth": 0,
            }

        durations = stats["durations"]
        avg = (
            round(sum(durations) / len(durations), 4)
            if durations
            else None
        )
        rate = (
            round(stats["success"] / stats["total"] * 100.0, 2)
            if stats["total"]
            else 0.0
        )

        return {
            "workflow_id": workflow_id,
            "total": stats["total"],
            "success": stats["success"],
            "failed": stats["failed"],
            "success_rate_pct": rate,
            "average_duration_seconds": avg,
            "max_depth": stats["max_depth"],
        }

    def recent(
        self,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        return list(self.history[-limit:])

    def reset(self) -> None:
        self.total = 0
        self.success = 0
        self.failed = 0
        self.max_depth_observed = 0
        self.by_workflow.clear()
        self.history.clear()
