# Domain: Deploy (GHCR + Traefik VPS)

## Purpose

Define how app-bingo is built, published, and served at `https://bingo.lionapp.cloud` on the Hostinger VPS behind `traefik-wpez`.

## Requirements

### Requirement: Container image on GHCR

CI MUST publish the app image to `ghcr.io/lelion13/app-bingo` from the GitHub repository `lelion13/app-bingo` (workflow `.github/workflows/ghcr.yml`). Tags SHOULD include `latest` on `main` and a short SHA.

#### Scenario: Push to main

- GIVEN a push to `main` on `lelion13/app-bingo`
- WHEN the GHCR workflow completes successfully
- THEN an image `ghcr.io/lelion13/app-bingo` MUST be available with a `latest` and/or SHA tag

### Requirement: Production compose with Traefik

Production MUST run via `docker-compose.prod.yml` (project name `app-bingo`) with Traefik labels for `Host(\`bingo.lionapp.cloud\`)`, entrypoint `websecure`, TLS, and cert resolver `letsencrypt`, load-balancing port 8000. Typical VPS path: `/docker/app-bingo`.

#### Scenario: HTTPS host routing

- GIVEN Traefik `traefik-wpez` is running and DNS for `bingo.lionapp.cloud` points at the VPS
- WHEN the compose stack is up
- THEN `https://bingo.lionapp.cloud/health` MUST return 200
- AND HTML routes under that host MUST be served by the bingo container

### Requirement: Production environment hardening

When `APP_ENV` is `production` or `prod`, FastAPI interactive docs (`/docs`, `/redoc`, `/openapi.json`) MUST be disabled. Compose SHOULD set `APP_ENV=production` and CORS toward `https://bingo.lionapp.cloud`. The container SHOULD run as a non-root user with `no-new-privileges` and dropped capabilities as defined in compose/Dockerfile.

#### Scenario: Docs off in prod

- GIVEN production environment
- WHEN a client requests `/docs`
- THEN the response MUST NOT expose Swagger UI (typically 404)

### Requirement: Healthcheck interval

Compose healthchecks MUST probe `/health` with a long interval (about 60s) to avoid saturating `dockerd`. The Dockerfile SHOULD NOT define an aggressive duplicate HEALTHCHECK.

#### Scenario: Container marked healthy

- GIVEN the bingo service has started successfully
- WHEN Docker evaluates the healthcheck
- THEN the service MUST become `healthy` using `/health`

### Requirement: Deploy documentation

Operator steps for GHCR login (if private), pull, and up MUST be documented under `docs/deploy-vps.md`.

#### Scenario: Operator can redeploy

- GIVEN a new image tag was published
- WHEN the operator follows `docs/deploy-vps.md`
- THEN they can pull and recreate the stack on the VPS without guessing Traefik labels
