# Delta for UI

## ADDED Requirements

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

The viewer MUST list all currently drawn balls from server state (or a complete visual board of drawn ones), with the latest visually emphasized. Ordering SHOULD put newest first or otherwise make the latest obvious.

#### Scenario: Multiple draws

- GIVEN several balls in `salidas`
- WHEN the viewer updates
- THEN every number in `salidas` MUST be visible in the history/board section
