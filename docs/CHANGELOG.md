CHANGELOG
Projeto: Nicky Virthy (NV)

Histórico Oficial de Versões

---

v1.11.0-operational-hardening
Data: Agosto/2026
Status: CONCLUÍDA / HOMOLOGADA

Objetivo
Completar a sequência pós-Foundation: enforcement de segurança configurável,
métricas de workflow, templates/import-export, hardening da API e implantação
systemd com porta oficial.

Implementado

Security Layer (modo restritivo)
- enforcement.yaml (compatibility | soft | strict)
- Permission Engine com avaliação real via permissions.yaml
- Scope Engine com avaliação real via scopes.yaml
- Audit enriquecido (mode + engine)
- Default permanece compatibility (zero breaking change)

Workflow Metrics
- metrics.py (total, success, failed, duration, depth, por workflow)
- Integração automática no WorkflowManager / engines
- finished_at preenchido ao final das execuções
- API: get_metrics_summary, get_workflow_metrics, get_recent_executions

Templates / Import-Export
- serializer.py (YAML / JSON, arquivo, string, dict, diretório)
- templates.py (catálogo oficial: system_diagnostics, filesystem_snapshot, empty)
- API no Manager: export/import + list/instantiate/load templates

API Layer Hardening
- CORS configurável (NV_CORS_ORIGINS)
- Rate Limit in-memory (NV_RATE_LIMIT_*)
- Health expõe estado de CORS e Rate Limit
- Versão da API: 1.11.0

Implantação
- nv-api.service (systemd, porta oficial 7001)
- nv-api.env.example
- API_DEPLOY.md

Homologação
- Suite crítica: 48/48 PASSED
- Dependências: PyYAML, pytest-asyncio

Resultado
Runtime operacional, seguro e implantável em produção.
Sequência pós-Foundation 100% concluída.

---

v1.10.0-api-layer
Data: Agosto/2026
Status: CONCLUÍDA / HOMOLOGADA

Objetivo
Expor o Runtime via API REST controlada, com autenticação e endpoints operacionais.

Implementado
- interfaces/api/server.py (FastAPI + lifespan)
- Autenticação por header X-API-Key (NV_API_KEY)
- Endpoints de Workflows (list / get / create / execute)
- Endpoints de Executions (list / get)
- Endpoints de Actions (list / get / execute)
- Health público com indicador auth_enabled
- Suite formal tests/test_api_layer.py (14/14 PASSED)

Resultado
API Layer operacional sobre o Runtime real.
Foundation 100% concluída.

---

v1.9.2-nested-workflows
Data: Agosto/2026
Status: CONCLUÍDA / HOMOLOGADA

Objetivo
Completar o Workflow Engine com Nested Workflows, proteção de pilha e limpeza técnica.

Implementado / Corrigido
- WorkflowStack alinhado (enter/leave/contains/clear)
- DAG Engine estabilizado (stages + parallel + _inputs)
- Nested Workflows homologados
- Proteção de recursão e profundidade máxima
- Eliminação de datetime.utcnow() (timezone.utc)
- Suite de testes DAG + Nested: 13/13 PASSED

Resultado
Workflow Engine completo (Linear + DAG + Nested + Scheduler).
Foundation em 99%.

---
