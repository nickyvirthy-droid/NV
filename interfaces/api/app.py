from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.runtime.runtime import NickyRuntime

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
    return {
        "status": "healthy",
        "system": "NV",
    }


@app.get("/state")
async def state():
    return runtime.state_manager.get_state()
