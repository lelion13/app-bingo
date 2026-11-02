# Delta for Deploy

## ADDED Requirements

### Requirement: SQLite volume

Production compose MUST mount a persistent volume (or bind mount) for the SQLite database file so user/bingo/config data survive container recreation.

#### Scenario: Restart keeps users

- GIVEN bootstrapped admin exists in the mounted DB
- WHEN the bingo container is recreated with the same volume
- THEN admin login MUST still succeed

### Requirement: JWT secret in environment

Production MUST supply `JWT_SECRET` (or equivalent) via env/secrets. The app MUST NOT ship a production default secret in the image.

#### Scenario: Missing secret in prod

- GIVEN `APP_ENV=production` and JWT secret unset/empty
- WHEN the app starts
- THEN startup MUST fail fast OR refuse to issue tokens (documented secure behavior)

## MODIFIED Requirements

### Requirement: (compose env surface)

Prod env MUST document DB path, JWT secret, and bootstrap procedure in `docs/deploy-vps.md` (or equivalent).

(Previously: only `APP_ENV` / `CORS_ORIGINS` / image tag.)
