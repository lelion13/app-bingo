# Proposal (archived): Deploy GHCR + Traefik

**Status**: Implemented  
**Date**: 2026-11-01

## Intent

Publish bingo to the user’s GitHub (`lelion13/app-bingo`), GHCR, and VPS Traefik at `bingo.lionapp.cloud`.

## Delivered

- `.github/workflows/ghcr.yml` → `ghcr.io/lelion13/app-bingo`
- `docker-compose.prod.yml` Traefik labels (websecure / letsencrypt)
- Dockerfile non-root; `/health`; docs off when `APP_ENV=production`
- `docs/deploy-vps.md`, `.env.prod.example`
- Fix Starlette `TemplateResponse(request, name)` after prod 500 (`unhashable type: 'dict'`)

## Out of scope

- Changing DNS (already resolved)
- Auth on public bingo
