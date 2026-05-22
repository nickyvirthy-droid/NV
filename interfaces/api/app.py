from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.runtime.runtime import NickyRuntime

from core.events.event import Event
from core.events.types import EventType

from pydantic import BaseModel

from core.runtime.metadata import (
    RuntimeMetadata,
)

runtime = NickyRuntime()

class ActionRequest(BaseModel):
    action: str
    payload: dict

class ChatRequest(BaseModel):
    message: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    await runtime.startup()

    yield

    await runtime.shutdown()


app = FastAPI(
    title="NV",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        **RuntimeMetadata.get(),
    }

@app.get("/state")
async def state():
    return runtime.state_manager.get_state()

@app.post("/actions")
async def actions(
    request: ActionRequest,
):
    return await runtime.action_executor.execute(
        request.action,
        request.payload,
    )

@app.post("/chat")
async def chat(
    request: ChatRequest,
):
    return await runtime.chat_service.chat(
        request.message,
    )
