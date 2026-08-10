"""
OMEGA DRAKON • SYSTEMS

Teste formal da API Layer (v1.10.0)

Cobertura:
- Health (público)
- Autenticação X-API-Key (401 / 200)
- Listagem de workflows
- Execução de workflow
"""

import os

import pytest
from fastapi.testclient import TestClient


# ----------------------------------------------------------
# Fixtures
# ----------------------------------------------------------

TEST_API_KEY = "test-nicky-api-key-2026"


@pytest.fixture(scope="module")
def client():
    """
    Sobe o app com NV_API_KEY definida
    e retorna um TestClient.
    """
    os.environ["NV_API_KEY"] = TEST_API_KEY

    # Importa depois de setar a env para o módulo ler a chave
    from interfaces.api import server as api_server

    # Garante que o módulo usa a chave de teste
    api_server.NV_API_KEY = TEST_API_KEY

    with TestClient(api_server.app) as c:
        yield c

    # Limpa
    os.environ.pop("NV_API_KEY", None)


def auth_headers():
    return {"X-API-Key": TEST_API_KEY}


# ----------------------------------------------------------
# Health
# ----------------------------------------------------------

def test_health_public(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["layer"] == "API Layer"
    assert data["version"] == "1.11.0"
    assert data["auth_enabled"] is True


# ----------------------------------------------------------
# Autenticação
# ----------------------------------------------------------

def test_workflows_without_key_returns_401(client):
    response = client.get("/workflows")
    assert response.status_code == 401


def test_workflows_with_invalid_key_returns_401(client):
    response = client.get(
        "/workflows",
        headers={"X-API-Key": "chave-invalida"},
    )
    assert response.status_code == 401


def test_workflows_with_valid_key_returns_200(client):
    response = client.get(
        "/workflows",
        headers=auth_headers(),
    )
    assert response.status_code == 200

    data = response.json()
    assert "workflows" in data
    assert isinstance(data["workflows"], list)


# ----------------------------------------------------------
# Workflows
# ----------------------------------------------------------

def test_list_includes_system_diagnostics(client):
    response = client.get(
        "/workflows",
        headers=auth_headers(),
    )
    assert response.status_code == 200

    workflows = response.json()["workflows"]
    assert "system_diagnostics" in workflows


def test_get_workflow_not_found(client):
    response = client.get(
        "/workflows/nao_existe",
        headers=auth_headers(),
    )
    assert response.status_code == 404


def test_get_system_diagnostics(client):
    response = client.get(
        "/workflows/system_diagnostics",
        headers=auth_headers(),
    )
    assert response.status_code == 200

    data = response.json()
    assert data["workflow_id"] == "system_diagnostics"
    assert "steps" in data


# ----------------------------------------------------------
# Execução
# ----------------------------------------------------------

def test_execute_system_diagnostics(client):
    response = client.post(
        "/workflows/system_diagnostics/execute",
        headers=auth_headers(),
    )
    assert response.status_code == 200

    data = response.json()
    assert data["workflow_id"] == "system_diagnostics"
    assert data["status"] == "COMPLETED"
    assert "execution_id" in data
    assert isinstance(data["results"], dict)
    assert len(data["results"]) > 0
    assert data["errors"] == []


def test_execute_unknown_workflow_returns_404(client):
    response = client.post(
        "/workflows/workflow_inexistente/execute",
        headers=auth_headers(),
    )
    assert response.status_code == 404


# ----------------------------------------------------------
# Executions
# ----------------------------------------------------------

def test_list_executions(client):
    # Garante pelo menos uma execução
    client.post(
        "/workflows/system_diagnostics/execute",
        headers=auth_headers(),
    )

    response = client.get(
        "/executions",
        headers=auth_headers(),
    )
    assert response.status_code == 200

    data = response.json()
    assert "executions" in data
    assert isinstance(data["executions"], list)

# ----------------------------------------------------------
# Actions
# ----------------------------------------------------------

def test_list_actions(client):
    response = client.get("/actions", headers=auth_headers())
    assert response.status_code == 200

    data = response.json()
    assert "actions" in data
    assert isinstance(data["actions"], list)
    assert "system_info" in data["actions"]
    assert "cpu_info" in data["actions"]


def test_get_action_not_found(client):
    response = client.get(
        "/actions/action_inexistente",
        headers=auth_headers(),
    )
    assert response.status_code == 404


def test_execute_action_system_info(client):
    response = client.post(
        "/actions/system_info/execute",
        headers=auth_headers(),
        json={"payload": {}},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["action"] == "system_info"
    assert "result" in data
    assert data["result"] is not None


def test_execute_action_without_key_returns_401(client):
    response = client.post(
        "/actions/system_info/execute",
        json={"payload": {}},
    )
    assert response.status_code == 401
