# Proposal: Usuarios, roles y bingo multi-tenant

## Intent

Allow multiple operators, each with their own bingo and public visor, managed by an admin — replacing the single shared in-memory game.

## Scope

### In Scope

- Users with roles `admin` | `operador`; passwords bcrypt; JWT on control panel
- Exactly one bingo per user (created with the user); admin also has a bingo
- Admin-only ABM: create, edit role/password, deactivate (no hard delete)
- First admin via one-shot bootstrap command/script
- SQLite persistence (users, bingo state, per-user modal config)
- Public visor at `/visor/<usuario>`; QR/link per logged-in user
- Protected draw/reset/estado/config for the authenticated user's bingo

### Out of Scope

- PostgreSQL / multi-worker shared DB
- Hard delete of users
- Visor authentication
- Username rename / vanity URLs beyond login slug
- Multiple bingos per user

## Approach

Modular FastAPI: auth + users + bingo repositories on SQLite; JWT dependency on mutating/control routes; public scoped visor+estado by username; Docker volume for DB file; bootstrap CLI creates first admin + bingo.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `main.py` | Modified | Wire routers; remove globals |
| `backend/` (new) | New | schemas, services, repos, auth |
| `templates/` + `static/js/` | Modified | Login, ABM, scoped APIs/QR |
| `docker-compose.prod.yml` | Modified | Volume + JWT/DB env |
| Specs auth/game/ui/config/deploy | New/Delta | Behavior contracts |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Data loss without volume | Med | Document + mount SQLite path |
| Breaking existing `/visor` | High | 404 bare path; migrate QR to `/visor/<user>` |
| Weak JWT secret | Med | Require `JWT_SECRET` in prod |

## Rollback Plan

Revert deploy image; remove volume mount if unused. No prod user data yet → safe wipe of SQLite file.

## Dependencies

- `bcrypt`, JWT lib (e.g. `PyJWT` / `python-jose`), SQLite driver (stdlib `sqlite3` or SQLAlchemy)

## Success Criteria

- [ ] Admin bootstraps, creates operador; each has isolated bingo state
- [ ] Unauthenticated draw/reset/config rejected; visor public by username
- [ ] Deactivated user cannot login; config follows user across devices
- [ ] Prod compose persists SQLite across container restarts
