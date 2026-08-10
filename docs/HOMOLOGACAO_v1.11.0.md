HOMOLOGAÇÃO v1.11.0
Projeto: Nicky Virthy (NV)

Documento Oficial de Homologação
Data: Agosto/2026
Status: AGUARDANDO EXECUÇÃO NO SERVIDOR


================================================================
1. OBJETIVO
================================================================

Validar que a sequência pós-Foundation (itens 1–5) não quebrou
o Runtime e que as novas capacidades estão operacionais.

Somente após todos os blocos PASS pode-se fechar a versão.


================================================================
2. AMBIENTE
================================================================

Servidor: nickyserver
Path:     ~/NV
Python:   venv ativo
Banco:    MariaDB (nicky_db / nicky_test_db)
Comando base:

  cd ~/NV
  source venv/bin/activate


================================================================
3. BLOCO A — REGRESSÃO (deve continuar passando)
================================================================

# Suite completa (recomendado)
pytest tests/ -v --tb=short 2>&1 | tee /tmp/nv_homolog_full.log

# Ou por grupos críticos:

# A1. Security Layer (legado)
pytest tests/test_security_*.py -v --tb=short

# A2. Workflow Engine (Linear + DAG + Nested + Scheduler)
pytest tests/test_workflow_*.py tests/test_workflows.py -v --tb=short

# A3. API Layer
pytest tests/test_api_layer.py -v --tb=short

# A4. Actions / Runtime core
pytest tests/test_action*.py tests/test_kernel*.py tests/test_runtime*.py -v --tb=short

Critério de sucesso: 0 failures nos testes existentes.


================================================================
4. BLOCO B — NOVAS CAPACIDADES (v1.11.0)
================================================================

Estes testes precisam ser criados ou executados manualmente
se ainda não existirem arquivos dedicados.

----------------------------------------------------------------
B1. Security Enforcement (Item 1)
----------------------------------------------------------------

Arquivos envolvidos:
  core/security/manager.py
  core/security/permission_engine.py
  core/security/scope_engine.py
  config/security/enforcement.yaml

Checklist manual / script:

  [ ] mode=compatibility → todas as actions liberadas
  [ ] mode=soft          → avalia + audita, NÃO bloqueia
  [ ] mode=strict        → bloqueia permission_denied e scope_denied
  [ ] guest + filesystem_delete → denied em strict
  [ ] admin + filesystem_delete → allowed
  [ ] system_exec com comando fora de allowed_commands → denied
  [ ] system_exec com ls → allowed
  [ ] SecurityManager.reload() recarrega YAMLs

Comando sugerido (quando existir):
  pytest tests/test_security_enforcement.py -v


----------------------------------------------------------------
B2. Workflow Metrics (Item 2)
----------------------------------------------------------------

Arquivos:
  core/workflows/metrics.py
  core/workflows/manager.py
  core/workflows/engine.py
  core/workflows/dag_engine.py

Checklist:

  [ ] Após execute_workflow com sucesso → metrics.success incrementa
  [ ] Após falha → metrics.failed incrementa
  [ ] get_metrics_summary() retorna total, success_rate, avg duration
  [ ] get_workflow_metrics(workflow_id) retorna stats do fluxo
  [ ] get_recent_executions() retorna histórico
  [ ] finished_at é preenchido ao final da execução
  [ ] Nested workflows registram depth corretamente

Comando sugerido:
  pytest tests/test_workflow_metrics.py -v


----------------------------------------------------------------
B3. Templates + Import/Export (Item 3)
----------------------------------------------------------------

Arquivos:
  core/workflows/serializer.py
  core/workflows/templates.py
  core/workflows/manager.py

Checklist:

  [ ] export_workflow(id, format="yaml") retorna string válida
  [ ] export_workflow_to_file grava arquivo
  [ ] import_workflow(arquivo) registra e retorna Workflow
  [ ] export_all_to_directory / import_directory round-trip
  [ ] list_templates() retorna IDs oficiais
  [ ] instantiate_template(...) cria e registra cópia
  [ ] load_all_templates() registra todos

Comando sugerido:
  pytest tests/test_workflow_serializer.py tests/test_workflow_templates.py -v


----------------------------------------------------------------
B4. CORS + Rate Limit (Item 4)
----------------------------------------------------------------

Arquivo:
  interfaces/api/server.py

Checklist (manual com curl / httpx):

  [ ] GET /health → 200 e contém cors_origins + rate_limit_*
  [ ] Sem NV_CORS_ORIGINS → CORS restrito (sem Access-Control-Allow-Origin amplo)
  [ ] Com NV_CORS_ORIGINS=https://exemplo.com → header correto
  [ ] Rate limit: após N requests → 429 + Retry-After
  [ ] /health isento de rate limit
  [ ] Headers X-RateLimit-Limit / Remaining presentes

Teste rápido:
  for i in $(seq 1 70); do curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:7001/workflows; done


----------------------------------------------------------------
B5. systemd / Porta oficial (Item 5)
----------------------------------------------------------------

Arquivos:
  nv-api.service
  nv-api.env.example

Checklist:

  [ ] sudo systemctl start nv-api → active (running)
  [ ] curl http://127.0.0.1:7001/health → 200
  [ ] journalctl -u nv-api -n 20 → sem erros de boot
  [ ] Porta 7001 escutando (ss -tlnp | grep 7001)
  [ ] NV_API_KEY protege endpoints (401 sem chave)
  [ ] Reinício do serviço recupera limpo


================================================================
5. COMANDO ÚNICO DE REGRESSÃO (copiar e colar)
================================================================

cd ~/NV && source venv/bin/activate && \
pytest tests/ -v --tb=line 2>&1 | tee /tmp/nv_homolog_v1.11.log && \
echo "==== RESUMO ====" && \
tail -20 /tmp/nv_homolog_v1.11.log


================================================================
6. CRITÉRIO DE FECHAMENTO
================================================================

A versão v1.11.0 só pode ser fechada quando:

  1. Bloco A (regressão) = 0 failures
  2. Bloco B (novas capacidades) = todos os checks PASS
  3. nv-api.service estável
  4. Documentação atualizada (CHANGELOG, MILESTONE, FOUNDATION)

Após isso:
  - Commit final
  - Tag v1.11.0
  - Atualizar docs oficiais
  - Abrir próxima milestone


================================================================
7. RELATÓRIO ESPERADO
================================================================

Envie o resultado no formato:

  BLOCO A: X passed / Y failed
  BLOCO B1 Security: PASS/FAIL + observações
  BLOCO B2 Metrics: PASS/FAIL
  BLOCO B3 Templates: PASS/FAIL
  BLOCO B4 CORS/Rate: PASS/FAIL
  BLOCO B5 systemd: PASS/FAIL

  Falhas (se houver):
  - arquivo / teste / mensagem de erro


OMEGA DRAKON • SYSTEMS
Tecnologia que respira.
