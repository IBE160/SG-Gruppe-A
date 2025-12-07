# Story 1.4: User Logout

Status: ready-for-dev

## Story

As an authenticated user,
I want to be able to log out of the application using Supabase Authentication,
so that my session is terminated and my account is secure.

## Acceptance Criteria

*   **Given** an authenticated user is in the application
*   **When** they click the "Log Out" button
*   **Then** their Supabase session is terminated
*   **And** they are redirected to the homepage or login page.

## Tasks / Subtasks

- **Frontend Development:**
    - Implement a "Log Out" button in the appropriate UI component (e.g., navigation bar, user profile dropdown).
    - Attach an event handler to the "Log Out" button to:
        - Call Supabase `signOut` method (`supabase.auth.signOut()`).
        - Ensure client-side session/cookies are cleared.
        - Redirect the user to the homepage/login page.
- **Backend/Server-Side:**
    - Ensure Supabase server-side client (if used in middleware/actions) respects the logout and clears cookies.

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - Authentication: Supabase Auth (`supabase.auth.signOut`).
  - Frontend: Next.js (App Router).
- **Source tree components to touch:**
  - `frontend/components/SignOutButton.tsx` (or similar)
  - `frontend/app/login/actions.ts` (if using Server Action for logout)
  - `frontend/utils/supabase/server.ts`
- **Testing standards summary:**
  - Verify "Log Out" button appears only when authenticated.
  - Verify clicking it redirects to home/login and clears session.

### References

- [Source: docs/epics.md#Story-14-User-Logout]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Authentication-API]
- [Source: docs/architecture.md#32-Backend-API]

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/1-4-user-logout.context.xml

### Agent Model Used

gemini-1.5-pro

### Debug Log References

### Completion Notes List

### File List
