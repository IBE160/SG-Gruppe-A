# Story 2.2: CV Parsing

Status: ready-for-dev

## Story

As a developer,
I want to parse the uploaded CV file,
so that I can extract the text content for analysis.

## Acceptance Criteria

1.  Given a CV file has been uploaded
    When the parsing process is triggered
    Then the text content of the CV is extracted and stored.

## Tasks / Subtasks

- [ ] Task 1: CV Parsing Logic (AC: 1)
  - [ ] Subtask 1.1: Create a Python script or function within the Backend (e.g. `app/services/cv_parser.py`) to handle `.docx` parsing using `python-docx`.
  - [ ] Subtask 1.2: Implement text extraction logic that preserves basic structure (paragraphs) but removes formatting noise.
  - [ ] Subtask 1.3: Handle errors gracefully (e.g., unreadable files, password-protected files).
- [ ] Task 2: Integration with Upload Flow (AC: 1)
  - [ ] Subtask 2.1: Integrate the parsing service into the CV Upload endpoint (`POST /api/cv/upload`).
  - [ ] Subtask 2.2: Ensure parsing happens asynchronously or efficiently after upload.
  - [ ] Subtask 2.3: Store the extracted text back into the `CV` table in PostgreSQL (`extracted_text` column).
- [ ] Task 3: Testing (AC: 1)
  - [ ] Subtask 3.1: Unit test the parsing function with sample `.docx` files.
  - [ ] Subtask 3.2: Integration test the upload-and-parse flow.
  - [ ] Subtask 3.3: Verify that extracted text is correctly saved to the database.

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - **Backend:** Python, FastAPI, `python-docx`.
  - **Database:** PostgreSQL (stores the result).
- **Source tree components to touch:**
  - Backend: `app/services/cv_parser.py` (new), `app/routers/cv.py` (update).
- **Testing standards summary:**
  - Verify extraction accuracy for standard CV layouts.
  - Ensure robust error handling for malformed files.

### Learnings from Previous Story

- **From Story 2.1 (CV Upload):**
  - Story 2.1 established the file storage and database record. Story 2.2 picks up immediately after the upload.
  - The file path stored in Story 2.1 is the key input for this story. The parsing service needs access to this file.
  - Since the backend is unified (Python), file access is direct.

### Project Structure Notes

- Alignment with unified project structure:
  - Backend services in `app/services/`.
- Detected conflicts or variances:
  - None.

### References

- [Source: docs/epics.md#Story-2.2-CV-Parsing]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]
- [Source: docs/architecture.md#3.3.-AI-Service]
- [Source: docs/sprint-artifacts/2-1-cv-upload.md]

## Dev Agent Record

### Context Reference

- `docs/sprint-artifacts/2-2-cv-parsing.context.xml`

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- 2025-12-06: Updated status to ready-for-dev after generating context.
- 2025-12-06: Initial draft created.
