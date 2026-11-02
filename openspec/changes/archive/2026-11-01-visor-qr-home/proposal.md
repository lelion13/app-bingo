# Proposal: QR y link amigable al visor en home

## Intent

Make the mobile/tablet visor reachable from the bingo home by scanning a QR code and via a short friendly link, both always targeting production `https://bingo.lionapp.cloud/visor`.

## Scope

### In Scope

- Show a ~120px QR in the left home column below the action buttons
- Show a friendly link labeled `bingo.lionapp.cloud/visor` (href = full HTTPS prod URL)
- Remove the existing **Visor** button from home
- Client-side QR generation (no new backend endpoint required)
- SDD delta specs under `ui` (update discoverability requirement)

### Out of Scope

- Dynamic QR based on current host / LAN IP
- Changing `/visor` behavior
- Auth / PIN for visor
- Configurable prod URL via UI (may use a single constant / env later if needed)

## Approach

1. Replace the Visor `<a>` with a small “compartir visor” block: QR canvas/img + anchor.
2. Use a lightweight client QR library (CDN) or equivalent to encode `https://bingo.lionapp.cloud/visor`.
3. Keep Configuración and other controls unchanged.

## Affected Areas

- `templates/index.html`
- Possibly `static/js/main.js` or a tiny `static/js/visor-qr.js`
- `openspec/specs/ui/spec.md` (via delta then archive)

## Rollback Plan

Restore Visor button; remove QR block and script.

## Risks

- Small QR (~120px) may be hard to scan from far away
- Prod URL hardcoded while browsing localhost (by design)
