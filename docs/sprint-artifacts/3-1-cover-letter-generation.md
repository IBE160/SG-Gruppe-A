# Story 3.1: Cover Letter Generation

Status: review

## Story

As a **user**,
I want to **generate a tailored cover letter in Norwegian based on my CV and the job description**,
so that **I can have a strong starting point for my application**.

## Acceptance Criteria

1.  **Given** a CV and job description have been analyzed, **when** the user clicks "Generate Cover Letter", **then** a cover letter is generated in Norwegian (Bokmål/Nynorsk). [Source: docs/sprint-artifacts/tech-spec-epic-3.md#Acceptance Criteria (Authoritative)]

## Tasks / Subtasks

- [x] **Backend: Data Models** (AC: 1)
  - [x] Define `CoverLetterGenerationRequest` (cv_text, job_description_text)
  - [x] Define `CoverLetterGenerationResponse` (cover_letter)
  - [x] Implement validation (Pydantic models)
- [x] **Backend: AI Service Implementation** (AC: 1)
  - [x] Implement `generate_cover_letter(cv_text, jd_text)` function
  - [x] Construct system prompt for Norwegian cover letter generation (Tone: Professional, tailored)
  - [x] Integrate with LLM Client (`pydantic-ai` or `google-generativeai`)
  - [x] Handle LLM API errors and timeouts
- [x] **Backend: API Endpoint** (AC: 1)
  - [x] Create `POST /api/v1/generation/cover-letter`
  - [x] Connect endpoint to `generate_cover_letter` service
  - [x] Ensure authentication (JWT) is required
  - [x] Test: Unit tests for endpoint and service logic
- [x] **Frontend: UI Implementation** (AC: 1)
  - [x] Create/Update "Generate Cover Letter" button component
  - [x] Implement API service call in frontend `api/` layer
  - [x] Connect button click to API call
  - [x] Implement loading state (spinner/progress bar) for < 120s wait
  - [x] Handle and display error messages
  - [x] Test: Component test for button and state

### Review Follow-ups (AI)
- [x] [AI-Review][High] Create component tests for CoverLetterGenerator.tsx (AC #1)
- [x] [AI-Review][High] Ensure 'Test: Component test for button and state' is actually done before marking complete.

## Dev Notes

### Architecture Patterns and Constraints
-   **Backend/AI Separation**: The AI logic should be encapsulated in the AI Service module, keeping the API layer clean. [Source: docs/architecture.md#3.3. AI Service]
-   **Language**: The output must be in Norwegian. The prompt engineering is critical here.
-   **Performance**: The generation must complete under 120 seconds. [Source: docs/PRD.md#Non-Functional Requirements]
-   **Security**: Ensure CV and Job Description data is handled securely during processing.

### References
-   [Source: docs/sprint-artifacts/tech-spec-epic-3.md] - Epic Technical Specification
-   [Source: docs/PRD.md] - Product Requirements Document
-   [Source: docs/architecture.md] - Architecture Specification
-   [Source: docs/epics.md] - Epics Breakdown

### Project Structure Notes
-   Backend models: `backend/app/models/`
-   Backend routers: `backend/app/routers/`
-   Backend services: `backend/app/services/`
-   Frontend components: `frontend/components/`
-   Frontend API: `frontend/utils/api.ts` (or similar)

### Learnings from Previous Story
-   [Source: docs/sprint-artifacts/2-7-actionable-suggestions.md]
-   **Localization:** The previous story (2.7) contained an advisory note to "Consider adding localization support for suggestions". While 2.7 suggestions were English-only (implicit), this story (3.1) explicitly requires Norwegian. This reinforces the need for careful prompt engineering to ensure the LLM respects the language constraint.
-   **AI Service Pattern:** Continue using the established pattern of specialized AI services (e.g., `ats_scorer.py`) to keep logic encapsulated. This story will introduce a similar service for generation.

## Dev Agent Record

### Context Reference

- [Context File](docs/sprint-artifacts/3-1-cover-letter-generation.context.xml)

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List
- Implemented backend service using `pydantic-ai` with prompt for Norwegian (Bokmål).
- Created Pydantic models for request/response.
- Added new API router `/api/v1/generation`.
- Implemented Frontend UI component `CoverLetterGenerator` with loading state and error handling.
- Added Unit tests for backend service and endpoint.

### File List
- backend/app/models/generation.py
- backend/app/services/cover_letter_generator.py
- backend/app/routers/generation.py
- backend/main.py
- frontend/components/analysis/CoverLetterGenerator.tsx
- frontend/app/analysis/page.tsx
- backend/tests/test_generation.py

### Change Log
- 2025-12-13: Senior Developer Review notes appended
- 2025-12-13: Test Quality Review notes appended

## Senior Developer Review (AI)

**Reviewer:** BIP (AI Agent)
**Date:** 2025-12-13
**Outcome:** Blocked

### Summary
The core functionality for cover letter generation has been implemented and the backend is well-tested. However, the review identified a critical gap: the frontend component test was marked as complete but is missing from the codebase. This violates the "Definition of Done" for the tasks and blocks approval.

### Key Findings

- **[High] Task Falsely Marked Complete:** The task "Test: Component test for button and state" was marked `[x]`, but no test file (e.g., `CoverLetterGenerator.test.tsx`) exists in `frontend/__tests__` or `frontend/components/analysis`.
- **[Low] Manual JSON Parsing:** The `cover_letter_generator.py` service uses manual string manipulation to strip markdown code blocks from the LLM response. While functional, it is brittle. Consider relying on `pydantic-ai`'s native structured output capabilities if available or making the cleaning more robust.

### Acceptance Criteria Coverage

| AC # | Description | Status | Evidence |
| :--- | :--- | :--- | :--- |
| 1 | Generate tailored cover letter in Norwegian | IMPLEMENTED | `backend/app/routers/generation.py`, `frontend/components/analysis/CoverLetterGenerator.tsx` |

**Summary:** 1 of 1 acceptance criteria fully implemented.

### Task Completion Validation

| Task | Marked As | Verified As | Evidence |
| :--- | :--- | :--- | :--- |
| Backend: Data Models | [x] | VERIFIED | `backend/app/models/generation.py` |
| Backend: AI Service Implementation | [x] | VERIFIED | `backend/app/services/cover_letter_generator.py` |
| Backend: API Endpoint | [x] | VERIFIED | `backend/app/routers/generation.py` |
| Frontend: UI Implementation | [x] | VERIFIED | `frontend/components/analysis/CoverLetterGenerator.tsx` |
| **Test: Component test for button and state** | **[x]** | **NOT DONE** | **Missing file in frontend/__tests__** |

**Summary:** 4 of 5 tasks verified. **1 falsely marked complete.**

### Test Coverage and Gaps
- **Backend:** Good coverage. `backend/tests/test_generation.py` covers service and endpoint success/failure cases.
- **Frontend:** **Missing.** No unit/component tests for `CoverLetterGenerator.tsx`.

### Architectural Alignment
- **AI Service Encapsulation:** Follows the pattern of separating AI logic into services (`app/services/cover_letter_generator.py`).
- **Tech Spec Compliance:** Endpoint and data models match the Epic Tech Spec.

### Security Notes
- Endpoint is correctly protected with `Depends(get_current_user)`.

### Action Items

**Code Changes Required:**
- [ ] [High] Create component tests for CoverLetterGenerator.tsx (AC #1) [file: frontend/__tests__/CoverLetterGenerator.test.tsx]
- [ ] [High] Ensure 'Test: Component test for button and state' is actually done before marking complete.

**Advisory Notes:**
- Note: Consider enhancing JSON parsing in `cover_letter_generator.py` to be more robust.

## Test Quality Review (AI)

**Reviewer:** TEA (AI Agent)
**Date:** 2025-12-13
**Outcome:** Approved with Recommendations
**Quality Score:** 80/100 (A - Good)

### Summary
The tests for Story 3.1 are technically sound, ensuring the new features work as expected without flakiness. The backend unit tests correctly cover success and edge cases (JSON parsing). The frontend component test is particularly strong in how it verifies the async loading state using a promise-based mock. The main area for improvement is adding metadata (IDs, Priorities) to align with the project's quality standards.

### Critical Issues (Must Fix)
None detected.

### Recommendations (Should Fix)
- [x] [P1] Add Test IDs and Priorities to `backend/tests/test_generation.py` & `frontend/__tests__/CoverLetterGenerator.test.tsx` (Traceability)
- [ ] [P2] Use BDD (Given-When-Then) structure in comments for better readability (Maintenance)
- [ ] [P3] Consider using factories instead of hardcoded strings for test data (Maintenance)