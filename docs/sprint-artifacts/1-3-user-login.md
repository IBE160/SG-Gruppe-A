# Story 1.3: User Login

Status: ready-for-dev

## Story

As a registered user,
I want to be able to log in with my email and password,
so that I can access my account and saved data.

## Acceptance Criteria

1.  Given a user is on the login page
    When they enter their correct email and password
    And they click the "Log In" button
    Then the system authenticates the user
    And a JWT token is returned to the client
    And the user is redirected to their dashboard.

## Tasks / Subtasks

- [ ] Task 1: Implement Backend Login Endpoint (AC: 1)
  - [ ] Subtask 1.1: Create `POST /api/v1/auth/login` endpoint
  - [ ] Subtask 1.2: Implement password verification (using bcrypt)
  - [ ] Subtask 1.3: Implement JWT token generation
  - [ ] Subtask 1.4: Securely return JWT (e.g. HttpOnly cookie)
  - [ ] Subtask 1.5: Create unit tests for login logic (success, invalid credentials)
  - [ ] Subtask 1.6: Create integration test for `/login` endpoint
- [ ] Task 2: Implement Frontend Login Form (AC: 1)
  - [ ] Subtask 2.1: Create Login Page UI
  - [ ] Subtask 2.2: Implement form state and validation
  - [ ] Subtask 2.3: Connect form submission to backend API
  - [ ] Subtask 2.4: Handle successful login (redirect to dashboard)
  - [ ] Subtask 2.5: Handle login errors (display error message)
  - [ ] Subtask 2.6: Create unit/component tests for LoginForm interaction

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - Backend: Python/FastAPI
  - Database: PostgreSQL (User model)
  - Authentication: JWT (Json Web Token)
  - Security: Passlib (bcrypt) for password hashing, HttpOnly cookies for token storage
- **Source tree components to touch:**
  - `backend/main.py` (or router file)
  - `backend/app/api/auth.py` (or similar)
  - `frontend/pages/login.tsx` (or similar)
  - `frontend/components/LoginForm.tsx`
- **Testing standards summary:**
  - Unit tests for backend login logic (success, invalid credentials) using `pytest`.
  - Integration tests for API endpoint using `TestClient`.
  - Frontend tests for form interaction.

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming):
  - Backend routes should follow standard FastAPI patterns (Routers).
  - Frontend should use Next.js pages/app directory structure.
  - File paths above are indicative; follow structure established in Story 1.1/1.2.
- Detected conflicts or variances (with rationale):
  - None.

### References

- [Source: docs/epics.md#Story-1.3-User-Login]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md]
- [Source: docs/architecture.md]

## Dev Agent Record

### Context Reference

- `docs/sprint-artifacts/1-3-user-login.context.xml`
- `docs/sprint-artifacts/1-3-user-login.context.xml`

### Agent Model Used

gemini-2.5-flash

### Debug Log References

### Completion Notes List

### File List