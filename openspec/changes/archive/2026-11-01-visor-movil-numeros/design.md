# Design: Visor móvil de números

## Architecture

```
[Main console /] --draw--> main.py memory
                              ^
[Visor /visor] --poll GET /estado/ every 1.5s--+
```

No new backend state. Viewer is a thin Jinja page + JS.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Transport | HTTP poll 1.5s | Matches stack; bingo pace does not need WS |
| Path | `/visor` | Short to share on LAN |
| Rendering | Last number hero + grid of salidas (newest first) | Glanceable on phone |
| Colors | Same decade colors as home `getColorBolilla` | Visual consistency |
| 3D | None | Battery/perf on mobile |

## Sequence

1. User opens `/visor`
2. JS fetches `/estado/`, paints UI
3. `setInterval` 1500ms repeats fetch; if `salidas` length/last changed, re-render
4. Main console continues using existing draw APIs

## Files

- `main.py` — route
- `templates/visor.html` — layout
- `static/js/visor.js` — poll + render
- `templates/index.html` — link “Visor”
