# Story 1.4: User Logout

Status: ready-for-dev

## Story

As an authenticated user,
I want to be able to log out of the application,
so that my session is terminated and my account is secure.

## Acceptance Criteria

*   **Given** an authenticated user is in the application
*   **When** they click the "Log Out" button
*   **Then** their session is terminated
*   **And** they are redirected to the homepage.

## Tasks / Subtasks

- **Frontend Development:**
    - Implement a "Log Out" button in the appropriate UI component (e.g., navigation bar, user profile dropdown).
    - Attach an event handler to the "Log Out" button to:
        - Call the backend logout API (`POST /api/auth/logout`).
        - Clear the client-side JWT token (e.g., from local storage or cookies).
        - Redirect the user to the homepage.
- **Backend Development:**
    - Create a `POST /api/auth/logout` endpoint. (Source: `tech-spec-epic-1.md`)
    - Implement logic within the endpoint to:
        - Invalidate the JWT token if a server-side token invalidation mechanism is in place (e.g., by adding to a blacklist).
        - Ensure the response to the client indicates successful logout.
- **Testing:**
    - **Unit Tests:**
        - Verify Frontend `logout` function correctly clears JWT and redirects.
        - Verify Backend `POST /api/auth/logout` endpoint handles token invalidation correctly (if applicable).
    - **Integration Tests:**
        - Test the full flow: login, then logout, and attempt to access a protected route (should fail).
        - Verify the client-side token is successfully removed after logout.
    - **E2E Tests:**
        - Simulate a user logging in, navigating, and then logging out, verifying redirection to the homepage.
    - **Security Testing:**
        - Ensure the logout endpoint is secure and cannot be exploited.

## Dev Notes

### Requirements & Context Summary for Story 1.4: User Logout

**User Story Statement:**
As an authenticated user, I want to be able to log out of the application, so that my session is terminated and my account is secure.

**Source Epic:** Epic 1: Foundation & User Onboarding
**Source PRD Requirements:** FR002 (The system must allow authenticated users to log in and log out.)

**Acceptance Criteria:**
*   **Given** an authenticated user is in the application
*   **When** they click the "Log Out" button
*   **Then** their session is terminated
*   **And** they are redirected to the homepage.

**Technical Context from Tech Spec (Epic 1):**
*   **Authentication API:** `POST /api/auth/logout`: User logout (invalidate token server-side or client-side clear).

**Architectural Considerations:**
*   **Authentication Mechanism:** JSON Web Tokens (JWT) are used for stateless and secure user authentication. Session termination will involve discarding the JWT token on the client-side, and potentially server-side invalidation if applicable.

**Related Technical Notes from Epic:**
*   The client should discard the JWT token. If using server-side sessions, the session should be invalidated.

### Project Structure Alignment and Lessons Learned

**Learnings from Previous Story:** First story in epic - no predecessor context.

**Relevant Project Structure:**
*   **Frontend (Next.js Application)**: Will contain the UI for the logout button and handle client-side JWT token disposal.
*   **Backend (Node.js/Express.js API)**: Will provide the `/api/auth/logout` endpoint to handle server-side session termination if necessary, and potentially invalidate the JWT.

No specific file paths, module names, or component locations are explicitly mandated by `unified-project-structure.md` (which is not present). Alignment will follow general project conventions for Frontend and Backend API development.

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