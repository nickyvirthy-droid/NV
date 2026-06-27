# Nicky Virthy (NV)

Runtime Cognitivo Modular para execução local de agentes inteligentes, automação operacional e evolução controlada.

Versão Atual: v1.8.0-workflow-engine

Status: Foundation Concluída

Última Atualização: Junho/2026

---

# Visão Geral

O Nicky Virthy (NV) é uma plataforma modular desenvolvida para funcionar como um Runtime Cognitivo Local.

Seu objetivo é fornecer uma infraestrutura capaz de combinar:

* memória persistente;
* gerenciamento de sessões;
* sistema de eventos;
* execução de ações;
* integração com modelos de linguagem;
* persistência em banco de dados;
* plugins extensíveis;
* automação operacional;
* evolução segura de código;
* execução controlada de ferramentas operacionais;
* governança operacional e segurança;
* orquestração de workflows automatizados.

O projeto foi concebido para evoluir gradualmente de um runtime inteligente para uma plataforma operacional cognitiva completa.

---

# Estado Atual

Versão:
v1.8.0-workflow-engine

Foundation:
100% concluída (Core base estabilizado)

Status Geral:
Estável para desenvolvimento.
Tool Runtime concluído.
Security Layer concluída.
Workflow Engine Linear concluída.

---

# Capacidades Implementadas

## Runtime Kernel
Responsável pelo ciclo de vida do sistema.
Recursos:
* bootstrap do runtime;
* gerenciamento de serviços;
* coordenação de módulos;
* carregamento de componentes.

Status:
✅ Implementado

---

## Event System
Sistema interno de eventos.
Recursos:
* publicação de eventos;
* assinatura de eventos;
* comunicação desacoplada.

Status:
✅ Implementado

---

## Action System
Camada responsável pela execução de capacidades operacionais.
Componentes:
* ActionManager
* ActionRegistry
* ActionContext
* ActionResolver

Recursos:
* registro de ações;
* descoberta de ações;
* execução controlada.

Status:
✅ Implementado

---

## Memory Layer
Sistema de memória persistente e contextual.
Componentes:
* MemoryManager
* ProfileMemory
* RuntimeMemory
* Fact Extraction
* Resolver

Recursos:
* armazenamento persistente;
* recuperação contextual;
* gerenciamento de perfil;
* resolução de informações.

Status:
✅ Implementado

---

## Database Layer
Infraestrutura de persistência.
Componentes:
* DatabaseConnection
* DatabaseManager
* Repositories
* Migrations

Recursos:
* MariaDB nativo;
* acesso estruturado;
* persistência de runtime;
* reutilização por ferramentas operacionais.

Status:
✅ Implementado

---

## Session Layer
Gerenciamento de sessões operacionais.
Componentes:
* SessionManager
* SessionHistory

Recursos:
* histórico;
* rastreamento;
* contexto temporal.

Status:
✅ Implementado

---

## Registry Layer
Container interno de serviços.
Recursos:
* registro de serviços;
* resolução de dependências;
* compartilhamento de componentes.

Status:
✅ Implementado

---

## Provider Layer
Integração com provedores de IA.
Recursos:
* àbstração de providers;
* integração Ollama;
* expansão futura para múltiplos modelos.

Status:
✅ Implementado

---

## Plugin Layer
Sistema de extensibilidade.
Recursos:
* carregamento dinâmico;
* descoberta automática;
* expansão modular.

Status:
✅ Implementado

---

## Tool Runtime
Primeira geração operacional concluída.
Total atual:
56 Actions Operacionais

Recursos:

### Sistema
* system_info
* datetime
* uptime
* disk_usage
* memory_usage
* cpu_info
* ip_address
* system_which
* system_hostname
* system_env
* system_ping
* system_user
* system_groups

### Processos
* process_list
* process_info
* process_kill

### Docker
* docker_list
* docker_status
* docker_logs
* docker_stats

### Serviços
* service_list
* service_status
* service_logs

### Arquivos
* filesystem_search
* filesystem_read
* filesystem_write
* filesystem_delete
* filesystem_exists
* filesystem_info
* filesystem_list
* filesystem_mkdir
* filesystem_move
* filesystem_copy
* filesystem_touch
* filesystem_tree
* filesystem_hash
* filesystem_archive
* filesystem_extract

### Git
* git_branch
* git_status
* git_commit
* git_add
* git_log
* git_diff
* git_checkout
* git_fetch
* git_pull
* git_push

### Banco de Dados
* database_tables
* database_schema
* database_query

### Introspecção
* action_info
* action_schema
* action_validate

Status:
✅ Implementado

---

