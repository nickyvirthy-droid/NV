"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: core/workflows/context.py

Descrição: Contexto isolado em memória por ID único de execução para passagem de dados estruturados.

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from typing import Dict, Any

class WorkflowContext:
    def __init__(self, execution_id: str):
        self.execution_id: str = execution_id
        self.data: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def evaluate_condition(self, expression: str) -> bool:
        """
        Avalia expressões lógicas seguras baseadas nas variáveis de contexto atuais.
        Exemplo: "results.get('cpu_info', {}).get('usage', 0) < 80"
        """
        try:
            # Escopo restrito para evitar injeções de código
            allowed_globals = {"__builtins__": None}
            allowed_locals = {"results": self.data, "context": self.data}
            return bool(eval(expression, allowed_globals, allowed_locals))
        except Exception as e:
            return False
