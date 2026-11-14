"""FastAPI entrypoint and synthetic WebSocket telemetry stream."""
from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .api import router
from .config import load_settings
from .database import close_engine
from .telemetry import TelemetryHub, simulated_samples


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_engine()


settings = load_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "x-research-role"],
)
app.include_router(router)
hub = TelemetryHub(max_clients=settings.max_telemetry_clients)


@app.get("/health")
async def health() -> dict[str, object]:
    return {"status": "ok", "service": "lpbf-research", "version": "0.1.0"}


@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket) -> None:
    await hub.join(websocket)
    try:
        async for observation in simulated_samples():
            await websocket.send_json(observation)
    except (WebSocketDisconnect, RuntimeError, OSError):
        return
    finally:
        await hub.leave(websocket)
