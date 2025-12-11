# Story 2.5: Gap Analysis

Status: review

## Story

As a user,
I want to see a list of key skills and qualifications from the job description that are missing from my CV,
so that I can improve my CV.

## Acceptance Criteria

1.  Given a CV and job description have been analyzed
    When the gap analysis is displayed
    Then the user can see a clear list of missing skills and qualifications.

## Tasks / Subtasks

- [x] Task 1: AI Service Gap Analysis Logic (AC: 1)
  - [x] Subtask 1.1: Define prompt template to compare extracted CV skills vs. JD skills.
  - [x] Subtask 1.2: Create Pydantic model for gap analysis result (e.g., `class GapAnalysisResult(BaseModel): missing_skills: list[str], missing_qualifications: list[str], match_percentage: float`).
  - [x] Subtask 1.3: Implement the comparison function in `app/services/gap_analyzer.py` using the LLM.
- [x] Task 2: Backend Integration (AC: 1)
  - [x] Subtask 2.1: Implement `POST /ai/analyze-gap` endpoint (or service method) in FastAPI.
  - [x] Subtask 2.2: Call the gap analysis logic with parsed CV content and JD analysis results.
  - [x] Subtask 2.3: Store gap analysis results in `Results` table (or JSONB in `CV` or `JobDescription` join table).
- [x] Task 3: Frontend Display (AC: 1)
  - [x] Subtask 3.1: Create `GapAnalysisDisplay` component in React.
  - [x] Subtask 3.2: Fetch gap analysis results from the backend API.
  - [x] Subtask 3.3: Render missing skills/qualifications clearly (e.g., red tags or list).
- [x] Task 4: Testing (AC: 1)
  - [x] Subtask 4.1: Unit test logic with known mismatching text.
  - [x] Subtask 4.2: Integration test the full flow (frontend -> backend -> db).

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - **Backend:** Python, FastAPI, Pydantic AI.
  - **Frontend:** Next.js, Tailwind.
  - **Data:** Gap analysis is derived data; consider if it needs permanent storage or transient calculation. *Decision:* Store it to allow "Saved Applications Dashboard" later (Nice to Have feature, but good practice for MVP persistence).
- **Source tree components to touch:**
  - Backend: `app/services/gap_analyzer.py` (new), `app/models/gap.py` (new), `app/routers/analysis.py` (new).
  - Frontend: `src/components/analysis/GapAnalysisDisplay.tsx` (new).
- **Testing standards summary:**
  - Verify that synonyms are handled gracefully by the LLM (e.g., "React.js" vs "ReactJS" shouldn't be a gap).

### Learnings from Previous Story

- **From Story 2.4 (JD Analysis):**
  - Prompt engineering is key. We likely have structured data for the JD now.
  - We also have the raw text of the CV from Story 2.2.
  - We might need to run a "Skill Extraction" step on the CV *before* comparing, or do it in one shot. *Decision:* One-shot comparison ("Here is CV text, here are JD requirements, what is missing?") is often more robust for LLMs than extracting-then-comparing logic, as it captures nuance better.

### Project Structure Notes

- Alignment with unified project structure:
  - Standard component/service split.
- Detected conflicts or variances:
  - None.

### References

- [Source: docs/epics.md#Story-2.5-Gap-Analysis]
- [Source: docs/sprint-artifacts/2-4-job-description-analysis.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md]

## Dev Agent Record

### Context Reference

- `docs/sprint-artifacts/2-5-gap-analysis.context.xml`

### Agent Model Used

gemini-2.0-flash

### Debug Log References

### Completion Notes List

- Implemented Gap Analysis using Gemini 2.0 Flash via Pydantic AI (`backend/app/services/gap_analyzer.py`).
- Created `GapAnalysisResult` model and `AnalysisResultDB` model for persistence.
- Added `/ai/analyze-gap` endpoint in `backend/app/routers/analysis.py` which saves results to Supabase `results` table.
- Added Unit tests for logic (`backend/tests/test_gap_analyzer.py`) and Integration tests for API (`backend/tests/test_analysis_integration.py`).
- Created Frontend Component `GapAnalysisDisplay.tsx` and Analysis Page `frontend/app/analysis/page.tsx` for user interaction.

### File List

- backend/app/models/gap.py
- backend/app/services/gap_analyzer.py
- backend/tests/test_gap_analyzer.py
- backend/app/models/result.py
- backend/app/routers/analysis.py
- backend/main.py
- backend/tests/test_analysis_integration.py
- frontend/components/analysis/GapAnalysisDisplay.tsx
- frontend/app/analysis/page.tsx

## Change Log

- 2025-12-11: Implemented all tasks and moved to review.
- 2025-12-06: Updated status to ready-for-dev after generating context.
- 2025-12-06: Initial draft created.