"""
OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: interfaces/api/server.py

Descrição:
API Layer externa baseada em FastAPI.
Expõe o Runtime de forma controlada e auditável.
Autenticação por header X-API-Key.
CORS configurável e Rate Limiting para produção.

Versão: v1.11.0

Interface Viva: Nicky Virthy
Arquiteto: Alex Projeti
"""

from __future__ import annotations

import os
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from core.runtime.kernel import RuntimeKernel
from core.workflows.models import Workflow


# ==========================================================
# Configuração via ambiente
# ==========================================================

NV_API_KEY = os.getenv("NV_API_KEY", "").strip()

# CORS
# NV_CORS_ORIGINS: lista separada por vírgula.
# Exemplos:
#   NV_CORS_ORIGINS=*                          → permite qualquer origem (dev)
#   NV_CORS_ORIGINS=https://app.exemplo.com    → produção restrita
# Se vazio → comportamento seguro: nenhuma origem externa liberada
#            (apenas same-origin / ferramentas locais).
_cors_raw = os.getenv("NV_CORS_ORIGINS", "").strip()
if _cors_raw == "*":
    CORS_ORIGINS: list[str] = ["*"]
elif _cors_raw:
    CORS_ORIGINS = [o.strip() for o in _cors_raw.split(",") if o.strip()]
else:
    CORS_ORIGINS = []

CORS_ALLOW_CREDENTIALS = (
    os.getenv("NV_CORS_ALLOW_CREDENTIALS", "false").strip().lower()
    in ("1", "true", "yes")
)

# Rate Limit
RATE_LIMIT_ENABLED = (
    os.getenv("NV_RATE_LIMIT_ENABLED", "true").strip().lower()
    in ("1", "true", "yes")
)
RATE_LIMIT_REQUESTS = int(os.getenv("NV_RATE_LIMIT_REQUESTS", "60"))
RATE_LIMIT_WINDOW = int(os.getenv("NV_RATE_LIMIT_WINDOW", "60"))  # segundos


# ==========================================================
# Autenticação
# ==========================================================

async def require_api_key(
    x_api_key: Optional[str] = Header(
        default=None,
        alias="X-API-Key",
    ),
) -> None:
    """
    Valida o header X-API-Key.
    Se NV_API_KEY não estiver definida no ambiente,
    a API opera em modo aberto (desenvolvimento).
    """
    if not NV_API_KEY:
        return

    if not x_api_key or x_api_key != NV_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key.",
            headers={"WWW-Authenticate": "API-Key"},
        )


