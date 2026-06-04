# Roadmap

This roadmap is the durable source of truth for Hermes Control Center feature tracking. Each PR phase should update this file before the PR is considered complete.

## Product goal

Build a private, mobile-friendly Hermes Control Center that acts as a web gateway/control plane for Hermes Agent — not only a read-only dashboard.

Core idea:

```text
/sessions/[id] = conversation + control plane
```

The app should let the user inspect Hermes state, continue conversations, approve/deny actions inline, monitor active work, and eventually manage selected knowledge/config workflows without exposing secrets to browser code.

## Tracking system

Use three lightweight artifacts:

1. `docs/roadmap.md` — canonical feature backlog, phase gates, and completion status.
2. GitHub PRs — one focused milestone per PR phase.
3. GitHub issues or project board — optional backlog mirror for granular tickets.

Rule: if a feature request comes up during debugging or design review, add it to the backlog here instead of relying on memory.

## Status legend

```text
[ ] Not started
[~] In progress
[x] Done / merged
[>] Deferred intentionally
[?] Needs decision
```

## Phase 1 — Session UX foundation

**Goal:** Make session pages feel like a usable chat/workspace before wiring full write actions.

### Features

- [x] Improved session detail layout
- [x] Message timeline with role-aware styling
- [x] Markdown rendering for assistant/user content
- [x] Code block rendering with copy action
- [x] Collapsible tool call blocks
- [x] Tool stdout/stderr display with truncation/expand affordance
- [x] Jump-to-latest behavior
- [x] Role/type filters inside a session
- [x] Mobile sticky composer shell
- [x] Current session status indicator: idle/running/waiting/failed
- [x] Empty/error/loading states

### Acceptance gate

Phase 1 is complete when:

- A user can open a session on mobile and desktop and understand the conversation flow.
- Tool calls are readable without overwhelming the page.
- The composer shell exists, even if sending is not wired yet.
- The next PR can focus on API/gateway write behavior instead of UI basics.

### Verification

- [x] API tests pass.
- [x] Production web build passes on Node 24.
- [>] Authenticated browser walkthrough is pending deploy/local auth setup.

## Phase 2 — Web gateway message sending

**Goal:** Let Control Center send messages into Hermes through the Hermes API server/gateway adapter.

### Features

- [ ] Decide Hermes API server/gateway adapter contract
- [ ] Add backend endpoint: `POST /sessions/{id}/messages`
- [ ] Add backend endpoint or event route: `GET /sessions/{id}/events`
- [ ] Add web composer send behavior
- [ ] Show optimistic pending user message
- [ ] Poll or stream session updates after sending
- [ ] Handle busy session state
- [ ] Add queue/steer/interrupt affordance design, even if partial
- [ ] Prevent browser access to secrets/client env
- [ ] Add tests for API request validation

### Acceptance gate

Phase 2 is complete when:

- A user can send a message from `/sessions/[id]` and see Hermes continue that session.
- The implementation uses the Hermes API server/gateway adapter path as the intended architecture.
- Busy/error states are visible and recoverable.

## Phase 3 — Inline approvals

**Goal:** Make approvals timeline-native inside sessions, with `/approvals` as a global inbox only.

### Features

- [ ] Detect pending approval requests for a session
- [ ] Render approval cards inline in the session timeline
- [ ] Add approve action from session page
- [ ] Add deny action from session page
- [ ] Preserve approved/denied state in the visible timeline
- [ ] Add global `/approvals` overview for all sessions
- [ ] Link global approval cards back to exact session/message
- [ ] Add audit event for approval/denial
- [ ] Confirm risky/destructive actions remain safety-gated

### Acceptance gate

Phase 3 is complete when:

- The primary approval flow happens inside the conversation.
- The global approvals page is only an overview/triage queue.
- Approval actions update the original session view without losing context.

## Phase 4 — Activity and runs

**Goal:** Provide a central operational view of active Hermes work.

### Features

- [ ] Active sessions list
- [ ] Running tools/processes
- [ ] Waiting approvals
- [ ] Recent completions
- [ ] Failed runs/errors
- [ ] Cron job status list
- [ ] Gateway/log status summaries
- [ ] Lightweight event/audit timeline

### Acceptance gate

Phase 4 is complete when:

- The home/activity view answers: what is Hermes doing, what needs me, and what recently failed/completed?

## Phase 5 — Odysseus-style app shell and PWA polish

**Goal:** Turn the tool into a polished self-hosted control workspace.

### Features

- [ ] Better sidebar on desktop
- [ ] Better bottom navigation on mobile
- [ ] Command launcher
- [ ] Global search
- [ ] Better route icons and visual hierarchy
- [ ] PWA install polish
- [ ] Responsive touch targets
- [ ] Deep links to sessions/approvals/activity

### Acceptance gate

Phase 5 is complete when:

- The app feels coherent as a daily-use control center, not a collection of pages.

## Phase 6 — Knowledge/config workflows

**Goal:** Add controlled read/write workflows after the core gateway experience is stable.

### Features

- [ ] KB root browsing in read-only mode
- [ ] Markdown editing for explicitly allowlisted KB folders
- [ ] Skills viewer
- [ ] Memory viewer
- [ ] Config viewer
- [ ] Safe config edit affordances where appropriate
- [ ] Calendar read/create/edit with explicit delete confirmation

### Acceptance gate

Phase 6 is complete when:

- Knowledge/config tools are useful but do not bypass existing Hermes safety expectations.

## Deployment/security backlog

- [x] VPS deploy flow with `appuser`
- [x] Runner SSH key deployment path
- [x] Repo env secrets documented
- [ ] Minimal auth/session management
- [ ] Audit log
- [ ] Deployment docs
- [ ] Health/status endpoints
- [x] Node 24 runtime for builds/deploys
- [ ] No client secrets in browser code
- [ ] Hidden deploy IPs via GitHub env secrets

## Open design decisions

- [?] Exact Hermes API server/gateway adapter contract for web session continuation
- [?] Whether session updates start with polling or SSE in Phase 2
- [?] How much queue/steer/interrupt lands in Phase 2 vs later
- [?] Whether GitHub issues should mirror every roadmap item or only PR phases

## Backlog parking lot

Add future ideas here during debugging/revision so they are not lost:

- [ ] Session export/share affordances
- [ ] File/image attachments from web composer
- [ ] Terminal log tail view
- [ ] Per-session run summary
- [ ] User-facing status banners for gateway/API downtime
