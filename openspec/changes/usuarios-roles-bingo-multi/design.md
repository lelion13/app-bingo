# Design: Usuarios, roles y bingo multi-tenant

## Technical Approach

Split the monolith into domain modules over SQLite. JWT protects panel APIs; public routes are health + `/visor/{username}` + `/estado/{username}`. One bingo row (pool JSON + salidas JSON) and one config row per user.

## Architecture Decisions

| Decision | Choice | Rejected | Rationale |
|----------|--------|----------|-----------|
| DB | SQLite file | Postgres | Low traffic; simple volume |
| Auth | JWT + bcrypt | Sessions-only / API keys | Matches workspace security rules |
| Tenancy | 1 bingo / user (username slug) | Shared game / codes | Confirmed product rule |
| Bootstrap | CLI one-shot | Env auto-admin | Explicit ops step |
| ABM | Soft deactivate | Hard delete | Keep bingo history |
| Config | SQLite per user | sessionStorage | Cross-device |

## Data Flow

```
Login ──► JWT ──► Panel (/, config, ABM)
                      │
                      ▼
                 SQLite (users, bingos, configs)
                      │
Visor /visor/{u} ──► GET /estado/{u} (public, read-only)
```

Draw/reset: JWT → resolve `user_id` → mutate that bingo only.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `main.py` | Modify | App factory; include routers; drop globals |
| `app/db.py` | Create | SQLite connect/init schema |
| `app/models` / repos | Create | users, bingos, configs |
| `app/auth/` | Create | bcrypt, JWT, deps, login router |
| `app/api/users.py` | Create | Admin ABM |
| `app/api/bingo.py` | Create | Auth mutations + public estado |
| `app/api/config.py` | Create | Auth get/put settings |
| `scripts/bootstrap_admin.py` | Create | First admin + bingo |
| `templates/login.html`, `usuarios.html` | Create | Auth/ABM UI |
| `templates/index.html`, `visor.html`, `configuracion.html` | Modify | Auth gate; scoped URLs |
| `static/js/*` | Modify | Token storage; scoped fetch; QR per user |
| `requirements.txt` | Modify | bcrypt, PyJWT, etc. |
| `docker-compose.prod.yml` | Modify | Volume + secrets |
| `docs/deploy-vps.md` | Modify | Bootstrap + volume |

## Interfaces / Contracts

```text
POST /auth/login {username, password} → {access_token, token_type, role, username}
GET  /estado/{username}               → {restantes, salidas, total}  # public
GET  /iniciar_bingo/  (JWT)           → reset own bingo
GET  /sacar_bolilla/  (JWT)           → draw own bingo
GET/PUT /api/config/  (JWT)           → {modal_seconds, modal_cm}
CRUD /api/users/      (JWT admin)     → user list/create/patch/deactivate
GET  /visor/{username}                → HTML public
```

Username: URL-safe slug = login username (unique, case-normalized policy in impl).

## Testing Strategy

| Layer | What | Approach |
|-------|------|----------|
| Unit | bcrypt verify, JWT claims, pool draw | pytest |
| Integration | login, isolation A/B, deactivate, config persist | TestClient + temp SQLite |
| Manual | QR URL, visor poll, bootstrap on compose volume | checklist |

## Migration / Rollout

No existing prod user data. Deploy new image + empty volume; run bootstrap once; create operadores. Bare `/visor` stops serving the old shared game.

## Open Questions

- [x] Resolved in discovery (SQLite, URL shape, bootstrap, ABM, config)
- [ ] Exact username normalization (lowercase?) — default lowercase in apply
