# syntax=docker/dockerfile:1

FROM node:24-bookworm-slim AS web-build

WORKDIR /app

COPY package.json yarn.lock ./
COPY apps/web/package.json apps/web/package.json
COPY scripts scripts

RUN corepack enable \
  && yarn install --frozen-lockfile

COPY apps/web apps/web

ENV NUXT_PUBLIC_API_BASE=/api \
    NUXT_API_INTERNAL_BASE=http://127.0.0.1:8787

RUN yarn build:web

FROM node:24-bookworm-slim AS runtime

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3 python3-venv \
  && rm -rf /var/lib/apt/lists/*

COPY apps/api/requirements.txt apps/api/requirements.txt
RUN python3 -m venv /opt/hermes-control-api \
  && /opt/hermes-control-api/bin/pip install --no-cache-dir --upgrade pip \
  && /opt/hermes-control-api/bin/pip install --no-cache-dir -r apps/api/requirements.txt

COPY apps/api/app apps/api/app
COPY --from=web-build /app/apps/web/.output apps/web/.output
COPY deploy/start-kamal.sh /usr/local/bin/start-kamal

RUN chmod +x /usr/local/bin/start-kamal

ENV NODE_ENV=production \
    HOST=0.0.0.0 \
    PORT=3000 \
    NITRO_HOST=0.0.0.0 \
    NITRO_PORT=3000 \
    NUXT_PUBLIC_API_BASE=/api \
    NUXT_API_INTERNAL_BASE=http://127.0.0.1:8787 \
    HERMES_STATE_DB=/root/.hermes/state.db \
    HERMES_CONTROL_ALLOWED_ROOTS=/srv/syncthing/kb-private:/srv/syncthing/kb-shared \
    HERMES_CONTROL_CORS_ORIGINS=https://slugb0t.work

EXPOSE 3000

CMD ["start-kamal"]
