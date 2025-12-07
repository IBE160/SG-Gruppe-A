# Story 1.3: User Login

Status: ready-for-dev

## Story

As a registered user,
I want to be able to log in with my email and password using Supabase Authentication,
so that I can access my account and saved data.

## Acceptance Criteria

1.  Given a user is on the login page
    When they enter their correct email and password
    And they click the "Log In" button
    Then the system authenticates the user using Supabase
    And a session is established
    And the user is redirected to their dashboard.

## Tasks / Subtasks

- [ ] Task 1: Implement Supabase Login (AC: 1)
  - [ ] Subtask 1.1: Create/Update Login Page UI with email and password fields
  - [ ] Subtask 1.2: Implement form submission handler using Supabase `signInWithPassword`
  - [ ] Subtask 1.3: Handle Auth state changes and session persistence (via Supabase SSR/cookies)
  - [ ] Subtask 1.4: Handle login errors (e.g., wrong password, user not found)
  - [ ] Subtask 1.5: Redirect user to dashboard/home upon successful login
  - [ ] Subtask 1.6: Create unit/component tests for Login interaction

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - Authentication: Supabase Auth (`supabase.auth.signInWithPassword`).
  - Frontend: Next.js (App Router).
  - Use `@supabase/ssr` for server-side auth support and cookie management.
- **Source tree components to touch:**
  - `frontend/app/login/page.tsx`
  - `frontend/app/login/actions.ts` (Server Actions)
  - `frontend/utils/supabase/server.ts`
  - `frontend/utils/supabase/client.ts`
- **Testing standards summary:**
  - Frontend tests for form interaction and error display.
  - Integration tests for the Supabase login flow (mocking Supabase client).

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming):
  - Frontend should use Next.js App Router structure.
  - Supabase utilities in `frontend/utils/supabase`.

### References

- [Source: docs/epics.md#Story-1.3-User-Login]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md]
- [Source: docs/architecture.md]

## Dev Agent Record

### Context Reference

- `docs/sprint-artifacts/1-3-user-login.context.xml`

### Agent Model Used

gemini-2.5-flash

### Debug Log References

### Completion Notes List

### File List
