#!/usr/bin/env bash
set -euo pipefail

api_pid=""
web_pid=""

shutdown() {
  if [[ -n "$web_pid" ]] && kill -0 "$web_pid" 2>/dev/null; then
    kill "$web_pid" 2>/dev/null || true
  fi
  if [[ -n "$api_pid" ]] && kill -0 "$api_pid" 2>/dev/null; then
    kill "$api_pid" 2>/dev/null || true
  fi
  wait || true
}
trap shutdown TERM INT EXIT

cd /app

/opt/hermes-control-api/bin/uvicorn app.main:app \
  --app-dir /app/apps/api \
  --host 127.0.0.1 \
  --port 8787 &
api_pid=$!

NODE_ENV=production node apps/web/.output/server/index.mjs &
web_pid=$!

wait -n "$api_pid" "$web_pid"
exit $?
