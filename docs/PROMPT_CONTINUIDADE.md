PROMPT_CONTINUIDADE.md
Projeto: Nicky Virthy (NV)

Versão Atual: v1.11.0-operational-hardening
Data de Referência: Agosto/2026
Status da Foundation: 100% Concluída
Status do Hardening: 100% Concluído / Homologado


CONTINUIDADE DO PROJETO
Antes de qualquer alteração, leia:
docs/README.md
docs/CHANGELOG.md
docs/FOUNDATION.md
docs/MILESTONE.md
docs/SECURITY_LAYER.md
docs/PROMPT_CONTINUIDADE.md
docs/API_DEPLOY.md
docs/HOMOLOGACAO_v1.11.0.md


ESTADO ATUAL
Versão: v1.11.0-operational-hardening
Status: ESTÁVEL / HOMOLOGADA
Foundation: 100%
Hardening pós-Foundation: 100%
Suite crítica: 48/48 PASSED


ARQUITETURA
NV Runtime
├── Runtime Kernel
├── Event System
├── Registry / Session / Database / Memory
├── Provider / Plugin
├── Coder Engine
├── Tool Runtime
├── Security Layer (enforcement: compatibility | soft | strict)
├── Workflow Engine (Linear + DAG + Nested + Scheduler + Metrics + Templates)
└── API Layer (FastAPI + X-API-Key + CORS + Rate Limit)


API LAYER
Porta oficial: 7001
Base URL local: http://127.0.0.1:7001
Auth: header X-API-Key (env NV_API_KEY)
Health: GET /health (público)
Serviço systemd: nv-api.service

Endpoints protegidos:
- GET/POST /workflows
- GET /workflows/{id}
- POST /workflows/{id}/execute
- GET /executions
- GET /executions/{id}
- GET /actions
- GET /actions/{name}
- POST /actions/{name}/execute

CORS: NV_CORS_ORIGINS
Rate Limit: NV_RATE_LIMIT_ENABLED / REQUESTS / WINDOW


SEQUÊNCIA PÓS-FOUNDATION
1. Security Layer – modo restritivo          ✅ Homologado
2. Métricas de Workflow                      ✅ Homologado
3. Templates / Import-Export YAML-JSON       ✅ Homologado
4. CORS e rate limit em produção             ✅ Homologado
5. Integração systemd / porta oficial        ✅ Homologado


DEPENDÊNCIAS RELEVANTES
- PyYAML>=6.0
- pytest-asyncio (testes)
- FastAPI / uvicorn


PRÓXIMOS PASSOS SUGERIDOS
- Limpeza de datetime.utcnow() nos testes do scheduler
- Persistência de Audit no Database Layer
- Workflow real de Approval
- Security Reports
- Evolução incremental em direção a v2.0.0-operational-cognitive-runtime


REGRAS
Não quebrar Runtime, Tool Runtime, Security, Coder, Workflows nem API pública.
Evoluir de forma incremental.
Default de segurança permanece compatibility até ativação explícita.


OMEGA DRAKON • SYSTEMS
Tecnologia que respira.
