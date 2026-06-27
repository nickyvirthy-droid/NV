# ⚙️ SUBSISTEMA DE WORKFLOWS (v1.8.x)

Módulo responsável pela orquestração linear de tarefas operacionais dentro do ecossistema Nicky Virthy, acoplando e automatizando chamadas nativas do `ActionManager` através do `RuntimeKernel`.

## 🏗️ Arquitetura do Componente

*   **WorkflowModels (`models.py`):** Define as estruturas de dados e contratos via `@dataclass` (`Workflow` e `WorkflowStep`).
*   **WorkflowContext (`context.py`):** Gerencia o estado em memória, isolamento de IDs únicos (`execution_id`) e o acúmulo de payloads e resultados gerados por etapa.
*   **WorkflowRegistry (`registry.py`):** Catálogo dinâmico para armazenamento, busca e indexação dos fluxos operacionais disponíveis no sistema.
*   **WorkflowEngine (`engine.py`):** Motor de execução linear responsável por iterar os passos, validar dependências, injetar metadados e manipular falhas de runtime de forma isolada.
*   **WorkflowManager (`manager.py`):** Fachada central (Facade) que integra o catálogo e o motor, expondo uma interface limpa para o Kernel disparar execuções.

## 🚀 Exemplo de Execução Real

```python
manager = WorkflowManager()
fluxo = Workflow(
    id="fluxo_exemplo",
    name="Checagem de Sistema",
    steps=[
        WorkflowStep(name="data", action="datetime", payload={}),
        WorkflowStep(name="cpu", action="cpu_info", payload={})
    ]
)
manager.register_workflow(fluxo)
result = await manager.execute_workflow("fluxo_exemplo", kernel_services=kernel)
