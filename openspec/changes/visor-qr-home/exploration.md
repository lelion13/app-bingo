# Exploration: QR + link al visor en home

## Need

Operators need attendees/helpers on another phone/tablet to open `/visor` without typing a long URL — scan a QR on the main bingo console, or tap a short friendly link.

## Decisions (clarified)

| Topic | Choice |
|-------|--------|
| Target URL | Always production: `https://bingo.lionapp.cloud/visor` |
| Placement | Left column, below control buttons |
| Existing Visor button | Remove; QR + friendly link only |
| Friendly link label | `bingo.lionapp.cloud/visor` (no `https://` in visible text) |
| QR display size | Small (~120px) |

## Approach options

| Option | Notes |
|--------|-------|
| A. Client-side QR (CDN lib / canvas) | No backend; works offline once page loaded |
| B. Server-rendered QR image | Extra dependency/route |

**Choice: A** — generate QR in the browser pointing at the fixed prod URL.

## Risks

- Local/dev home still shows prod QR (intentional per product decision)
- Small QR harder at long distance (accepted: option A size)
