from __future__ import annotations

import os
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{12,}"),
    re.compile(r"gho_[A-Za-z0-9_]{12,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[^\s'\"]+"),
]


class HealthResponse(BaseModel):
    status: str
    service: str


class SystemStatus(BaseModel):
    hermes_connected: bool
    live_updates: str
    allowed_roots: list[str]
    state_db: str | None
    session_count: int
    active_session_count: int
    latest_activity_at: str | None


class SessionSummary(BaseModel):
    id: str
    title: str
    source: str
    model: str | None
    started_at: str | None
    last_activity_at: str | None
    message_count: int
    tool_call_count: int
    preview: str


class MessageSummary(BaseModel):
    id: int
    session_id: str
    role: str
    tool_name: str | None
    timestamp: str | None
    content: str


class SessionDetail(SessionSummary):
    messages: list[MessageSummary]


class ApprovalSummary(BaseModel):
    id: str
    status: str
    message: str


@dataclass(frozen=True)
class Settings:
    allowed_roots: tuple[str, ...]
    state_db: Path


def load_settings() -> Settings:
    raw_roots = os.getenv(
        "HERMES_CONTROL_ALLOWED_ROOTS",
        "/srv/syncthing/kb-private:/srv/syncthing/kb-shared",
    )
    roots = tuple(str(Path(part).expanduser()) for part in raw_roots.split(":") if part)
    state_db = Path(os.getenv("HERMES_STATE_DB", "~/.hermes/state.db")).expanduser()
    return Settings(allowed_roots=roots, state_db=state_db)


def redact(text: str | None) -> str:
    if not text:
        return ""
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def compact(text: str | None, limit: int = 220) -> str:
    safe = redact(text).strip()
    if len(safe) <= limit:
        return safe
    return safe[: limit - 1].rstrip() + "…"


def iso_timestamp(value: float | int | None) -> str | None:
    if value is None:
        return None
    return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat()


def connect_state_db(settings: Settings) -> sqlite3.Connection:
    if not settings.state_db.exists():
        raise HTTPException(status_code=503, detail=f"Hermes state database not found: {settings.state_db}")
    conn = sqlite3.connect(f"file:{settings.state_db}?mode=ro&immutable=1", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def session_summary_from_row(row: sqlite3.Row) -> SessionSummary:
    title = row["title"] or "Untitled session"
    preview = compact(row["preview"], 260)
    return SessionSummary(
        id=row["id"],
        title=title,
        source=row["source"],
        model=row["model"],
        started_at=iso_timestamp(row["started_at"]),
        last_activity_at=iso_timestamp(row["last_activity_at"] or row["started_at"]),
        message_count=row["message_count"] or 0,
        tool_call_count=row["tool_call_count"] or 0,
        preview=preview,
    )


def message_summary_from_row(row: sqlite3.Row, limit: int = 1200) -> MessageSummary:
    content = redact(row["content"] or "")
    if len(content) > limit:
        content = content[: limit - 1].rstrip() + "…"
    return MessageSummary(
        id=row["id"],
        session_id=row["session_id"],
        role=row["role"],
        tool_name=row["tool_name"],
        timestamp=iso_timestamp(row["timestamp"]),
        content=content,
    )


def create_app() -> FastAPI:
    app = FastAPI(
        title="Hermes Control Center API",
        version="0.1.0",
        description="Lightweight control API for the Hermes Control Center dashboard.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("HERMES_CONTROL_CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001").split(","),
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok", service="hermes-control-center-api")

    @app.get("/status", response_model=SystemStatus)
    def status() -> SystemStatus:
        settings = load_settings()
        session_count = 0
        active_session_count = 0
        latest_activity_at = None
        hermes_connected = settings.state_db.exists()
        if hermes_connected:
            with connect_state_db(settings) as conn:
                session_count = conn.execute("select count(*) from sessions").fetchone()[0]
                active_session_count = conn.execute("select count(*) from sessions where ended_at is null").fetchone()[0]
                latest_ts = conn.execute("select max(timestamp) from messages").fetchone()[0]
                latest_activity_at = iso_timestamp(latest_ts)
        return SystemStatus(
            hermes_connected=hermes_connected,
            live_updates="polling-preview",
            allowed_roots=list(settings.allowed_roots),
            state_db=str(settings.state_db) if hermes_connected else None,
            session_count=session_count,
            active_session_count=active_session_count,
            latest_activity_at=latest_activity_at,
        )

    @app.get("/sessions", response_model=list[SessionSummary])
    def sessions(limit: int = 12) -> list[SessionSummary]:
        settings = load_settings()
        limit = max(1, min(limit, 50))
        with connect_state_db(settings) as conn:
            rows = conn.execute(
                """
                select
                  s.id,
                  s.title,
                  s.source,
                  s.model,
                  s.started_at,
                  s.message_count,
                  s.tool_call_count,
                  max(m.timestamp) as last_activity_at,
                  (
                    select mm.content
                    from messages mm
                    where mm.session_id = s.id and mm.role in ('user', 'assistant')
                    order by mm.timestamp desc
                    limit 1
                  ) as preview
                from sessions s
                left join messages m on m.session_id = s.id
                group by s.id
                order by coalesce(last_activity_at, s.started_at) desc
                limit ?
                """,
                (limit,),
            ).fetchall()
        return [session_summary_from_row(row) for row in rows]

    @app.get("/sessions/{session_id}", response_model=SessionDetail)
    def session_detail(session_id: str, message_limit: int = 30) -> SessionDetail:
        settings = load_settings()
        message_limit = max(1, min(message_limit, 100))
        with connect_state_db(settings) as conn:
            row = conn.execute(
                """
                select
                  s.id,
                  s.title,
                  s.source,
                  s.model,
                  s.started_at,
                  s.message_count,
                  s.tool_call_count,
                  max(m.timestamp) as last_activity_at,
                  (
                    select mm.content
                    from messages mm
                    where mm.session_id = s.id and mm.role in ('user', 'assistant')
                    order by mm.timestamp desc
                    limit 1
                  ) as preview
                from sessions s
                left join messages m on m.session_id = s.id
                where s.id = ?
                group by s.id
                """,
                (session_id,),
            ).fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Session not found")
            message_rows = conn.execute(
                """
                select id, session_id, role, content, tool_name, timestamp
                from messages
                where session_id = ? and role in ('user', 'assistant', 'tool')
                order by timestamp desc
                limit ?
                """,
                (session_id, message_limit),
            ).fetchall()
        summary = session_summary_from_row(row)
        messages = [message_summary_from_row(message_row) for message_row in reversed(message_rows)]
        return SessionDetail(**summary.model_dump(), messages=messages)

    @app.get("/activity", response_model=list[MessageSummary])
    def activity(limit: int = 20) -> list[MessageSummary]:
        settings = load_settings()
        limit = max(1, min(limit, 50))
        with connect_state_db(settings) as conn:
            rows = conn.execute(
                """
                select id, session_id, role, content, tool_name, timestamp
                from messages
                where role in ('user', 'assistant', 'tool')
                order by timestamp desc
                limit ?
                """,
                (limit,),
            ).fetchall()
        return [message_summary_from_row(row, limit=500) for row in rows]

    @app.get("/approvals", response_model=list[ApprovalSummary])
    def approvals() -> list[ApprovalSummary]:
        return [
            ApprovalSummary(
                id="preview-no-live-approval-bridge-yet",
                status="placeholder",
                message="Hermes approval data is not exposed through a stable API yet. This dashboard will show live approval requests here once the approval bridge is implemented.",
            )
        ]

    return app


app = create_app()
