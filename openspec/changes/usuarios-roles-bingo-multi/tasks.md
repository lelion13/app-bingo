# Tasks: Usuarios, roles y bingo multi-tenant

## Phase 1: Foundation

- [x] 1.1 Add deps (`bcrypt`, `PyJWT`) to `requirements.txt`
- [x] 1.2 Create `app/db.py` + schema (users, bingos, configs) on SQLite path from env
- [x] 1.3 Implement user/bingo/config repositories (create user ⇒ create bingo + default config)
- [x] 1.4 Implement bcrypt + JWT helpers and FastAPI deps (`get_current_user`, `require_admin`)
- [x] 1.5 Add `scripts/bootstrap_admin.py` (fail if admin exists; create admin + bingo)

## Phase 2: API

- [x] 2.1 `POST /auth/login` + generic 401; reject deactivated
- [x] 2.2 Admin `/api/users` create / list / patch role-password / deactivate
- [x] 2.3 JWT `iniciar_bingo` / `sacar_bolilla` / own estado against caller bingo only
- [x] 2.4 Public `GET /estado/{username}` (404 if missing)
- [x] 2.5 JWT `GET/PUT /api/config/` for modal seconds/cm
- [x] 2.6 Wire routers in `main.py`; remove global bolilla lists

## Phase 3: UI

- [x] 3.1 Login page + client token storage; gate `/` and `/configuracion`
- [x] 3.2 Admin usuarios ABM page (create/edit/deactivate); hide from operador
- [x] 3.3 Update `main.js` draws/reset/estado to send JWT and use own APIs
- [x] 3.4 Config page load/save via `/api/config/`; retire sessionStorage as source of truth
- [x] 3.5 Visor route `/visor/{username}` + poll `/estado/{username}`; bare `/visor` → 404
- [x] 3.6 QR + friendly link → `https://bingo.lionapp.cloud/visor/{username}`

## Phase 4: Deploy & docs

- [x] 4.1 Compose volume for SQLite + `JWT_SECRET` / `DATABASE_PATH` env
- [x] 4.2 Update `docs/deploy-vps.md` (volume, secret, bootstrap)
- [x] 4.3 Update `openspec/config.yaml` context for auth/SQLite/multi-bingo

## Phase 5: Verification

- [x] 5.1 Test: login success/fail; deactivated blocked; operador 403 on ABM
- [x] 5.2 Test: bingo isolation between two users; restart keeps SQLite state
- [x] 5.3 Test: config persists per user; visor public without JWT
- [x] 5.4 Manual: bootstrap → create operador → QR opens correct visor
