# Auth Specification

## Purpose

Authenticate operators, authorize admin ABM, and issue short-lived JWTs for the control panel. Visor remains public.

## Requirements

### Requirement: Roles

The system MUST support roles `admin` and `operador`. Only `admin` MUST access user ABM endpoints and UI.

#### Scenario: Operador blocked from ABM

- GIVEN a valid JWT for an `operador`
- WHEN that client calls a user-management endpoint
- THEN the response MUST be 403

### Requirement: Password storage

Passwords MUST be stored with bcrypt (salted hash). Plain-text passwords MUST NEVER be logged, returned, or stored.

#### Scenario: Create user hashes password

- GIVEN an admin creates a user with password P
- WHEN the user record is persisted
- THEN only a bcrypt hash MUST be stored
- AND API responses MUST NOT include P or the hash

### Requirement: Login issues JWT

`POST /auth/login` MUST accept username + password and return a JWT access token on success. Failures MUST use a generic message (no user enumeration).

#### Scenario: Valid login

- GIVEN an active user with correct password
- WHEN they POST login credentials
- THEN the response MUST include an access token
- AND MUST NOT expose password material

#### Scenario: Bad credentials

- GIVEN wrong password or unknown username
- WHEN login is attempted
- THEN the response MUST be 401 with a generic error
- AND MUST NOT reveal whether the username exists

### Requirement: Deactivated users cannot authenticate

A user marked inactive MUST NOT receive a new JWT and MUST NOT access protected routes.

#### Scenario: Deactivated login

- GIVEN a deactivated user
- WHEN they attempt login
- THEN the response MUST be 401

### Requirement: Protected control routes

Home control APIs (draw, reset, own estado for panel, config read/write) and ABM MUST require a valid JWT (signature, expiry, required claims). `/health` and public visor/estado-by-user MUST NOT require JWT.

#### Scenario: Draw without token

- GIVEN no Authorization header
- WHEN `GET /sacar_bolilla/` (or scoped equivalent) is called
- THEN the response MUST be 401

### Requirement: Bootstrap first admin

The system MUST provide a one-shot CLI/script that creates the first `admin` (and their bingo) when invoked. Empty DB MUST NOT auto-create an admin from env alone.

#### Scenario: Bootstrap creates admin

- GIVEN an empty user table
- WHEN the bootstrap command runs with username/password
- THEN an active `admin` user MUST exist
- AND exactly one bingo MUST exist for that user

### Requirement: User ABM (admin only)

Admin MUST be able to create users, edit role and password, and deactivate users. Hard delete MUST NOT be offered.

#### Scenario: Create operador with bingo

- GIVEN an authenticated admin
- WHEN they create an `operador` with username U
- THEN U MUST be active with role operador
- AND exactly one bingo for U MUST exist

#### Scenario: Deactivate

- GIVEN an active user U
- WHEN admin deactivates U
- THEN U MUST NOT login
- AND U's bingo data MUST remain in storage (not hard-deleted)
