"""Runtime configuration; no hardcoded credentials."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "LPBF Build Qualification Research"
    environment: str = "development"
    database_url: str = "sqlite+aiosqlite:///:memory:"
    allowed_origins: tuple[str, ...] = ("http://localhost:3000",)
    max_telemetry_clients: int = 120
    telemetry_interval_seconds: float = 1.5


def load_settings() -> Settings:
    raw_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000")
    return Settings(
        environment=os.environ.get("APP_ENV", "development"),
        database_url=os.environ.get(
            "DATABASE_URL", "sqlite+aiosqlite:///:memory:"
        ),
        allowed_origins=tuple(
            origin.strip() for origin in raw_origins.split(",") if origin.strip()
        ),
    )