# ==========================================================
# Rate Limiter (in-memory, fixed window)
# ==========================================================

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting simples por IP (ou X-Forwarded-For).
    Janela fixa configurável via ambiente.
    Não bloqueia /health.
    """

    def __init__(
        self,
        app,
        *,
        max_requests: int = 60,
        window_seconds: int = 60,
        enabled: bool = True,
    ):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.enabled = enabled
        # ip -> list[timestamps]
        self._hits: dict[str, list[float]] = defaultdict(list)

    def _client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        if request.client:
            return request.client.host or "unknown"
        return "unknown"

    async def dispatch(self, request: Request, call_next) -> Response:
        if not self.enabled:
            return await call_next(request)

        # Health sempre livre
        if request.url.path == "/health":
            return await call_next(request)

        ip = self._client_ip(request)
        now = time.time()
        window_start = now - self.window_seconds

        # Limpa timestamps antigos
        hits = [t for t in self._hits[ip] if t > window_start]
        self._hits[ip] = hits

        if len(hits) >= self.max_requests:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": (
                        f"Rate limit exceeded. "
                        f"Max {self.max_requests} requests "
                        f"per {self.window_seconds}s."
                    )
                },
                headers={
                    "Retry-After": str(self.window_seconds),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Window": str(self.window_seconds),
                },
            )

        self._hits[ip].append(now)
        remaining = max(0, self.max_requests - len(self._hits[ip]))

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Window"] = str(self.window_seconds)
        return response


# ==========================================================
# Runtime (singleton da API)
# ==========================================================

_kernel: Optional[RuntimeKernel] = None


def get_kernel() -> RuntimeKernel:
    global _kernel
    if _kernel is None:
        _kernel = RuntimeKernel()
    return _kernel


# ==========================================================
# Schemas
# ==========================================================

class HealthResponse(BaseModel):
    status: str
    layer: str
    version: str
    foundation: str
    auth_enabled: bool
    cors_origins: list[str]
    rate_limit_enabled: bool
    rate_limit_requests: int
    rate_limit_window: int


class WorkflowCreateResponse(BaseModel):
    message: str
    workflow_id: str


class ExecutionSummary(BaseModel):
    execution_id: str
    workflow_id: str
    status: str
    results: dict[str, Any] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)


class ActionExecuteRequest(BaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class ActionExecuteResponse(BaseModel):
    action: str
    result: Any


# ==========================================================
# App
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    kernel = get_kernel()
    if not getattr(kernel.state, "started", False):
        await kernel.boot()
    yield
    # shutdown (reservado para limpeza futura)


app = FastAPI(
    title="Nicky Virthy REST API Layer",
    version="1.11.0",
    description="Interface externa estável do Runtime Cognitivo NV.",
    lifespan=lifespan,
)

# ----------------------------------------------------------
# Middlewares (ordem importa)
# ----------------------------------------------------------

# Rate Limit (mais externo)
app.add_middleware(
    RateLimitMiddleware,
    max_requests=RATE_LIMIT_REQUESTS,
    window_seconds=RATE_LIMIT_WINDOW,
    enabled=RATE_LIMIT_ENABLED,
)

# CORS
if CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_ALLOW_CREDENTIALS,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[
            "X-RateLimit-Limit",
            "X-RateLimit-Remaining",
            "X-RateLimit-Window",
            "Retry-After",
        ],
    )


# ----------------------------------------------------------
# Health (público — sem auth)
# ----------------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
)
def health_check():
    return HealthResponse(
        status="healthy",
        layer="API Layer",
        version="1.11.0",
        foundation="100%",
        auth_enabled=bool(NV_API_KEY),
        cors_origins=CORS_ORIGINS if CORS_ORIGINS else [],
        rate_limit_enabled=RATE_LIMIT_ENABLED,
        rate_limit_requests=RATE_LIMIT_REQUESTS,
        rate_limit_window=RATE_LIMIT_WINDOW,
    )


# ----------------------------------------------------------
# Workflows (protegidos)
# ----------------------------------------------------------

@app.get(
    "/workflows",
    dependencies=[Depends(require_api_key)],
)
def list_workflows():
    kernel = get_kernel()
    return {"workflows": kernel.workflows.list()}


@app.get(
    "/workflows/{workflow_id}",
    dependencies=[Depends(require_api_key)],
)
def get_workflow(workflow_id: str):
    kernel = get_kernel()
    workflow = kernel.workflows.get(workflow_id)

    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow not found: {workflow_id}",
        )

    return workflow


@app.post(
    "/workflows",
    response_model=WorkflowCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
def create_workflow(workflow: Workflow):
    kernel = get_kernel()
    kernel.workflows.register(workflow)

    return WorkflowCreateResponse(
        message=f"Workflow {workflow.workflow_id} registered.",
        workflow_id=workflow.workflow_id,
    )


@app.post(
    "/workflows/{workflow_id}/execute",
    response_model=ExecutionSummary,
    dependencies=[Depends(require_api_key)],
)
async def execute_workflow(workflow_id: str):
    kernel = get_kernel()

    workflow = kernel.workflows.get(workflow_id)
    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workflow not found: {workflow_id}",
        )

    try:
        execution = await kernel.workflows.execute(workflow_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return ExecutionSummary(
        execution_id=execution.execution_id,
        workflow_id=execution.workflow_id,
        status=execution.status,
        results=execution.results,
        errors=execution.errors,
    )


# ----------------------------------------------------------
# Executions (protegidos)
# ----------------------------------------------------------

@app.get(
    "/executions",
    dependencies=[Depends(require_api_key)],
)
def list_executions(limit: int = 50):
    kernel = get_kernel()
    executions = kernel.workflows.list_executions(limit=limit)

    items = []
    for e in executions:
        if isinstance(e, dict):
            items.append(
                {
                    "execution_id": e.get("execution_id"),
                    "workflow_id": e.get("workflow_id"),
                    "status": e.get("status"),
                }
            )
        else:
            items.append(
                {
                    "execution_id": e.execution_id,
                    "workflow_id": e.workflow_id,
                    "status": e.status,
                }
            )

    return {"executions": items}


@app.get(
    "/executions/{execution_id}",
    response_model=ExecutionSummary,
    dependencies=[Depends(require_api_key)],
)
def get_execution(execution_id: str):
    kernel = get_kernel()
    execution = kernel.workflows.get_execution(execution_id)

    if execution is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Execution not found: {execution_id}",
        )

    return ExecutionSummary(
        execution_id=execution.execution_id,
        workflow_id=execution.workflow_id,
        status=execution.status,
        results=getattr(execution, "results", {}) or {},
        errors=getattr(execution, "errors", []) or [],
    )


# ----------------------------------------------------------
# Actions (protegidos)
# ----------------------------------------------------------

@app.get(
    "/actions",
    dependencies=[Depends(require_api_key)],
)
def list_actions():
    kernel = get_kernel()
    return {"actions": kernel.actions.registry.list()}


@app.get(
    "/actions/{action_name}",
    dependencies=[Depends(require_api_key)],
)
def get_action(action_name: str):
    kernel = get_kernel()
    action = kernel.actions.registry.get(action_name)

    if action is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action not found: {action_name}",
        )

    if hasattr(action, "model_dump"):
        return action.model_dump()
    if hasattr(action, "dict"):
        return action.dict()
    if isinstance(action, dict):
        return action

    return {
        "name": action_name,
        "type": type(action).__name__,
    }


@app.post(
    "/actions/{action_name}/execute",
    response_model=ActionExecuteResponse,
    dependencies=[Depends(require_api_key)],
)
async def execute_action(
    action_name: str,
    body: ActionExecuteRequest | None = None,
):
    kernel = get_kernel()

    if kernel.actions.registry.get(action_name) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action not found: {action_name}",
        )

    payload = body.payload if body else {}

    try:
        result = await kernel.actions.execute(
            action_name=action_name,
            payload=payload,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return ActionExecuteResponse(
        action=action_name,
        result=result,
    )
