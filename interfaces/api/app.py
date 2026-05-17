from fastapi import FastAPI

from core.state.manager import StateManager

app = FastAPI(title="NV")

state_manager = StateManager()


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.get("/state")
async def state():
    return state_manager.get_state()
