"""
OMEGA DRAKON • SYSTEMS
Script de Teste de Integração: Workflow Engine com Kernel Real (v1.8.x)
Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

import asyncio
import logging
import sys
from core.runtime.kernel import RuntimeKernel
from core.workflows.models import Workflow, WorkflowStep
from core.workflows.manager import WorkflowManager

# Configuração de Logs alinhada com o barramento do NV
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("NV.Tests.RealWorkflow")

async def run_real_test():
    logger.info("Inicializando o RuntimeKernel real para o teste de integração...")
    
    # 1. Instancia e inicializa o Kernel real do sistema (executa o boot nativo)
    kernel = RuntimeKernel()
    await kernel.boot()
    
    logger.info("Kernel boot concluído. Inicializando WorkflowManager...")
    
    # 2. Instancia o gerenciador de workflows da v1.8.x
    manager = WorkflowManager()
    
    # 3. Define o fluxo utilizando Actions reais mapeadas no seu Registry
    real_workflow = Workflow(
        id="fluxo_operacional_real",
        name="Workflow Real de Produção",
        description="Testando a integração ponta a ponta com Actions do Kernel",
        steps=[
            WorkflowStep(
                name="obter_data_hora", 
                action="datetime",  # Action Real do seu catálogo
                payload={}
            ),
            WorkflowStep(
                name="coletar_cpu", 
                action="cpu_info",  # Outra Action Real do seu catálogo
                payload={}
            )
        ]
    )
    
    # 4. Registra o fluxo no catálogo do Registry
    manager.register_workflow(real_workflow)
    
    print("\n" + "="*60 + "\n🚀 DISPARANDO WORKFLOW REAL ATRAVÉS DO KERNEL\n" + "="*60)
    
    try:
        # 5. Executa o workflow passando os serviços reais do kernel carregado
        result = await manager.execute_workflow(
            workflow_id="fluxo_operacional_real",
            kernel_services=kernel,
            metadata={"user": "alex", "env": "production", "mode": "integration_test"}
        )
        
        print("\n" + "="*60 + "\n📊 ANÁLISE DE CRITÉRIO DE CONCLUSÃO\n" + "="*60)
        print(f"Sucesso do Fluxo: {result.success}")
        print(f"Status de Execução: {result.status}")
        print(f"Resultados Reais das Actions: {result.results}")
        
        if result.success:
            print("\n✅ CRITÉRIOS V1.8.X ATENDIDOS COM SUCESSO:")
            print("   - WorkflowManager, Registry, Engine, Models e Context integrados.")
            print("   - Motor orquestrando Actions REAIS do ecossistema Nicky Virthy!")
        else:
            print(f"\n❌ O fluxo falhou. Erro retornado: {result.error}")
            
    except Exception as e:
        print(f"\n❌ Erro crítico durante a orquestração do teste integrado: {str(e)}")
    
    finally:
        # Encerra graciosamente os serviços do kernel se aplicável
        if hasattr(kernel, "shutdown"):
            await kernel.shutdown()

if __name__ == "__main__":
    asyncio.run(run_real_test())
