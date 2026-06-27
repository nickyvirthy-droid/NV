"""
OMEGA DRAKON • SYSTEMS
Script de Teste Manual: Workflow Engine v1.8.x
"""

import asyncio
import logging
from core.workflows.models import Workflow, WorkflowStep
from core.workflows.manager import WorkflowManager

# Configura logs para podermos ver os disparos da Engine na tela
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("NV.Tests.Workflow")

# Mock simples do Kernel para simular o EventBus e as Actions sem carregar o sistema todo
class MockEventBus:
    async def emit(self, event_name: str, payload: dict):
        print(f"\n📢 [EVENTO DISPARADO]: {event_name}")
        print(f"   Payload: {payload}")

class MockActionManager:
    async def execute(self, action_name: str, payload: dict) -> dict:
        print(f"🎬 [ActionManager Executando]: {action_name} com payload {payload}")
        # Retorna um sucesso simulado com dados incrementais para testar o repasse de contexto
        return {"success": True, "executed": action_name, "data_received": payload.get("input", "nenhum")}

class MockKernel:
    def __init__(self):
        self.events = MockEventBus()
        self.actions = MockActionManager()

async def run_test():
    logger.info("Inicializando cenário de teste do Workflow Engine...")
    
    # 1. Instancia o gerenciador de workflows
    manager = WorkflowManager()
    kernel_mock = MockKernel()

    # 2. Define um fluxo linear simples: Etapa 1 -> Etapa 2
    test_workflow = Workflow(
        id="fluxo_teste_linear",
        name="Workflow de Teste Linear Puro",
        description="Testando a v1.8.x sem paralelismo",
        steps=[
            WorkflowStep(name="etapa_inicial", action="system.log_info", payload={"input": "Iniciando NV"}),
            WorkflowStep(name="etapa_meio", action="process.check_status", payload={"input": "Processando dados"})
        ]
    )

    # 3. Registra o fluxo no catálogo
    manager.register_workflow(test_workflow)

    # 4. Executa o fluxo usando o mock do kernel
    print("\n" + "="*50 + "\n🚀 INICIANDO EXECUÇÃO DO WORKFLOW\n" + "="*50)
    result = await manager.execute_workflow(
        workflow_id="fluxo_teste_linear",
        kernel_services=kernel_mock,
        metadata={"user": "alex", "env": "development"}
    )
    
    print("\n" + "="*50 + "\n📊 RESULTADO FINAL DO WORKFLOW\n" + "="*50)
    print(f"Sucesso: {result.success}")
    print(f"Status: {result.status}")
    print(f"Resultados Acumulados por Etapa: {result.results}")

if __name__ == "__main__":
    asyncio.run(run_test())
