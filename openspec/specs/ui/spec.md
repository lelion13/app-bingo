# Domain: UI (Home / Bolillero / Visor)

## Purpose

Describe the home bingo experience (responsive layout, 3D ball, circular number modal, Últimas) and the read-only mobile/tablet viewer at `/visor`.

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

Primary user-visible labels and toasts on the home flow SHOULD remain in Spanish (Iniciar Bingo, Sacar Bolilla, Ver Bolillas, Configuración, Últimas, Visor móvil, etc.).

### Requirement: Home discovers viewer

The home page MUST discover the viewer via a production QR and friendly link in the left control column (below the primary action buttons). A separate **Visor** button control MUST NOT be shown.

#### Scenario: No Visor button

- GIVEN the home page is loaded
- WHEN the operator inspects the left controls
- THEN there MUST NOT be a standalone “Visor” button
- AND the QR + friendly link block MUST be present below the remaining actions

### Requirement: Production visor QR on home

The home page MUST display a QR code in the left control column, below the primary action buttons. The QR MUST encode exactly `https://bingo.lionapp.cloud/visor`. The rendered QR SHOULD be approximately 120px wide (small).

#### Scenario: Scan opens production visor

- GIVEN the home page is loaded (any host)
- WHEN a device scans the displayed QR
- THEN it MUST open `https://bingo.lionapp.cloud/visor`
- AND MUST NOT encode the current page origin instead of production

### Requirement: Friendly visor link on home

Adjacent to the QR (same left-column block), the home page MUST show a clickable link whose visible text is `bingo.lionapp.cloud/visor` and whose `href` is `https://bingo.lionapp.cloud/visor`.

#### Scenario: Tap friendly link

- GIVEN the home page is loaded
- WHEN the user activates the friendly link
- THEN the browser MUST navigate to `https://bingo.lionapp.cloud/visor`

### Requirement: Mobile viewer page

The system MUST serve a read-only viewer at `GET /visor` and `GET /visor/` optimized for phone and tablet viewports. The page MUST NOT expose controls to start the game, draw balls, or open configuration.

#### Scenario: Open viewer

- GIVEN the server is running
- WHEN a client opens `/visor`
- THEN a mobile-first view of drawn numbers MUST be shown
- AND no Iniciar / Sacar / Configuración actions MUST be available on that page

### Requirement: Live sync via estado

The viewer MUST refresh its display from `GET /estado/` on a short interval (approximately 1–2 seconds) so new draws appear without reloading the page.

#### Scenario: New ball appears

- GIVEN the viewer is open and polling
- WHEN the main console draws a new bolilla
- THEN within about two seconds the viewer MUST show that number as the latest
- AND include it among the listed salidas

### Requirement: Latest number prominence

The viewer MUST show the most recently drawn number in a large, prominent display when at least one ball has been drawn. If none have been drawn, it MUST show a clear empty state.

#### Scenario: Empty game

- GIVEN `salidas` is empty
- WHEN the viewer renders
- THEN it MUST indicate that no balls have been drawn yet
- AND MUST NOT invent a number

### Requirement: History of drawn balls

The viewer MUST list all currently drawn balls from server state, with the latest visually emphasized. Ordering SHOULD put newest first.

#### Scenario: Multiple draws

- GIVEN several balls in `salidas`
- WHEN the viewer updates
- THEN every number in `salidas` MUST be visible in the history section
