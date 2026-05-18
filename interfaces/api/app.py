from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.runtime.runtime import NickyRuntime

from core.events.event import Event
from core.events.types import EventType

runtime = NickyRuntime()


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
    await runtime.event_bus.emit(
        Event(
            type=EventType.SYSTEM_HEALTH_CHECK,
            source="api.health",
            payload={},
        )
    )

    return {
        "status": "healthy",
        "system": "NV",
    }

@app.get("/state")
async def state():
    return runtime.state_manager.get_state()
