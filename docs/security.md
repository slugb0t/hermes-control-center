# Security model

The dashboard should be treated as privileged infrastructure because it can eventually view sessions, edit files, approve commands, and modify calendar data.

## Principles

- Private-network first: Tailscale or localhost by default.
- No secrets in frontend JavaScript.
- Backend validates every privileged action.
- File access is constrained to explicit allowlisted roots.
- Dangerous actions remain approval-gated.
- Audit logs record writes, approvals, config changes, and destructive actions.

## Recommended deployment defaults

- Bind API to localhost/private interface.
- Serve behind HTTPS if exposed beyond localhost.
- Use HttpOnly, Secure, SameSite cookies for auth.
- Add CSRF protection for state-changing requests.
- Disable public signup.
- Require explicit confirmation for file deletes, calendar deletes, and tool approvals.

## Mobile/PWA notes

The iPhone home-screen app is still a web client. It must use the same backend protections as desktop:

- no direct shell access
- no raw Google/Hermes credentials
- no unrestricted filesystem browsing
- no command execution bypass
