# Architecture

Hermes Control Center is designed as a lightweight control plane, not an AI workload host.

```text
Nuxt SPA/PWA frontend
        ↓ authenticated HTTP + SSE/WebSocket
Hermes Control API
        ↓ controlled adapters
Hermes Agent state, logs, approvals, KB folders, calendar tools
```

## Frontend

- Nuxt with `ssr: false` for a static/SPA deployment target.
- Mobile-first responsive layout.
- Bottom navigation on phones, sidebar on desktop.
- No secrets or privileged filesystem/calendar/tool logic in browser code.

## Backend

- FastAPI scaffold for the control plane.
- Owns authentication, authorization, file-root allowlists, approval checks, and audit logging.
- Intended to integrate with Hermes APIs/state rather than directly bypassing Hermes safety flows.

## Real-time updates

Use SSE or WebSockets for:

- gateway/system health
- active sessions
- tool call lifecycle events
- approval requests
- terminal output tails
- KB file/indexing status
- cron job status

Avoid deploying a heavy metrics stack on small servers. Persist important events, cap hot in-memory buffers, and paginate old logs.
