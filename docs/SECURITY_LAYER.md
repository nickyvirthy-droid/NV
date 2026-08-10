SECURITY_LAYER
Projeto: Nicky Virthy (NV)

Versão: v1.11.0-security-enforcement
Data: Agosto/2026
Status: EM EVOLUÇÃO


Visão Geral
A Security Layer é a infraestrutura responsável pela governança operacional do NV Runtime.

Seu objetivo é fornecer um ponto central de validação para todas as operações executadas pelo sistema.

A camada foi projetada para evoluir sem quebrar compatibilidade, permitindo a ativação gradual de:

permissões;
escopos;
aprovações;
auditoria;
políticas operacionais.


Objetivos
A Security Layer existe para:

validar solicitações antes da execução;
centralizar regras de segurança;
registrar decisões operacionais;
permitir futuras políticas RBAC;
preparar o Runtime para ambientes multiusuário;
suportar workflows de aprovação;
fornecer rastreabilidade operacional.


Arquitetura
Fluxo atual:

Action Request
        ↓
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

A execução de uma Action somente ocorre após a passagem por toda a pipeline de validação
(quando o modo de enforcement exige bloqueio).


Enforcement Configurável (v1.11.0)

Arquivo:
config/security/enforcement.yaml

Modos disponíveis:

| Mode            | Comportamento                                      |
|-----------------|----------------------------------------------------|
| compatibility   | Tudo liberado (estado legado / default)            |
| soft            | Avalia + audita, nunca bloqueia                    |
| strict          | Avalia + bloqueia quando Policy/Permission/Scope negar |

Controles individuais:

- policy: true/false
- permission: true/false
- scope: true/false
- approval: true/false   (ainda desativado por padrão)
- fail_closed: true/false
- default_role: admin

Comportamento:

- compatibility → engines retornam allowed=True (compatibilidade total)
- soft          → engines avaliam regras reais e registram no Audit, mas o Manager não bloqueia
- strict        → engines avaliam regras reais; Manager bloqueia se fail_closed=true


SecurityManager
Responsável por coordenar toda a Security Layer.

Arquivo:
core/security/manager.py

Funções:
- orquestrar engines;
- carregar enforcement.yaml;
- consolidar decisões conforme o modo;
- registrar auditoria;
- fornecer interface única ao Runtime;
- permitir reload() das configurações.

Status:
✅ Implementado (enforcement configurável)


SecurityDecision
Objeto padrão utilizado pela camada de segurança.

Arquivo:
core/security/models.py

Campos:
- allowed
- reason
- engine
- mode

Status:
✅ Implementado


Policy Engine
Arquivo:
core/security/policy_engine.py

Responsável por:
- validações globais;
- políticas operacionais;
- decisões iniciais.

Status:
✅ Implementado

Modo Atual:
Compatibilidade (estrutura pronta para regras futuras).


Permission Engine
Arquivo:
core/security/permission_engine.py

Responsável por:
- permissões operacionais por role;
- validação de acesso usando permissions.yaml;
- hierarquia read < write < admin.

Status:
✅ Implementado

Modo Atual:
Avaliação real quando mode != compatibility.


Scope Engine
Arquivo:
core/security/scope_engine.py

Responsável por:
- delimitação de escopo (paths, commands, tables);
- restrições operacionais via scopes.yaml;
- validação contextual do payload.

Status:
✅ Implementado

Modo Atual:
Avaliação real quando mode != compatibility.


Approval Engine
Arquivo:
core/security/approval_engine.py

Responsável por:
- aprovações manuais;
- workflows de autorização;
- validação de operações críticas.

Status:
✅ Implementado (infraestrutura)

Modo Atual:
Desativado por padrão (approval: false).
Ativação futura controlada pelo enforcement.yaml.


Audit Engine
Arquivo:
core/security/audit_engine.py

Responsável por:
- registrar eventos;
- rastrear decisões;
- produzir histórico operacional em memória.

Status:
✅ Implementado

Persistência futura planejada (Database Layer).


Configuração
Diretório:
config/security/

Arquivos:
- enforcement.yaml   → modo e flags de enforcement
- permissions.yaml   → mapa de permissões por role + actions
- scopes.yaml        → restrições de path / command / table
- approval.yaml      → ações que exigem aprovação


Integração com o Runtime
A Security Layer permanece integrada ao Runtime sem alterar o comportamento existente
enquanto o mode = compatibility.

Benefícios:
- compatibilidade preservada;
- ativação gradual sem breaking change;
- desacoplamento da lógica de segurança;
- hot-reload via SecurityManager.reload().


Modo Compatibilidade (default)
Nenhuma Action é bloqueada.
Nenhuma aprovação é exigida.
Nenhuma restrição de escopo é aplicada.
Todas as engines retornam decisões permissivas.

Objetivo:
Garantir migração segura da arquitetura.


Testes
Arquivos planejados / existentes:
tests/test_security_policy.py
tests/test_security_permission.py
tests/test_security_scope.py
tests/test_security_approval.py
tests/test_security_audit.py
tests/test_security_manager.py
tests/test_security_enforcement.py  (novo)


Estrutura da Security Layer
core/security/
├── __init__.py
├── exceptions.py
├── manager.py
├── models.py
├── roles.py
├── policy_engine.py
├── permission_engine.py
├── scope_engine.py
├── approval_engine.py
├── audit_engine.py
└── audit_models.py

config/security/
├── enforcement.yaml
├── permissions.yaml
├── scopes.yaml
└── approval.yaml


Roadmap restante (desta frente)
- Testes formais do enforcement (compatibility / soft / strict)
- Persistência de Audit no Database Layer
- Workflow real de Approval
- Security Reports


Resultado da v1.11.0-security-enforcement
Entregue:
- Enforcement configurável (compatibility | soft | strict)
- Permission Engine com avaliação real
- Scope Engine com avaliação real
- Audit enriquecido (mode + engine)
- Configuração centralizada em enforcement.yaml
- Compatibilidade total preservada (default = compatibility)

Quebras de API:
Nenhuma


Estado Atual
Versão:
v1.11.0-security-enforcement (em evolução)

Status:
Item 1 da sequência pós-Foundation

Próximo Item:
Métricas de Workflow


OMEGA DRAKON • SYSTEMS
Tecnologia que respira.
