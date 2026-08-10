⚙️ SUBSISTEMA DE WORKFLOWS (v1.9.2 + Metrics + Templates + Serializer)

Módulo responsável pela orquestração linear e DAG de tarefas operacionais dentro do ecossistema Nicky Virthy, acoplando e automatizando chamadas nativas do ActionManager através do RuntimeKernel.

🏗️ Arquitetura do Componente

WorkflowModels (models.py): Define as estruturas de dados e contratos via Pydantic (Workflow, WorkflowStep, WorkflowExecution).

WorkflowContext (context.py): Gerencia o estado em memória, isolamento de IDs únicos (execution_id) e o acúmulo de payloads e resultados gerados por etapa. Suporta herança e contexto compartilhado.

WorkflowRegistry (registry.py): Catálogo dinâmico para armazenamento, busca e indexação dos fluxos operacionais disponíveis no sistema.

WorkflowEngine (engine.py): Motor de execução linear responsável por iterar os passos, validar dependências, injetar metadados e manipular falhas de runtime de forma isolada.

WorkflowDAGEngine (dag_engine.py): Motor de execução por grafo (stages + parallel).

WorkflowManager (manager.py): Fachada central (Facade) que integra o catálogo e o motor, expondo uma interface limpa para o Kernel disparar execuções. Inclui Nested Workflows, Stack, Metrics, Import/Export e Templates.

WorkflowStack (workflow_stack.py): Proteção de recursão e profundidade máxima.

WorkflowMetrics (metrics.py): Coletor de métricas operacionais (total, sucesso, falha, duração, profundidade, por workflow).

WorkflowSerializer (serializer.py): Import / Export em YAML e JSON (arquivo único, string, dicionário e diretório inteiro).

WorkflowTemplates (templates.py): Catálogo de templates oficiais prontos para uso.

🚀 Exemplo de Execução Real

manager = WorkflowManager(kernel=kernel)

fluxo = Workflow(
    workflow_id="fluxo_exemplo",
    name="Checagem de Sistema",
    steps=[
        WorkflowStep(step_id="data", action_name="datetime", arguments={}),
        WorkflowStep(step_id="cpu", action_name="cpu_info", arguments={}),
    ]
)

manager.register(fluxo)
result = await manager.execute_workflow("fluxo_exemplo")

# Métricas
print(manager.get_metrics_summary())

# Import / Export
yaml_str = manager.export_workflow("fluxo_exemplo", format="yaml")
manager.export_workflow_to_file("fluxo_exemplo", "/tmp/fluxo.yaml")
manager.import_workflow("/tmp/fluxo.yaml")
manager.export_all_to_directory("/tmp/workflows_export")
manager.import_directory("/tmp/workflows_export")

# Templates
print(manager.list_templates())
manager.instantiate_template(
    "template.system_diagnostics",
    workflow_id="meu_diagnostico",
    register=True,
)
manager.load_all_templates()

📊 Capacidades (v1.11.0)

Métricas:
- get_metrics_summary()
- get_workflow_metrics(workflow_id)
- get_recent_executions(limit=20)
- reset_metrics()

Import / Export:
- export_workflow / export_workflow_to_file
- import_workflow (arquivo, string ou dict)
- export_all / export_all_to_directory
- import_directory

Templates:
- list_templates()
- get_template(template_id)
- instantiate_template(...)
- load_all_templates()
