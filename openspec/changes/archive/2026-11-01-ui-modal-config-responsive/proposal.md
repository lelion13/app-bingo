# Proposal (archived): UI modal, session config, responsive layout

**Status**: Implemented in chat (retroactive SDD documentation)  
**Date**: 2026-11-01  
**Project**: app-bingo

## Intent

Modernize draw feedback and operator controls without a database:

1. Show drawn number in a circular modal over the ball; auto-close.
2. Add `/configuracion` for modal duration (seconds) and size (cm), `sessionStorage` only.
3. Restore game UI from `/estado/` when returning from configuration (no accidental reset).
4. Make the home layout responsive; align logo with BINGO; taller “Últimas” with newest on top.

## Affected areas

- `main.py` — `/configuracion` route
- `templates/index.html`, `templates/configuracion.html`
- `static/js/main.js`, `config-store.js`, `configuracion.js`

## Rollback

Revert the listed files / restore from git prior to this workstream.

## Outcome

Merged into main specs under `openspec/specs/{game,ui,config}/spec.md` and `openspec/config.yaml` context updated.
