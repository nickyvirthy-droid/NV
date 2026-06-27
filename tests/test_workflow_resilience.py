"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: tests/test_workflow_resilience.py

Descrição: Teste funcional corrigido para validação de desvios e resiliência na v1.9.0.

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

import asyncio
from core.workflows.models import Workflow, WorkflowStep
from core.workflows.manager import WorkflowManager

async def run_test():
    print("[NICKY][INFO] Inicializando suite de validação da v1.9.0...")
    manager = WorkflowManager()

    # Definição do Workflow com caminhos mutuamente exclusivos
    steps = [
        # Passo 1: Executa a validação de estado inicial
        WorkflowStep(step_id="step_check", action_name="get_system_status"),
        
        # Passo 2: Avalia o retorno e bifurca o fluxo
        WorkflowStep(
            step_id="step_decision", 
            action_name="conditional_gate",
            condition_path="results.get('step_check', {}).get('status') == 'success'",
            if_true_next="step_success_path",
            if_false_next="step_fail_path"
        ),
        
        # Passo 3 (Caminho Verdadeiro): Executa a action normalmente e encerra aqui
        WorkflowStep(
            step_id="step_success_path", 
            action_name="log_event_success",
            if_true_next=None  # Sinaliza explicitamente à engine modificada para parar
        ),
        
        # Passo 4 (Caminho Falso): Não deve ser tocado se o step_decision for True
        WorkflowStep(
            step_id="step_fail_path", 
            action_name="fail_action", 
            retry_count=2, 
            retry_delay=0.1
        )
    ]

    wf = Workflow(workflow_id="wf_resilience_test", name="Teste de Robustez", steps=steps)
    manager.register_workflow(wf)

    # Execução do pipeline
    execution = await manager.start_execution("wf_resilience_test")
    
    print("\n--- [NICKY][INFO] RESULTADO FINAL DO TESTE ---")
    print(f"Status da Execução: {execution.status}")
    print(f"Resultados Armazenados: {execution.results}")
    print(f"Erros Coletados: {execution.errors}")
    
    assert execution.status == "COMPLETED", f"O workflow deveria terminar como COMPLETED, mas terminou como: {execution.status}"
    assert "step_success_path" in execution.results, "O caminho de sucesso deveria ter sido executado."
    assert "step_fail_path" not in execution.results, "O caminho de falha não deveria ter sido tocado."
    
    print("[NICKY][INFO] Todos os testes da v1.9.0 foram homologados com 100% de sucesso!")

if __name__ == "__main__":
    asyncio.run(run_test())
