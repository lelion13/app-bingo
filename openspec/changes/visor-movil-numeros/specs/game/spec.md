# Delta for Game

## ADDED Requirements

### Requirement: Viewer consumes public estado

The existing `GET /estado/` endpoint MUST remain sufficient for a read-only viewer; no new mutating endpoints are required for this change.

#### Scenario: Viewer does not mutate

- GIVEN the viewer page is open
- WHEN it polls for updates
- THEN it MUST only call read endpoints (e.g. `/estado/`)
- AND MUST NOT call `/iniciar_bingo/` or `/sacar_bolilla/`
