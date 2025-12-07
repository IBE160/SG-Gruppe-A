# Story 2.1: CV Upload

Status: ready-for-dev

## Story

As a user,
I want to upload my CV in `.doc` or `.docx` format,
so that the system can analyze it.

## Acceptance Criteria

1.  Given a user is on the dashboard
    When they select a `.doc` or `.docx` file to upload
    And they click "Upload"
    Then the file is successfully uploaded to the server.

## Tasks / Subtasks

- [ ] Task 1: Frontend CV Upload Component (AC: 1)
  - [ ] Subtask 1.1: Create a file input component in React that accepts only `.doc` and `.docx` extensions.
  - [ ] Subtask 1.2: Implement a progress indicator for the upload process.
  - [ ] Subtask 1.3: Integrate with the backend upload endpoint.
  - [ ] Subtask 1.4: Handle upload errors (e.g., wrong format, file too large) and display user-friendly messages.
- [ ] Task 2: Backend CV Upload Endpoint (AC: 1)
  - [ ] Subtask 2.1: Implement `POST /api/cv/upload` endpoint in Python/FastAPI.
  - [ ] Subtask 2.2: Configure `python-multipart` to handle multipart/form-data.
  - [ ] Subtask 2.3: Validate file type (ensure actual .doc/.docx MIME type) and size limit.
  - [ ] Subtask 2.4: Store the file securely (local storage for dev, prepared for S3/blob storage).
  - [ ] Subtask 2.5: Save metadata to the `CV` table in PostgreSQL (filename, upload timestamp, user_id).
- [ ] Task 3: Testing (AC: 1)
  - [ ] Subtask 3.1: Unit test the upload component's validation logic.
  - [ ] Subtask 3.2: Integration test the API endpoint with valid and invalid files using `TestClient`.
  - [ ] Subtask 3.3: Manual verification of the full upload flow.

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - **Frontend:** Next.js, Tailwind CSS, shadcn/ui.
  - **Backend:** Python, FastAPI, PostgreSQL, python-multipart.
  - **Security:** Validate file types strictly to prevent malicious uploads. Files should be stored outside the web root or in a private bucket.
  - **Data Model:** See `tech-spec-epic-1.md` for `CV Model` definition.
- **Source tree components to touch:**
  - Frontend: `src/components/cv/CVUpload.tsx` (new)
  - Backend: `app/routers/cv.py` (new), `app/services/cv_service.py` (new)
  - Database: Migration for `cv_files` table.
- **Testing standards summary:**
  - Verify both success and error states (e.g., network fail, invalid file).

### Learnings from Previous Story

- **From Story 1.5 (AI Service POC):**
  - Story 1.5 established the technical foundation for AI integration. This story builds the *primary* backend infrastructure in Python/FastAPI to ingest the data.
  - Ensure that the file storage mechanism chosen here is accessible to the parsing logic.
  - Adhere to the security patterns established in earlier stories (env vars, secure config).

### Project Structure Notes

- Alignment with unified project structure:
  - Frontend components in `src/components` (or `components/`).
  - Backend routes in `backend/app/routers`.
- Detected conflicts or variances:
  - `epics.md` places CV Upload in Epic 2. `tech-spec-epic-1.md` details it technically. I am using `tech-spec-epic-1.md` for technical details but `epics.md` for numbering.

### References

- [Source: docs/epics.md#Story-2.1-CV-Upload]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#CV-API]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Data-Models-and-Contracts]
- [Source: docs/sprint-artifacts/1-5-ai-service-integration.md]

## Dev Agent Record

### Context Reference

- `docs/sprint-artifacts/2-1-cv-upload.context.xml`

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- 2025-12-06: Updated status to ready-for-dev after generating context.
- 2025-12-06: Initial draft created.
