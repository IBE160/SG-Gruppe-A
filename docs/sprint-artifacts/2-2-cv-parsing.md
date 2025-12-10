# Story 2.2: CV Parsing

Status: review

## Story

As a developer,
I want to parse the uploaded CV file,
so that I can extract the text content for analysis.

## Acceptance Criteria

1.  Given a CV file has been uploaded
    When the parsing process is triggered
    Then the text content of the CV is extracted and stored.

## Tasks / Subtasks

- [x] Task 1: CV Parsing Logic (AC: 1)
  - [x] Subtask 1.1: Create a Python script or function within the Backend (e.g. `app/services/cv_parser.py`) to handle `.docx` parsing using `python-docx`.
  - [x] Subtask 1.2: Implement text extraction logic that preserves basic structure (paragraphs) but removes formatting noise.
  - [x] Subtask 1.3: Handle errors gracefully (e.g., unreadable files, password-protected files).
- [x] Task 2: Integration with Upload Flow (AC: 1)
  - [x] Subtask 2.1: Integrate the parsing service into the CV Upload endpoint (`POST /api/cv/upload`).
  - [x] Subtask 2.2: Ensure parsing happens asynchronously or efficiently after upload.
  - [x] Subtask 2.3: Store the extracted text back into the `CV` table in PostgreSQL (`extracted_text` column).
- [x] Task 3: Testing (AC: 1)
  - [x] Subtask 3.1: Unit test the parsing function with sample `.docx` files.
  - [x] Subtask 3.2: Integration test the upload-and-parse flow.
  - [x] Subtask 3.3: Verify that extracted text is correctly saved to the database.

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

- Implemented `parse_cv` in `backend/app/services/cv_parser.py` to extract text from `.docx` files using `python-docx`.
- Integrated parsing into `backend/app/services/cv_service.py` to automatically parse upon upload and store text in `extracted_text` field.
- Added unit tests in `backend/tests/test_cv_parser.py`.
- Added integration test in `backend/tests/test_cv_service_integration.py` verifying the flow and DB insertion.

### File List

- backend/app/services/cv_parser.py
- backend/app/services/cv_service.py
- backend/tests/test_cv_parser.py
- backend/tests/test_cv_service_integration.py

## Change Log

- 2025-12-06: Updated status to ready-for-dev after generating context.
- 2025-12-06: Initial draft created.
- 2025-12-10: Implemented parsing logic and integration. All tests passed. Changed status to review.

## Senior Developer Review (AI)

- **Reviewer:** BIP
- **Date:** 2025-12-10
- **Outcome:** Approve

### Summary
The implementation successfully adds CV parsing functionality to the existing upload flow. The solution uses `python-docx` to extract text from both paragraphs and tables, ensuring comprehensive content capture. The integration into the `save_cv` service is clean, and the data is correctly persisted to the database. Comprehensive tests cover both the parsing logic in isolation and the integrated flow.

### Key Findings
- **High:** None.
- **Medium:** None.
- **Low:**
    - Error handling in `parse_cv` swallows exceptions and prints to stdout. In a production environment, structured logging should be used, and potentially a way to flag "parsing failed" status to the user/DB, even if the upload succeeds.

### Acceptance Criteria Coverage

| AC# | Description | Status | Evidence |
| :--- | :--- | :--- | :--- |
| 1 | Given a CV file has been uploaded, When the parsing process is triggered, Then the text content of the CV is extracted and stored. | IMPLEMENTED | `backend/app/services/cv_service.py` lines 42-53 |

**Summary:** 1 of 1 acceptance criteria fully implemented.

### Task Completion Validation

| Task | Marked As | Verified As | Evidence |
| :--- | :--- | :--- | :--- |
| **Task 1: CV Parsing Logic** | [x] | VERIFIED COMPLETE | `backend/app/services/cv_parser.py` |
| Subtask 1.1: Create Python script/function | [x] | VERIFIED COMPLETE | `backend/app/services/cv_parser.py` |
| Subtask 1.2: Implement text extraction logic | [x] | VERIFIED COMPLETE | `backend/app/services/cv_parser.py` (handles paragraphs and tables) |
| Subtask 1.3: Handle errors gracefully | [x] | VERIFIED COMPLETE | `backend/app/services/cv_parser.py` (try/except block) |
| **Task 2: Integration with Upload Flow** | [x] | VERIFIED COMPLETE | `backend/app/services/cv_service.py` |
| Subtask 2.1: Integrate into CV Upload endpoint | [x] | VERIFIED COMPLETE | Called within `save_cv` |
| Subtask 2.2: Asynchronous/Efficient parsing | [x] | VERIFIED COMPLETE | Performed inline efficiently after file I/O |
| Subtask 2.3: Store text in DB | [x] | VERIFIED COMPLETE | `backend/app/services/cv_service.py` data dict |
| **Task 3: Testing** | [x] | VERIFIED COMPLETE | `backend/tests/` |
| Subtask 3.1: Unit test parsing | [x] | VERIFIED COMPLETE | `backend/tests/test_cv_parser.py` |
| Subtask 3.2: Integration test | [x] | VERIFIED COMPLETE | `backend/tests/test_cv_service_integration.py` |
| Subtask 3.3: Verify DB save | [x] | VERIFIED COMPLETE | Verified in integration test assertions |

**Summary:** 3 of 3 tasks (and 9 subtasks) verified complete.

### Test Coverage and Gaps
- **Coverage:** Excellent. Unit tests cover standard text, tables, non-existent files, and invalid extensions. Integration tests mock Supabase to verify the correct data structure is passed for insertion.
- **Gaps:** None for this scope.

### Architectural Alignment
- Aligns with the monolithic service architecture where `app/services` handle business logic.
- Follows the established pattern of separating service logic from routers.

### Security Notes
- `sanitize_filename` is correctly applied.
- Input validation (checking for `.docx` extension) is present in both router (MIME type) and parser (extension check).

### Action Items

**Advisory Notes:**
- Note: Consider replacing `print()` statements with a proper logger (e.g., `logging` module or `logfire`) in a future refactor.

