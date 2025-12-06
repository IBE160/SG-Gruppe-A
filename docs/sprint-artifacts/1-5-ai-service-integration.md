# Story 1.5: AI Service Integration and Proof-of-Concept

Status: ready-for-dev

## Story

As a developer,
I want to establish a connection to the AI service and validate its core functionalities,
so that we can de-risk the project and ensure the AI-powered features can be built.

## Acceptance Criteria

1.  Given the project is set up
    When a connection to the chosen LLM's API is attempted
    Then the connection is successful.
2.  Given the project is set up
    When a sample CV and job description are sent to the AI service
    Then the service can successfully parse the CV, analyze the job description, and generate a basic cover letter.

## Tasks / Subtasks

- [ ] Task 1: Setup AI Environment (AC: 1)
  - [ ] Subtask 1.1: Obtain API keys for Gemini 2.5 Flash/Pro.
  - [ ] Subtask 1.2: Configure environment variables for secure key storage.
  - [ ] Subtask 1.3: Install necessary Python libraries (e.g., `google-generativeai`, `pydantic-ai`, `fastapi`, `python-docx`).
- [ ] Task 2: Implement Proof-of-Concept Script (AC: 1, 2)
  - [ ] Subtask 2.1: Create a standalone Python script to authenticate with the API.
  - [ ] Subtask 2.2: Implement a function to read a sample `.docx` file (mock CV).
  - [ ] Subtask 2.3: Implement a function to send a prompt (parsed CV + Job Ad) to the model.
  - [ ] Subtask 2.4: Implement a function to receive and print the generated cover letter.
- [ ] Task 3: Testing & Validation (AC: 1, 2)
  - [ ] Subtask 3.1: Execute POC script and verify successful API connection and authentication (AC 1).
  - [ ] Subtask 3.2: Verify script output contains coherent text generated from the input prompt (AC 2).

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - Backend: Python with FastAPI.
  - AI Model: Gemini 2.5 Flash/Pro.
  - Library: Pydantic AI (as per project context).
  - Security: API keys must NEVER be committed to version control. Use `.env` files.
- **Source tree components to touch:**
  - `backend/requirements.txt` (or `pyproject.toml`)
  - `backend/.env.example`
  - `backend/poc/ai_test.py` (or similar path for the POC)
- **Testing standards summary:**
  - Manual verification of the script output.
  - Ensure no errors during API connection.

### Learnings from Previous Story

- **From Story 1.4 (User Logout):**
  - While Story 1.4 focused on user authentication/logout, this story (1.5) establishes the *technical* connection to the AI service.
  - Security practices established in 1.4 (and 1.1) regarding environment variables and secure configuration must be strictly adhered to here, especially for API key management.
  - Although this is a POC, the foundational code should align with the backend structure established in earlier stories.

### Project Structure Notes

- Alignment with unified project structure (paths, modules, naming):
  - Ensure the backend setup aligns with the planned `backend/` directory structure.
- Detected conflicts or variances (with rationale):
  - Tech spec for Epic 1 does not explicitly detail this story, but it is present in `docs/epics.md` and is a critical predecessor for Epic 2 and 3.

### References

- [Source: docs/epics.md#Story-1.5-AI-Service-Integration-and-Proof-of-Concept]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md]
- [Source: docs/architecture.md]
- [Source: docs/sprint-artifacts/1-4-user-logout.md]
- [Source: .gemini/GEMINI.md] (For model selection)

## Dev Agent Record

### Context Reference

- `docs/sprint-artifacts/1-5-ai-service-integration.context.xml`

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- 2025-12-06: Updated status to ready-for-dev after generating context.
- 2025-12-06: Initial draft created and updated to address validation findings (status update, added references, improved testing tasks).
