# Domain: Configuration (Session)

## Purpose

Allow operators to tune number-modal behavior for the current browser session without a database. Settings MUST reset to defaults when the browser session ends (`sessionStorage` only).

## Requirements

### Requirement: Configuration page

The system MUST serve `GET /configuracion` (and `/configuracion/`) as an HTML page to edit session settings, with navigation back to the home bingo page.

#### Scenario: Open configuration

- GIVEN the server is running
- WHEN the user opens `/configuracion`
- THEN a configuration form MUST be shown
- AND saving MUST NOT persist values to any backend database

### Requirement: Modal duration (seconds)

The user MUST be able to set how many seconds the number modal stays open. Allowed range: 1–30 inclusive. Default MUST be **3** seconds when no session value exists.

#### Scenario: Default duration

- GIVEN a new browser session with empty `sessionStorage`
- WHEN a bolilla modal is shown
- THEN it MUST close after 3 seconds

#### Scenario: Custom duration

- GIVEN the user saved 5 seconds in configuration
- WHEN a bolilla modal is shown in that same session
- THEN it MUST close after 5 seconds

### Requirement: Modal size in centimeters

The user MUST be able to set the circular modal diameter in **centimeters** (range 3–20, default **8**). The number font size MUST scale proportionally to that diameter (implementation ratio: 55% of diameter).

#### Scenario: Proportional size

- GIVEN the user saved modal size 10 cm
- WHEN the modal opens
- THEN the circular overlay diameter MUST be 10 cm
- AND the number font size MUST be approximately 5.5 cm

### Requirement: Session-only persistence

Configuration values MUST be stored in `sessionStorage` keys managed by `static/js/config-store.js`. Closing the browser (ending the session) MUST return behavior to defaults on the next visit. Values MUST NOT be written to the server or a database.

#### Scenario: New session resets defaults

- GIVEN the user previously set non-default size and duration
- WHEN they fully close the browser and open the app again
- THEN duration MUST default to 3 s and size to 8 cm until changed again

### Requirement: Shared client helpers

Home and configuration pages MUST use the same `config-store.js` helpers so duration/size reads are consistent.

### Requirement: Configuration does not reset game

Opening `/configuracion` and returning to `/` MUST preserve server-side game state; only modal session preferences change.

#### Scenario: Config round-trip

- GIVEN balls already drawn on the server
- WHEN the operator saves modal settings and returns home
- THEN `/estado/` salidas MUST be unchanged by that navigation
- AND home MUST restore those salidas into the UI
