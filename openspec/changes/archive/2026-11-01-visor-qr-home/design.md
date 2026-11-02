# Design: visor-qr-home

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| URL | Hardcoded `https://bingo.lionapp.cloud/visor` | Product: always prod |
| Placement | Left column under buttons | Operator glance + scan |
| Visor button | Removed | Replaced by QR + link |
| Link label | `bingo.lionapp.cloud/visor` | Short readable |
| QR size | ~120px | Fits column |
| Generation | Client-side (e.g. CDN QR lib → canvas) | No backend |

## Constant

```js
const VISOR_PROD_URL = "https://bingo.lionapp.cloud/visor";
```

## UI sketch (left column)

```
[Logo]
[Iniciar Bingo]
[Ver Bolillas]
[Sacar Bolilla]
[Configuración]
[ QR 120px ]
bingo.lionapp.cloud/visor   ← <a href=VISOR_PROD_URL>
```

## Files

- `templates/index.html` — markup + script include
- `static/js/visor-qr.js` (or inline init in main) — draw QR
