# CHANGELOG

Projeto: Nicky Virthy (NV)

Histórico Oficial de Versões

---

# v1.8.0-workflow-engine

Data: Junho/2026

Status: CONCLUÍDA

---

## Objetivo

Introduzir o Subsistema de Workflows Core do NV Runtime.

A meta desta versão foi criar uma infraestrutura dedicada para orquestração assíncrona linear de tarefas operacionais, permitindo encadear e automatizar chamadas nativas do `ActionManager` através do `RuntimeKernel` com isolamento total de contexto.

---

## Implementado

### Workflow Foundation

Criação da camada modular de automação do runtime.

Componentes:

* WorkflowManager (Facade)
* WorkflowRegistry (Catálogo)
* WorkflowEngine (Motor)
* WorkflowModels (Modelos)
* WorkflowContext (Contexto)

---

### Integração ao Runtime

O Subsistema de Workflows foi acoplado diretamente ao coração do sistema, herdando as capacidades do Kernel Real e invocando o `ActionManager` através da camada de segurança nativa de forma transparente.

---

### Testes

Criados e homologados em ambiente real:

* test_workflow_engine.py
* test_workflow_real.py

Resultado:

Todos aprovados com sucesso, executando de ponta a ponta as Actions reais `datetime` e `cpu_info` do servidor.

---

## Compatibilidade

Nenhuma quebra de compatibilidade.

O motor linear estático opera isolado por ID único de execução (`execution_id`), preservando o ecossistema e as variáveis de ambiente sem riscos de contaminação de escopo.

---

## Resultado

Conclusão da primeira geração da Workflow Engine.

Foundation ampliada para:

100% concluída.

---

# v1.7.0-security-layer

Data: Junho/2026

Status: CONCLUÍDA

---

## Objetivo

Introduzir a primeira geração da Security Layer do NV Runtime.

A meta desta versão foi criar uma infraestrutura dedicada para governança operacional, validação de permissões, escopos, aprovações e auditoria, sem quebrar compatibilidade com o Tool Runtime existente.

---

## Implementado

### Security Foundation

Criação da camada de segurança central do runtime.

Componentes:

* SecurityManager
* SecurityDecision
* Security Exceptions

---

### Engines

Implementadas as engines fundamentais da Security Layer:

* PolicyEngine
* PermissionEngine
* ScopeEngine
* ApprovalEngine
* AuditEngine

---

### Configuração

Adicionados arquivos de configuração:

* permissions.yaml
* scopes.yaml
* approval.yaml

Localização:

