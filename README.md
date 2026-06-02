# Hermes Control Center

Hermes Control Center is a mobile-friendly web dashboard for operating a personal Hermes Agent install. The goal is a lightweight Mission Control interface that can run on a small VPS now, while staying portable to a larger home server later.

## Goals

- Responsive Nuxt UI that works well on desktop and iPhone Safari.
- PWA-style home-screen install experience.
- Lightweight backend API for status, activity, approvals, KB files, and calendar integrations.
- Real-time updates through SSE/WebSocket without a heavy observability stack.
- Secure-by-default design: private network first, backend-owned secrets, file allowlists, approval-gated dangerous actions.

## Repository layout

```text
apps/
  web/   Nuxt SPA/PWA frontend
  api/   FastAPI control API scaffold
docs/    Architecture, security, and roadmap notes
```

## Development

### Web

```bash
npm install
npm run dev:web
```

The Nuxt dev server defaults to `http://localhost:3000`.

### API

```bash
cd apps/api
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8787
```

### Build / test

```bash
npm run build:web
cd apps/api && python -m pytest -q
```

## MVP scope

- Dashboard/status page
- Live activity feed scaffold
- Sessions, approvals, KB, calendar, and settings screens
- Mobile bottom navigation + desktop sidebar
- PWA manifest and safe-area aware layout
- API health/status endpoints

Real Hermes integration will be added behind the API after the UI and security boundaries are stable.
