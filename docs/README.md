Nicky Virthy (NV)
Runtime Cognitivo Modular para execução local de agentes inteligentes, automação operacional e evolução controlada.

Versão Atual: v1.11.0-operational-hardening
Status: Foundation + Hardening Homologados
Última Atualização: Agosto/2026


Visão Geral
O Nicky Virthy (NV) é uma plataforma modular desenvolvida para funcionar como um Runtime Cognitivo Local.

Seu objetivo é fornecer uma infraestrutura capaz de combinar:

memória persistente;
gerenciamento de sessões;
sistema de eventos;
execução de ações;
integração com modelos de linguagem;
persistência em banco de dados;
plugins extensíveis;
automação operacional;
evolução segura de código;
execução controlada de ferramentas operacionais;
governança operacional e segurança;
orquestração de workflows automatizados.

O projeto foi concebido para evoluir gradualmente de um runtime inteligente para uma plataforma operacional cognitiva completa.


Estado Atual
Versão: v1.11.0-operational-hardening

Foundation: 100% concluída.
Hardening pós-Foundation: 100% concluído e homologado (48/48).

Status Geral:

Runtime estabilizado;
Tool Runtime concluído;
Security Layer com enforcement configurável;
Workflow Engine completo (Linear + DAG + Nested + Scheduler + Metrics + Templates);
API Layer com CORS, Rate Limit e porta oficial 7001 (nv-api.service).


Capacidades Implementadas
Runtime Kernel
Responsável pelo ciclo de vida do sistema.

Recursos:

bootstrap do runtime;
gerenciamento de serviços;
coordenação de módulos;
carregamento de componentes.

Status: ✅ Implementado


Event System
Sistema interno de eventos.

Recursos:

publicação de eventos;
assinatura de eventos;
comunicação desacoplada.

Status: ✅ Implementado


Action System
Camada responsável pela execução de capacidades operacionais.

Componentes:

ActionManager
ActionRegistry
ActionContext
ActionResolver

Recursos:

registro de ações;
descoberta de ações;
execução controlada.

Status: ✅ Implementado


Memory Layer
Sistema de memória persistente e contextual.

Componentes:

MemoryManager
ProfileMemory
RuntimeMemory
Fact Extraction
Resolver

Recursos:

armazenamento persistente;
recuperação contextual;
gerenciamento de perfil;
resolução de informações.

Status: ✅ Implementado


Database Layer
Infraestrutura de persistência.

Componentes:

DatabaseConnection
DatabaseManager
Repositories
Migrations

Recursos:

MariaDB nativo;
acesso estruturado;
persistência de runtime;
reutilização por ferramentas operacionais.

Status: ✅ Implementado


Session Layer
Gerenciamento de sessões operacionais.

Componentes:

SessionManager
SessionHistory

Recursos:

histórico;
rastreamento;
contexto temporal.

Status: ✅ Implementado


Registry Layer
Container interno de serviços.

Recursos:

registro de serviços;
resolução de dependências;
compartilhamento de componentes.

Status: ✅ Implementado


Provider Layer
Integração com provedores de IA.

Recursos:

abstração de providers;
integração Ollama;
expansão futura para múltiplos modelos.

Status: ✅ Implementado


Plugin Layer
Sistema de extensibilidade.

Recursos:

carregamento dinâmico;
descoberta automática;
expansão modular.

Status: ✅ Implementado


Tool Runtime
Primeira geração operacional concluída.

Total atual: 56 Actions Operacionais.
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

Status: ✅ Implementado


Coder Engine
Sistema de modificação segura de código.

Componentes:

FileInspector
SandboxManager
BackupManager
RollbackManager
ValidationEngine
ValidationPipeline
CodeAnalyzer
SafeApply
GitManager

Recursos:

análise estática;
aplicação de patches;
validação sintática;
execução de testes;
backups automáticos;
rollback automático;
sandbox isolada;
promoção segura.

Status: ✅ Implementado


Security Layer
Infraestrutura de governança operacional.

Componentes:

SecurityManager
SecurityDecision
PolicyEngine
PermissionEngine
ScopeEngine
ApprovalEngine
AuditEngine

Configuração:

permissions.yaml
scopes.yaml
approval.yaml

Recursos:

pipeline de validação;
decisões centralizadas;
auditoria operacional;
preparação para controle de permissões;
preparação para workflows de aprovação;
integração transparente ao Runtime.

Status: ✅ Implementado


Workflow Engine
Sistema de orquestração de pipelines e automações.

Componentes:

WorkflowManager
WorkflowRegistry
WorkflowEngine
WorkflowModels
WorkflowContext
WorkflowRepository
WorkflowHistory

Recursos:

execução assíncrona de workflows;
persistência de execuções;
histórico de execuções;
contexto isolado por execução;
condicionais;
desvio de fluxo;
retries automáticos;
timeouts por etapa;
eventos de execução;
integração nativa com ActionManager.

Status: ✅ Implementado


Arquitetura
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


Estrutura do Projeto
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


Segurança de Código
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


Instalação
git clone <repositorio>

cd NV

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt


Execução
python main.py


Testes
pytest tests -v


Roadmap
v1.9.0
API Layer

Objetivos:

API pública;
autenticação;
API Keys;
endpoints operacionais;
integração externa;
automação remota.


v2.0.0
Operational Cognitive Runtime

Objetivo:

Concluir a primeira geração do NV como plataforma operacional cognitiva completa.


Documentação
FOUNDATION.md
README.md
CHANGELOG.md
MILESTONE.md
SECURITY_LAYER.md
WORKFLOW_ENGINE.md
PROMPT_CONTINUIDADE.md
docs/workflows.md


Status da Versão
Versão: v1.8-final

Status: CONGELADA

Foundation: 100% concluída.


Licença
Projeto experimental de pesquisa e desenvolvimento.

Nicky Virthy (NV) Runtime Cognitivo Modular Local.

OMEGA DRAKON • SYSTEMS Tecnologia que respira.

