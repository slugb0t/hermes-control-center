from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_reports_ok():
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "hermes-control-center-api"}


def test_status_endpoint_exposes_allowed_roots_and_missing_db(monkeypatch, tmp_path):
    missing_db = tmp_path / "missing.db"
    monkeypatch.setenv("HERMES_CONTROL_ALLOWED_ROOTS", "/tmp/private:/tmp/shared")
    monkeypatch.setenv("HERMES_STATE_DB", str(missing_db))
    client = TestClient(create_app())

    response = client.get("/status")

    assert response.status_code == 200
    assert response.json() == {
        "hermes_connected": False,
        "live_updates": "polling-preview",
        "allowed_roots": ["/tmp/private", "/tmp/shared"],
        "state_db": None,
        "session_count": 0,
        "active_session_count": 0,
        "latest_activity_at": None,
    }


def test_sessions_endpoint_returns_recent_sessions_with_status(monkeypatch, tmp_path):
    db_path = tmp_path / "state.db"
    seed_state_db(db_path)
    monkeypatch.setenv("HERMES_STATE_DB", str(db_path))
    client = TestClient(create_app())

    response = client.get("/sessions")

    assert response.status_code == 200
    sessions = response.json()
    assert sessions[0]["id"] == "session-1"
    assert sessions[0]["title"] == "Dashboard preview"
    assert sessions[0]["preview"] == "Latest assistant response"
    assert sessions[0]["status"] == "running"
    assert sessions[1]["status"] == "idle"


def test_sessions_endpoint_filters_and_sorts_sessions(monkeypatch, tmp_path):
    db_path = tmp_path / "state.db"
    seed_state_db(db_path)
    monkeypatch.setenv("HERMES_STATE_DB", str(db_path))
    client = TestClient(create_app())

    oldest_response = client.get("/sessions?sort=oldest&tools=no-tools")
    assert oldest_response.status_code == 200
    assert [session["id"] for session in oldest_response.json()] == ["session-2"]

    query_response = client.get("/sessions?query=assistant&sort=most-messages")
    assert query_response.status_code == 200
    assert query_response.json()[0]["id"] == "session-1"


def test_session_filters_endpoint_returns_available_sources_and_models(monkeypatch, tmp_path):
    db_path = tmp_path / "state.db"
    seed_state_db(db_path)
    monkeypatch.setenv("HERMES_STATE_DB", str(db_path))
    client = TestClient(create_app())

    response = client.get("/sessions/filters")

    assert response.status_code == 200
    assert response.json() == {"sources": ["discord", "local"], "models": ["gpt-5.5"]}


def test_session_detail_redacts_secret_tokens(monkeypatch, tmp_path):
    db_path = tmp_path / "state.db"
    seed_state_db(db_path)
    monkeypatch.setenv("HERMES_STATE_DB", str(db_path))
    client = TestClient(create_app())

    response = client.get("/sessions/session-1")

    assert response.status_code == 200
    payload = response.json()
    assert payload["messages"][0]["content"] == "Please use [REDACTED]"
    assert payload["messages"][0]["content_truncated"] is False


def test_session_detail_exposes_tool_call_summary_for_empty_assistant_messages(monkeypatch, tmp_path):
    db_path = tmp_path / "state.db"
    seed_state_db(db_path)
    monkeypatch.setenv("HERMES_STATE_DB", str(db_path))
    client = TestClient(create_app())

    response = client.get("/sessions/session-1")

    assert response.status_code == 200
    payload = response.json()
    tool_call_message = payload["messages"][2]
    assert tool_call_message["role"] == "assistant"
    assert tool_call_message["content"].startswith("Tool call requested: terminal")
    assert "yarn test" in tool_call_message["content"]


def seed_state_db(path: Path) -> None:
    import sqlite3

    conn = sqlite3.connect(path)
    conn.executescript(
        """
        create table sessions (
            id text primary key,
            source text not null,
            user_id text,
            model text,
            model_config text,
            system_prompt text,
            parent_session_id text,
            started_at real not null,
            ended_at real,
            end_reason text,
            message_count integer default 0,
            tool_call_count integer default 0,
            input_tokens integer default 0,
            output_tokens integer default 0,
            cache_read_tokens integer default 0,
            cache_write_tokens integer default 0,
            reasoning_tokens integer default 0,
            billing_provider text,
            billing_base_url text,
            billing_mode text,
            estimated_cost_usd real,
            actual_cost_usd real,
            cost_status text,
            cost_source text,
            pricing_version text,
            title text,
            api_call_count integer default 0,
            handoff_state text,
            handoff_platform text,
            handoff_error text
        );
        create table messages (
            id integer primary key autoincrement,
            session_id text not null,
            role text not null,
            content text,
            tool_call_id text,
            tool_calls text,
            tool_name text,
            timestamp real not null,
            token_count integer,
            finish_reason text,
            reasoning text,
            reasoning_content text,
            reasoning_details text,
            codex_reasoning_items text,
            codex_message_items text,
            platform_message_id text,
            observed integer default 0
        );
        """
    )
    conn.execute(
        "insert into sessions (id, source, model, started_at, message_count, tool_call_count, title) values (?, ?, ?, ?, ?, ?, ?)",
        ("session-1", "discord", "gpt-5.5", 100.0, 3, 1, "Dashboard preview"),
    )
    conn.execute(
        "insert into sessions (id, source, model, started_at, ended_at, message_count, tool_call_count, title) values (?, ?, ?, ?, ?, ?, ?, ?)",
        ("session-2", "local", "gpt-5.5", 50.0, 60.0, 1, 0, "Older local session"),
    )
    conn.execute(
        "insert into messages (session_id, role, content, timestamp) values (?, ?, ?, ?)",
        ("session-1", "user", "Please use ghp_1234567890abcdefTOKEN", 101.0),
    )
    conn.execute(
        "insert into messages (session_id, role, content, timestamp) values (?, ?, ?, ?)",
        ("session-1", "assistant", "Latest assistant response", 102.0),
    )
    conn.execute(
        "insert into messages (session_id, role, content, tool_calls, timestamp) values (?, ?, ?, ?, ?)",
        (
            "session-1",
            "assistant",
            "",
            '[{"function":{"name":"terminal","arguments":"{\\"command\\":\\"yarn test\\"}"}}]',
            103.0,
        ),
    )
    conn.commit()
    conn.close()
