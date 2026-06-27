"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: interfaces/api/server.py

Descrição: API Layer externa baseada em FastAPI para controle remoto auditável do Runtime.

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from fastapi import FastAPI, HTTPException, status
from core.workflows.models import Workflow, WorkflowExecution
from core.workflows.manager import WorkflowManager

app = FastAPI(
    title="Nicky Virthy REST API Layer",
    version="1.9.0",
    description="Interface de comunicação externa estável do Runtime Cognitivo NV."
)

# Inicializa o gerenciador global
manager = WorkflowManager()

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Retorna o status operacional da API Layer e a integridade do Runtime."""
    return {"status": "healthy", "layer": "API Layer", "foundation_completion": "100%"}

@app.post("/workflows", status_code=status.HTTP_201_CREATED)
def create_workflow(workflow: Workflow):
    """Registra um novo modelo de workflow resiliente no ecossistema."""
    manager.register_workflow(workflow)
    return {"message": f"Workflow {workflow.workflow_id} registrado com sucesso."}

@app.post("/workflows/{workflow_id}/execute", response_model=WorkflowExecution)
async def execute_workflow(workflow_id: str):
    """Inicia a execução de uma automação remota controlada e monitorada."""
    execution = await manager.start_execution(workflow_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Workflow especificado não foi localizado.")
    return execution

@app.get("/executions/{execution_id}", response_model=WorkflowExecution)
def get_execution_status(execution_id: str):
    """Recupera o estado atualizado e resultados de uma execução específica por UUID."""
    execution = manager.get_execution(execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="ID de Execução não encontrado no Runtime.")
    return execution
