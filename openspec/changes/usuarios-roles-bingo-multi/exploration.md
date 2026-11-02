## Exploration: usuarios-roles-bingo-multi

### Current State

- Single in-memory bingo in `main.py` (`bolillas_disponibles` / `bolillas_salidas`).
- No DB, no auth; `/`, `/configuracion`, `/visor`, `/iniciar_bingo/`, `/sacar_bolilla/`, `/estado/` are open.
- Config in browser `sessionStorage` via `static/js/config-store.js`.
- Home QR/link hardcoded to `https://bingo.lionapp.cloud/visor`.
- Prod: one Traefik service, no volume for data.

### Affected Areas

- `main.py` — split monolith; JWT gates; per-user game APIs
- `templates/` + `static/js/` — login, ABM, scoped QR/visor/config
- New: SQLite models/repos/services, bootstrap CLI
- `docker-compose.prod.yml` — SQLite volume + secrets (`JWT_SECRET`)
- Specs: new `auth`; deltas `game`, `ui`, `config`, `deploy`

### Approaches

1. **SQLite + JWT + 1 bingo/user** — Persist users/bingo/config; panel JWT; public `/visor/<usuario>`.
   - Pros: fits low traffic; survives restart; matches stack rules (JWT/bcrypt)
   - Cons: modularize `main.py`; mount volume
   - Effort: High

2. **Keep memory + API keys** — Rejected: no ABM persistence, lost on restart.

### Recommendation

Approach 1. Username is login + visor slug. Admin bootstrapped by one-shot CLI. Soft-deactivate users.

### Risks

- Breaking bare `/visor` and shared `/estado/` (must scope by user)
- SQLite file lost without volume
- Username rename breaks QR URLs (disallow rename or redirect later)

### Ready for Proposal

Yes — decisions locked (1:1 bingo, SQLite, `/visor/<user>`, bootstrap CLI, admin has bingo, panel JWT / visor public, ABM deactivate, config in DB per user).
