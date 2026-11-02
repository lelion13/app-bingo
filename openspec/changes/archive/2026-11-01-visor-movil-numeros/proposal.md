# Proposal: Visor móvil de números

## Intent

Expose a phone/tablet URL that **only displays** the numbers that have been drawn (and the latest one prominently), synced to the live bingo state, with no game controls.

## Scope

### In Scope

- Route `GET /visor` (+ trailing slash)
- Mobile-first HTML page: last number large + list/grid of `salidas`
- Poll `GET /estado/` on an interval (~1.5s) to stay in sync
- Read-only: no iniciar/sacar/configuración actions
- Link from home (optional small “Visor”) so the URL is discoverable
- SDD delta specs for `ui` (+ note under `game` if needed)

### Out of Scope

- Auth / PIN to open the viewer
- WebSockets / SSE
- Changing draw logic or persistence
- Separate multi-game rooms

## Approach

1. Add FastAPI template route mirroring `/configuracion`.
2. New `templates/visor.html` + `static/js/visor.js` using existing `/estado/` and bolilla colors.
3. Poll and re-render; highlight latest ball.
4. Keep assets light (no Three.js).

## Affected Areas

- `main.py`
- `templates/visor.html` (new)
- `static/js/visor.js` (new)
- `templates/index.html` (link)
- `openspec/specs/ui` (and possibly `game`)

## Rollback Plan

Remove `/visor` route and viewer files; remove home link. Game behavior unchanged.

## Risks

- Polling lag of ~1–2s (acceptable for bingo calling pace)
- Same in-memory limits as the main game
