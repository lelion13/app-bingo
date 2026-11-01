# Exploration: Visor móvil de números

## Need

Operators run bingo on a main screen; players/helpers on phone/tablet need a **read-only** view of the last drawn number and the list of balls already out — without draw/reset controls.

## Current system

- Authoritative state: in-memory in `main.py`
- `GET /estado/` already returns `salidas`, `restantes`, `total`
- Home UI is control-heavy (3D + buttons); not ideal as a second display

## Options

| Approach | Pros | Cons |
|----------|------|------|
| A. New page + poll `/estado/` | Fits stack, no new infra | Slight delay (1–2s) |
| B. WebSocket/SSE push | Live instant | More code, overkill for bingo pace |
| C. Embed home in read-only mode | Reuse template | Still heavy 3D/assets |

**Choice: A** — `GET /visor` mobile-first page polling `/estado/`.

## URL

Recommend `/visor` (also `/visor/`). Clear, short to type/share on LAN.

## UX sketch

- Large last number (or empty state)
- Grid of drawn balls (newest emphasized / at top or full board 1–90 marked)
- Counter restantes optional
- No Iniciar / Sacar / Config
- Auto-refresh via poll ~1.5s

## Risks

- Multi-worker: same as game (shared memory not guaranteed) — out of scope
- Polling battery: 1.5s is fine for bingo
