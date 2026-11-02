# Delta for Game

## ADDED Requirements

### Requirement: One bingo per user

Each user MUST own exactly one bingo-of-90 instance. Creating a user MUST create that bingo. Admin users MUST also own a bingo.

#### Scenario: Isolation

- GIVEN users A and B each with draws in progress
- WHEN A draws a bolilla
- THEN B's `/estado` for B MUST be unchanged
- AND A's salidas MUST include the new bolilla

### Requirement: Scoped public estado

`GET /estado/<usuario>` (or equivalent path) MUST return that user's `restantes`, `salidas`, and `total` 90 without mutating state and without JWT.

#### Scenario: Unknown user

- GIVEN username Z does not exist
- WHEN a client requests estado for Z
- THEN the response MUST be 404

### Requirement: Authenticated own-game mutations

`iniciar_bingo` and `sacar_bolilla` MUST apply only to the authenticated user's bingo.

#### Scenario: Cannot mutate another bingo

- GIVEN JWT for user A
- WHEN A attempts to draw against user B's bingo
- THEN the system MUST reject the request (403/404)
- AND B's pool MUST be unchanged

## MODIFIED Requirements

### Requirement: Ninety-ball pool

The system MUST maintain, **per user bingo**, a shuffled pool of 1–90 and ordered `salidas`, persisted in SQLite (not process-global memory alone).

(Previously: single process-memory pool.)

#### Scenario: Survives restart

- GIVEN user A has drawn balls
- WHEN the app process restarts with the same SQLite file
- THEN A's `/estado/<A>` MUST still show the same `salidas`

### Requirement: Start / reset game

Authenticated reset MUST reshuffle only the caller's bingo.

(Previously: global `/iniciar_bingo/`.)

### Requirement: Draw ball

Authenticated draw MUST pop from the caller's pool only.

(Previously: global `/sacar_bolilla/`.)

### Requirement: Query state

Unscoped global `/estado/` MUST NOT expose a shared game. Panel MAY use authenticated own-estado; visor MUST use public `/estado/<usuario>`.

(Previously: single public `/estado/`.)

### Requirement: Viewer consumes public estado

The viewer MUST poll the **scoped** public estado for the username in the URL. It MUST NOT call mutating endpoints.

(Previously: poll global `/estado/`.)

### Requirement: Caution — persistence

Game state MUST persist in SQLite across restarts when the DB file is retained. Multi-worker still requires a single shared DB file/locking awareness.

(Previously: process-local memory only caution.)

## REMOVED Requirements

### Requirement: (none named — global unscoped game APIs as sole surface)

(Reason: replaced by per-user scoped APIs; bare unscoped mutating routes MUST NOT remain as the multi-tenant surface.)
