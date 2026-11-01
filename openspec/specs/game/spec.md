# Domain: Game (Bingo 90)

## Purpose

Define server-authoritative bingo-of-90 behavior: start/reset, draw, and state query. Client MUST restore UI from server state when returning to the home page so navigation (e.g. to configuration) does not appear to reset the game.

## Requirements

### Requirement: Ninety-ball pool

The system MUST maintain a shuffled pool of integers 1 through 90 inclusive, plus an ordered list of drawn balls, in process memory.

#### Scenario: Fresh process

- GIVEN the FastAPI process has just started
- WHEN no draws have occurred yet
- THEN `/estado/` SHALL report `total` 90, `restantes` 90, and `salidas` as an empty list

### Requirement: Start / reset game

`GET /iniciar_bingo/` MUST reset the pool to a new shuffle of 1–90 and clear drawn balls.

#### Scenario: Reset mid-game

- GIVEN some balls have already been drawn
- WHEN the client calls `GET /iniciar_bingo/`
- THEN the response MUST include a success message and `total` 90
- AND subsequent `/estado/` MUST show `restantes` 90 and empty `salidas`

### Requirement: Draw ball

`GET /sacar_bolilla/` MUST remove one ball from the available pool (front of shuffled list), append it to `salidas`, and return the ball plus remaining counts.

#### Scenario: Successful draw

- GIVEN at least one ball remains
- WHEN the client calls `GET /sacar_bolilla/`
- THEN the response MUST include `bolilla`, `restantes`, and full `salidas`
- AND that `bolilla` MUST NOT appear again until a reset

#### Scenario: Pool exhausted

- GIVEN no balls remain
- WHEN the client calls `GET /sacar_bolilla/`
- THEN the response MUST indicate an error / completed bingo condition without inventing a new number

### Requirement: Query state

`GET /estado/` MUST return current `restantes`, `salidas`, and `total` (90) without mutating state.

#### Scenario: Idempotent read

- GIVEN a mid-game state
- WHEN `/estado/` is called twice
- THEN both responses MUST match and the pool MUST be unchanged

### Requirement: Home restores client UI from server

Loading `GET /` MUST result in the client fetching `/estado/` and syncing counter, last-drawn display, and “Últimas” list. Navigating away to configuration and back MUST NOT call `/iniciar_bingo/` implicitly.

#### Scenario: Return from configuration

- GIVEN a game in progress on the server
- WHEN the user opens `/configuracion` and then returns to `/`
- THEN the home UI MUST reflect the same `restantes` and `salidas` as `/estado/`
- AND the game MUST NOT have been reset

### Caution: In-memory limits

Game state MUST be understood as process-local: it is lost on server restart and is not safe across multiple workers without shared storage.