```text
config/security/

### Auditoria

Implementado:

    AuditRecord  

    Audit Models  

    Audit Engine  

Objetivo:

Registrar eventos operacionais relacionados à segurança.  

### Integração ao Runtime

A Security Layer foi integrada ao fluxo de execução do Runtime.  

Pipeline atual:

Policy Engine
        ↓
Permission Engine
        ↓
Scope Engine
        ↓
Approval Engine
        ↓
Audit Engine
        ↓
Action Execute

### Testes

Criados:

    test_security_policy.py  

    test_security_permission.py  

    test_security_scope.py  

    test_security_approval.py  

    test_security_audit.py  

    test_security_manager.py  

Resultado:

Todos aprovados.

### Compatibilidade

Nenhuma quebra de compatibilidade.  

Todas as actions existentes permanecem operacionais.  

Modo atual:

Compatibilidade.  

Nenhuma regra restritiva está ativa.

### Resultado

Conclusão da primeira geração da Security Layer.  

Foundation ampliada para:

98% concluída.

v1.6.0-tool-runtime

Data: Junho/2026  

Status: CONCLUÍDA  
Objetivo

Transformar o NV Runtime em uma plataforma operacional capaz de executar ferramentas reais.  
Implementado
Tool Runtime

Implementação da primeira geração operacional.  

Total:

56 Actions Operacionais  
Sistema

    system_info  

    datetime  

    uptime  

    disk_usage  

    memory_usage  

    cpu_info  

    ip_address  

    system_which  

    system_hostname  

    system_env  

    system_ping  

    system_user  

    system_groups  

Processos

    process_list  

    process_info  

    process_kill  

Docker

    docker_list  

    docker_status  

    docker_logs  

    docker_stats  

Serviços

    service_list  

    service_status  

    service_logs  

Arquivos

    filesystem_search  

    filesystem_read  

    filesystem_write  

    filesystem_delete  

    filesystem_exists  

    filesystem_info  

    filesystem_list  

    filesystem_mkdir  

    filesystem_move  

    filesystem_copy  

    filesystem_touch  

    filesystem_tree  

    filesystem_hash  

    filesystem_archive  

    filesystem_extract  

Git

    git_branch  

    git_status  

    git_commit  

    git_add  

    git_log  

    git_diff  

    git_checkout  

    git_fetch  

    git_pull  

    git_push  

Banco de Dados

    database_tables  

    database_schema  

    database_query  

Introspecção

    action_info  

    action_schema  

    action_validate  

Resultado

Tool Runtime concluído.  

Foundation ampliada para:

96% concluída.  
v1.5.1-sandbox-hardening

Data: Junho/2026  

Status: CONCLUÍDA  
Objetivo

Eliminar riscos de corrupção de código durante modificações automáticas.  
Implementado
SandboxManager

Ambiente isolado para alterações.  
BackupManager

Backups automáticos.  
RollbackManager

Restauração automática.  
Validation Pipeline

Validação antes da promoção.  
Safe Apply

Aplicação segura de patches.  
Resultado

Sistema de modificação segura concluído.  
v1.5.0-coder-engine

Data: Junho/2026  

Status: CONCLUÍDA  
Objetivo

Introduzir o Coder Engine.  
Implementado

    FileInspector  

    CodeAnalyzer  

    ValidationEngine  

    RuntimeCoder[cite: 2]

    GitManager[cite: 2]

Resultado

Primeira geração do sistema de evolução segura de código[cite: 2].
v1.4.0-omega-drakon

Data: Junho/2026[cite: 2]

Status: CONCLUÍDA[cite: 2]
Objetivo

Consolidar a arquitetura principal do runtime[cite: 2].
Implementado

    Runtime Kernel[cite: 2]

    Event System[cite: 2]

    Registry Layer[cite: 2]

    Session Layer[cite: 2]

    Database Layer[cite: 2]

    Memory Layer[cite: 2]

    Plugin Layer[cite: 2]

    Provider Layer[cite: 2]

Resultado

Foundation operacional estabelecida[cite: 2].
Resumo Histórico
Versão	Marco
v1.4.0	Foundation Runtime
v1.5.0	Coder Engine
v1.5.1	Sandbox Hardening
v1.6.0	Tool Runtime
v1.7.0	Security Layer
v1.8.0	Workflow Engine

### Estado Atual

Versão Atual:
v1.8.0-workflow-engine

Status:
CONGELADA (v1.8.x concluída)

Foundation:
100% concluída

Próxima Etapa:
v1.9.0-dag-engine

---

# v1.8-final

Data: Junho/2026

Status: CONGELADA / HOMOLOGADA

---

## Homologação Final

Todos os testes do subsistema de workflows foram executados e aprovados.

Resultado:

```text
13 passed in 13s
```

## Funcionalidades Consolidadas

### Workflow Foundation

* WorkflowManager
* WorkflowRegistry
* WorkflowEngine
* WorkflowContext
* WorkflowExecution Persistence

### Resilience Layer

* Retry por Step
* Timeout por Step
* Controle de Erros
* Histórico de Execuções

### Controle de Fluxo

* Condition Path
* Skip de Etapas
* Branching (`if_true_next`)
* Branching (`if_false_next`)

## Persistência

* MariaDB
* Tabela: nv_workflow_executions

## Git

* Tag oficial: v1.8-final
* Branch de manutenção: develop-v1.4.0-memory-evolution
* Próxima branch: develop-v1.9.0-dag-engine

## Observações

* Histórico Git reescrito após GitHub Push Protection.
* Segredo removido do histórico do repositório.
* Branch `develop/v1.4.0-memory-evolution` renomeada para `develop-v1.4.0-memory-evolution`.

## Próxima Versão

* v1.9.0-dag-engine
* DAG (Directed Acyclic Graph)
* Execução paralela de Steps
* Dependências entre etapas
* Scheduler interno
* Nested Workflows
* Recuperação de Execuções
* Métricas de Workflow
