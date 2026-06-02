from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class SystemStatus(BaseModel):
    hermes_connected: bool
    live_updates: str
    allowed_roots: list[str]


@dataclass(frozen=True)
class Settings:
    allowed_roots: tuple[str, ...]


def load_settings() -> Settings:
    raw_roots = os.getenv(
        "HERMES_CONTROL_ALLOWED_ROOTS",
        "/srv/syncthing/kb-private:/srv/syncthing/kb-shared",
    )
    roots = tuple(str(Path(part).expanduser()) for part in raw_roots.split(":") if part)
    return Settings(allowed_roots=roots)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Hermes Control Center API",
        version="0.1.0",
        description="Lightweight control API for the Hermes Control Center dashboard.",
    )

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", service="hermes-control-center-api")

    @app.get("/status", response_model=SystemStatus)
    def status() -> SystemStatus:
        settings = load_settings()
        return SystemStatus(
            hermes_connected=False,
            live_updates="planned",
            allowed_roots=list(settings.allowed_roots),
        )

    return app


app = create_app()
