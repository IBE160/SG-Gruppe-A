# Story 3.1: Cover Letter Generation

Status: ready-for-dev

## Story

As a **user**,
I want to **generate a tailored cover letter in Norwegian based on my CV and the job description**,
so that **I can have a strong starting point for my application**.

## Acceptance Criteria

1.  **Given** a CV and job description have been analyzed, **when** the user clicks "Generate Cover Letter", **then** a cover letter is generated in Norwegian (Bokmål/Nynorsk). [Source: docs/sprint-artifacts/tech-spec-epic-3.md#Acceptance Criteria (Authoritative)]

## Tasks / Subtasks

- [ ] **Backend: Data Models** (AC: 1)
  - [ ] Define `CoverLetterGenerationRequest` (cv_text, job_description_text)
  - [ ] Define `CoverLetterGenerationResponse` (cover_letter)
  - [ ] Implement validation (Pydantic models)
- [ ] **Backend: AI Service Implementation** (AC: 1)
  - [ ] Implement `generate_cover_letter(cv_text, jd_text)` function
  - [ ] Construct system prompt for Norwegian cover letter generation (Tone: Professional, tailored)
  - [ ] Integrate with LLM Client (`pydantic-ai` or `google-generativeai`)
  - [ ] Handle LLM API errors and timeouts
- [ ] **Backend: API Endpoint** (AC: 1)
  - [ ] Create `POST /api/v1/generation/cover-letter`
  - [ ] Connect endpoint to `generate_cover_letter` service
  - [ ] Ensure authentication (JWT) is required
  - [ ] Test: Unit tests for endpoint and service logic
- [ ] **Frontend: UI Implementation** (AC: 1)
  - [ ] Create/Update "Generate Cover Letter" button component
  - [ ] Implement API service call in frontend `api/` layer
  - [ ] Connect button click to API call
  - [ ] Implement loading state (spinner/progress bar) for < 120s wait
  - [ ] Handle and display error messages
  - [ ] Test: Component test for button and state

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

### File List
