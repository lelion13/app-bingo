# Delta for UI

## ADDED Requirements

### Requirement: Login page

The system MUST serve a login UI. Unauthenticated visits to the control panel (`/`, `/configuracion`, admin ABM) MUST redirect or route to login.

#### Scenario: Anonymous home

- GIVEN no valid session/token
- WHEN the client opens `/`
- THEN the user MUST be prompted to login before control actions

### Requirement: Admin users screen

Admin MUST have a users ABM UI to create, edit role/password, and deactivate. Operador MUST NOT see ABM navigation.

#### Scenario: Operador UI

- GIVEN an operador is logged in
- WHEN they use the control panel
- THEN user-management controls MUST NOT be available

### Requirement: Per-user visor URL

The public viewer MUST be at `GET /visor/<usuario>`. Bare `GET /visor` MUST NOT serve another user's game (404 or explicit non-game response).

#### Scenario: Open juan visor

- GIVEN user `juan` exists
- WHEN a client opens `/visor/juan`
- THEN juan's drawn numbers MUST be shown read-only

## MODIFIED Requirements

### Requirement: Production visor QR on home

The home QR MUST encode `https://bingo.lionapp.cloud/visor/<username>` for the **logged-in** user (not a shared `/visor`).

(Previously: always `https://bingo.lionapp.cloud/visor`.)

#### Scenario: Scan opens own visor

- GIVEN user `maria` is logged in on home
- WHEN a device scans the QR
- THEN it MUST open `https://bingo.lionapp.cloud/visor/maria`

### Requirement: Friendly visor link on home

Visible text MUST be `bingo.lionapp.cloud/visor/<username>`; href MUST be the matching HTTPS URL.

(Previously: `bingo.lionapp.cloud/visor`.)

### Requirement: Mobile viewer page

Viewer path MUST be `/visor/<usuario>`; behavior (read-only, no controls) unchanged.

(Previously: `/visor` only.)

### Requirement: Live sync via estado

Viewer MUST poll scoped public estado for that username (~1–2s).

(Previously: global `/estado/`.)
