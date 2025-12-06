# Story 2.3: Job Description Input

Status: ready-for-dev

## Story

As a user,
I want to paste a job description into a text area,
so that the system can analyze it.

## Acceptance Criteria

1.  Given a user is on the dashboard
    When they paste text into the job description text area
    Then the text is successfully captured by the application.

## Tasks / Subtasks

- [ ] Task 1: Frontend Job Description Component (AC: 1)
  - [ ] Subtask 1.1: Create a text area component in React for pasting job descriptions.
  - [ ] Subtask 1.2: Implement basic client-side validation (e.g., minimum character count) to ensure meaningful input.
  - [ ] Subtask 1.3: Create a "Save" or "Analyze" button to trigger the submission.
- [ ] Task 2: Backend Job Description Endpoint (AC: 1)
  - [ ] Subtask 2.1: Implement `POST /api/job-description` endpoint in Node.js/Express.
  - [ ] Subtask 2.2: Validate the input text (ensure it's not empty or too long).
  - [ ] Subtask 2.3: Save the job description text to the `JobDescription` table in PostgreSQL.
  - [ ] Subtask 2.4: Link the job description to the authenticated user (user_id).
- [ ] Task 3: Testing (AC: 1)
  - [ ] Subtask 3.1: Unit test the frontend component for state updates on text input.
  - [ ] Subtask 3.2: Integration test the API endpoint with valid and empty text.
  - [ ] Subtask 3.3: Verify that the job description is correctly persisted in the database.

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - **Frontend:** Next.js, Tailwind CSS (for the text area styling).
  - **Backend:** Node.js, Express.js.
  - **Database:** PostgreSQL (`JobDescription` table).
  - **Data Model:** See `tech-spec-epic-1.md` for `JobDescription Model` definition.
- **Source tree components to touch:**
  - Frontend: `src/components/job/JobDescriptionInput.tsx` (new).
  - Backend: `src/routes/jobRoutes.ts` (new), `src/controllers/jobController.ts` (new).
  - Database: Migration for `job_descriptions` table (if not already created in Epic 1).
- **Testing standards summary:**
  - Ensure input validation works on both client and server sides.

### Learnings from Previous Story

- **From Story 2.2 (CV Parsing):**
  - Story 2.2 handled the CV side of the analysis equation. This story (2.3) handles the Job Description side.
  - Similar to CV upload, the data needs to be stored in the Node.js backend's database first before it can be sent to the AI service for analysis (which will be a subsequent story, likely 2.4).
  - Security: Input sanitization is crucial here to prevent XSS or SQL injection, even though we are using an ORM/query builder (implied by "PostgreSQL" and standard Node practices).

### Project Structure Notes

- Alignment with unified project structure:
  - Follow the pattern established in Story 2.1: Frontend components in `src/components`, Backend in `src/controllers` and `src/routes` (assuming the standard `node-api` structure).
- Detected conflicts or variances:
  - `epics.md` places this in Epic 2. `tech-spec-epic-1.md` defines the `JobDescription Model`. This confirms the pattern of using Epic 1 spec for foundational data structures used in Epic 2 features.

### References

- [Source: docs/epics.md#Story-2.3-Job-Description-Input]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#JobDescription-Model]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Job-Description-API]
- [Source: docs/sprint-artifacts/2-2-cv-parsing.md]

## Dev Agent Record

### Context Reference

- `docs/sprint-artifacts/2-3-job-description-input.context.xml`

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- 2025-12-06: Updated status to ready-for-dev after generating context.
- 2025-12-06: Initial draft created.
