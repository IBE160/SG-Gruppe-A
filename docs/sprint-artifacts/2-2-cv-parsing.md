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
  - [ ] Subtask 1.1: Create a Python script or function within the AI Service to handle `.docx` parsing using `python-docx`.
  - [ ] Subtask 1.2: Implement text extraction logic that preserves basic structure (paragraphs) but removes formatting noise.
  - [ ] Subtask 1.3: Handle errors gracefully (e.g., unreadable files, password-protected files).
- [ ] Task 2: Integration with Upload Flow (AC: 1)
  - [ ] Subtask 2.1: Define a trigger mechanism (e.g., an API call from the Node.js backend to the Python AI Service, or a shared database polling/queue). *Decision:* Use a direct API call for the MVP (`POST /ai/parse-cv`).
  - [ ] Subtask 2.2: Implement the `POST /ai/parse-cv` endpoint in the FastAPI service.
  - [ ] Subtask 2.3: Update the Node.js backend to call this endpoint after successful file upload (from Story 2.1).
  - [ ] Subtask 2.4: Store the extracted text back into the `CV` table in PostgreSQL (`extracted_text` column).
- [ ] Task 3: Testing (AC: 1)
  - [ ] Subtask 3.1: Unit test the Python parsing function with sample `.docx` files.
  - [ ] Subtask 3.2: Integration test the communication between Node.js backend and Python AI service.
  - [ ] Subtask 3.3: Verify that extracted text is correctly saved to the database.

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - **AI Service:** Python, FastAPI, `python-docx`.
  - **Backend:** Node.js, Express.js (orchestrates the flow).
  - **Database:** PostgreSQL (stores the result).
  - **Inter-service Communication:** REST API (Node calls Python).
- **Source tree components to touch:**
  - AI Service: `app/services/cv_parser.py` (new), `app/main.py` (endpoint).
  - Backend: `src/services/aiService.ts` (new - wrapper for calling AI API), `src/controllers/cvController.ts` (update).
- **Testing standards summary:**
  - Verify extraction accuracy for standard CV layouts.
  - Ensure robust error handling for malformed files.

### Learnings from Previous Story

- **From Story 2.1 (CV Upload):**
  - Story 2.1 established the file storage and database record. Story 2.2 picks up immediately after the upload.
  - The file path stored in Story 2.1 is the key input for this story. The AI service needs access to this file.
  - *Constraint Check:* If the AI service runs in a separate container, it might not have local file system access to the upload folder of the Node backend.
  - *Refinement:* For the MVP, assume a shared volume or pass the file content directly if small enough. However, passing file paths is cleaner. If strictly separate, the Node backend might need to stream the file to the Python service. *Decision for MVP:* Node backend will read the file it just uploaded and send the *stream/buffer* to the Python service via the `POST /ai/parse-cv` request (multipart upload to the internal AI API). This avoids shared volume complexity.

### Project Structure Notes

- Alignment with unified project structure:
  - AI Service code should be in `ai-service/` or `backend/python/` depending on the repo structure. Based on 1.5 context, it seemed to be `backend/`. I will assume `backend/` is the Node app and `ai-service/` (or similar) is the Python app, OR `backend` is Python. *Wait*, Story 1.5 said "Backend: Python with FastAPI". Story 2.1 said "Backend: Node.js". This is a conflict in my previous assumptions or the project naming.
  - *Correction:* `tech-spec-epic-1.md` says:
    - "Backend (Node.js/Express.js API)"
    - "CV Handling Service... performs initial text extraction/parsing using a basic `python-docx` integration (potentially via a lightweight child process or early AI Service interaction...)"
  - *Clarification:* The project likely has *two* backend components. I will refer to them as `node-api` and `ai-service` to avoid confusion.
- Detected conflicts or variances:
  - Need to confirm folder names. I will assume standard separation.

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
