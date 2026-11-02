# Delta for Configuration

## ADDED Requirements

### Requirement: Per-user server persistence

Modal duration (1–30s, default 3) and diameter cm (3–20, default 8) MUST be stored in SQLite for the authenticated user. Saving on `/configuracion` MUST update that user's row. Loading home/config MUST use server values for the logged-in user.

#### Scenario: Follows login across devices

- GIVEN user A saved duration 7 and size 10
- WHEN A logs in on another browser and opens home
- THEN modal behavior MUST use 7s and 10 cm

#### Scenario: Unauthenticated config

- GIVEN no JWT
- WHEN a client tries to save configuration via API
- THEN the response MUST be 401

## MODIFIED Requirements

### Requirement: Configuration page

`GET /configuracion` MUST require authentication (same session/JWT as panel). Saving MUST persist to the backend for that user.

(Previously: open page; save only to sessionStorage; no DB.)

### Requirement: Session-only persistence

(Previously: sessionStorage-only, reset on browser close.)

Configuration MUST NOT rely on sessionStorage as the source of truth. Client MAY cache server values for the session but MUST load/save via authenticated API.

#### Scenario: Browser restart keeps settings

- GIVEN user A saved non-default settings
- WHEN A closes the browser fully and logs in again
- THEN duration and size MUST still be A's saved values

### Requirement: Shared client helpers

`config-store.js` (or successor) MUST read/write through the authenticated config API helpers so home and configuration stay consistent with server state.

(Previously: sessionStorage keys only.)
