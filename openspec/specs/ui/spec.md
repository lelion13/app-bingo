# Domain: UI (Home / Bolillero)

## Purpose

Describe the home bingo experience: responsive layout, 3D ball, draw feedback via circular number modal, and the “Últimas” strip.

## Requirements

### Requirement: Responsive home layout

The home page MUST adapt to viewport size. On wide viewports (~900px+), the layout MUST use three columns: controls+logo | center game | últimas. Typography, logo, ball canvas, and chrome SHOULD scale with `clamp` / viewport units so the shell fits within the visible area when possible.

#### Scenario: Desktop alignment

- GIVEN a viewport at least ~900px wide
- WHEN the home page is shown
- THEN the club logo (left) MUST sit at approximately the same vertical band as the “BINGO” title (center)
- AND the “Últimas” column MUST stretch tall enough to show many balls with scrolling only when needed

#### Scenario: Narrow viewport

- GIVEN a narrow mobile viewport
- WHEN the home page is shown
- THEN columns MUST stack without horizontal overflow
- AND the 3D canvas MUST resize with its container

### Requirement: Adaptive 3D canvas

The Three.js renderer MUST resize when the canvas container size changes (window resize / ResizeObserver) so the ball stays sharp and fills the container.

#### Scenario: Resize window

- GIVEN the home page is open
- WHEN the browser window is resized
- THEN the WebGL canvas size MUST update to match the container

### Requirement: Number reveal modal on the ball

When a ball is successfully drawn, the system MUST show a circular modal superimposed on the ball containing the drawn number. The modal MUST auto-close after the configured session duration. There MUST NOT be a persistent large number fixed above the ball outside this modal.

#### Scenario: Draw shows then hides modal

- GIVEN the user completes a draw animation and the server returns a bolilla
- WHEN the result is applied
- THEN a circular overlay centered on the ball MUST display that number
- AND after the configured seconds the overlay MUST close by itself
- AND the result chip below the ball MAY continue showing the last number

### Requirement: Últimas ordering and capacity

The “Últimas” panel MUST list drawn balls with the most recent at the top. The client SHOULD retain up to 30 recent visuals in that panel. On restore from `/estado/`, order MUST still place newest at the top.

#### Scenario: Newest on top

- GIVEN balls 10 then 20 were drawn in that order
- WHEN both appear in “Últimas”
- THEN 20 MUST appear above 10

### Requirement: Spanish primary chrome

Primary user-visible labels and toasts on the home flow SHOULD remain in Spanish (Iniciar Bingo, Sacar Bolilla, Ver Bolillas, Configuración, Últimas, etc.).
