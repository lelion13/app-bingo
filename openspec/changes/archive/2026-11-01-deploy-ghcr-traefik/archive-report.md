# Archive report: deploy-ghcr-traefik

- **Archived**: 2026-11-01
- **Mode**: hybrid
- **Merged into main**: `openspec/specs/deploy/spec.md`
- **Also updated**: `openspec/specs/game/spec.md` (health + TemplateResponse requirement), `openspec/config.yaml`

## Prod verification notes

- `/health` 200 while HTML 500 → Jinja API mismatch (fixed)
- Image: `ghcr.io/lelion13/app-bingo`
- Host: `bingo.lionapp.cloud` via `traefik-wpez`