## Coder Engine
Sistema de modificação segura de código.
Componentes:
* FileInspector
* SandboxManager
* BackupManager
* RollbackManager
* ValidationEngine
* ValidationPipeline
* CodeAnalyzer
* SafeApply
* GitManager

Recursos:
* análise estática;
* aplicação de patches;
* validação sintática;
* execução de testes;
* backups automáticos;
* rollback automático;
* sandbox isolada;
* promoção segura.

Status:
✅ Implementado

---

## Security Layer
Infraestrutura de governança operacional.
Componentes:
* SecurityManager
* SecurityDecision

### Engines
* PolicyEngine
* PermissionEngine
* ScopeEngine
* ApprovalEngine
* AuditEngine

### Configuração
* permissions.yaml
* scopes.yaml
* approval.yaml

### Recursos
* pipeline de validação;
* decisões centralizadas;
* auditoria operacional;
* preparação para controle de permissões;
* preparação para workflows de aprovação;
* integração transparente ao Runtime.

Status:
✅ Implementado

Observação:
A Security Layer opera em modo compatibilidade.
Nenhuma restrição operacional está ativa nesta versão.

---

## Workflow Engine
Sistema de orquestração de pipelines e automações.
Componentes:
* WorkflowManager
* WorkflowRegistry
* WorkflowEngine
* WorkflowModels
* WorkflowContext

### Recursos
* Execução assíncrona linear de tarefas;
* Catálogo estruturado de fluxos reaproveitáveis;
* Isolamento estrito de variáveis de contexto por ID único de execução;
* Integração nativa com o ActionManager e o Kernel Real do sistema.

Status:
✅ Implementado (Fase Inicial Sequencial)

---

# Arquitetura

```text
NV Runtime

├── Runtime Kernel
├── Event System
├── Action System
├── Memory Layer
├── Database Layer
├── Session Layer
├── Registry Layer
├── Provider Layer
├── Plugin Layer
├── Tool Runtime
├── Coder Engine
├── Security Layer
├── Workflow Engine
└── API Layer

## Estrutura do Projeto

core/
├── actions/
├── capabilities/
├── coder.py
├── database/
├── events/
├── memory/
├── orchestration/
├── registry/
├── runtime/
├── security/
├── sessions/
├── state/
├── tools/
└── workflows/

plugins/

interfaces/

config/

storage/

sandbox/

tests/

docs/

## Segurança de Código

Desde a versão v1.5.1 todo patch segue o fluxo:

Arquivo Original
        ↓
Sandbox
        ↓
Patch
        ↓
Validação
        ↓
Backup
        ↓
Promoção

Em caso de erro:

Sandbox
        ↓
Erro
        ↓
Remoção
        ↓
Arquivo Original Preservado

## Instalação

Clonar o projeto:

git clone <repositorio>
cd NV

Criar ambiente virtual:

python3 -m venv .venv
source .venv/bin/activate

Instalar dependências:

pip install -r requirements.txt

## Execução

Inicializar o runtime:

python main.py

## Testes

Executar testes do runtime:

python tests/test_action_manager.py
python tests/test_execute_action.py
python tests/test_memory_manager.py
python tests/test_runtime_memory.py
python tests/test_database_manager.py

Executar testes da Security Layer:

python tests/test_security_policy.py
python tests/test_security_permission.py
python tests/test_security_scope.py
python tests/test_security_approval.py
python tests/test_security_audit.py
python tests/test_security_manager.py

Executar testes do Subsistema de Workflows:

python tests/test_workflow_engine.py
python tests/test_workflow_real.py

## Roadmap

v1.9.x

Workflow Engine Inteligente & Resiliente
Objetivos:

    Desvios condicionais (If/Else) baseados em resultados de Steps;

    Políticas de tolerância a falhas (Retries e timeouts automáticos por passo);

    Persistência histórica de execuções de workflows para auditoria.

v1.10.x

API Layer
Objetivos:

    API pública;

    integração externa;

    automação remota;

    endpoints operacionais.

v2.0.0

Operational Cognitive Runtime
Objetivo:
Concluir a primeira geração do NV como plataforma operacional cognitiva completa.
Documentação

## Documentação oficial do projeto:

    FOUNDATION.md

    README.md

    CHANGELOG.md

    MILESTONE.md

    SECURITY_LAYER.md

    WORKFLOW_ENGINE.md

    PROMPT_CONTINUIDADE.md

    docs/workflows.md

## Status da Versão

Versão:
v1.8.0-workflow-engine

Status:
CONGELADA (v1.8.x concluída)

Foundation:
100% concluída

## Licença

Projeto experimental de pesquisa e desenvolvimento.

Nicky Virthy (NV)
Runtime Cognitivo Modular Local.

OMEGA DRAKON • SYSTEMS
Tecnologia que respira.