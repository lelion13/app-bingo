# Archive report: ui-modal-config-responsive

- **Archived**: 2026-11-01
- **Mode**: hybrid (filesystem main specs + Engram project context refresh)
- **Note**: Work was applied before formal propose→spec→design pipeline; this archive captures lineage and points at the resulting source-of-truth specs.

## Specs synced to main

| Domain | Path |
|--------|------|
| game | `openspec/specs/game/spec.md` |
| ui | `openspec/specs/ui/spec.md` |
| config | `openspec/specs/config/spec.md` |

## Key behaviors locked in

- Server-authoritative bingo 90; `/estado/` restore on home load
- Modal overlay (cm diameter + proportional number); duration default 3s
- sessionStorage-only config; `/configuracion` page
- Responsive 3-column layout; logo aligned with BINGO; Últimas taller, newest first (up to 30)
