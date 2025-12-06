# Story 2.5: Gap Analysis

Status: ready-for-dev

## Story

As a user,
I want to see a list of key skills and qualifications from the job description that are missing from my CV,
so that I can improve my CV.

## Acceptance Criteria

1.  Given a CV and job description have been analyzed
    When the gap analysis is displayed
    Then the user can see a clear list of missing skills and qualifications.

## Tasks / Subtasks

- [ ] Task 1: AI Service Gap Analysis Logic (AC: 1)
  - [ ] Subtask 1.1: Define prompt template to compare extracted CV skills vs. JD skills.
  - [ ] Subtask 1.2: Create Pydantic model for gap analysis result (e.g., `class GapAnalysisResult(BaseModel): missing_skills: list[str], missing_qualifications: list[str], match_percentage: float`).
  - [ ] Subtask 1.3: Implement the comparison function in `app/services/gap_analyzer.py` using the LLM.
- [ ] Task 2: Backend Integration (AC: 1)
  - [ ] Subtask 2.1: Implement `POST /ai/analyze-gap` endpoint in FastAPI service.
  - [ ] Subtask 2.2: Update Node.js backend to orchestrate this: Call Python API with parsed CV content and JD analysis results.
  - [ ] Subtask 2.3: Store gap analysis results in `Results` table (or JSONB in `CV` or `JobDescription` join table).
- [ ] Task 3: Frontend Display (AC: 1)
  - [ ] Subtask 3.1: Create `GapAnalysisDisplay` component in React.
  - [ ] Subtask 3.2: Fetch gap analysis results from Node.js API.
  - [ ] Subtask 3.3: Render missing skills/qualifications clearly (e.g., red tags or list).
- [ ] Task 4: Testing (AC: 1)
  - [ ] Subtask 4.1: Unit test Python logic with known mismatching text.
  - [ ] Subtask 4.2: Integration test the full flow (frontend -> node -> python -> db).

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - **AI Service:** Python, FastAPI, Pydantic AI.
  - **Backend:** Node.js.
  - **Frontend:** Next.js, Tailwind.
  - **Data:** Gap analysis is derived data; consider if it needs permanent storage or transient calculation. *Decision:* Store it to allow "Saved Applications Dashboard" later (Nice to Have feature, but good practice for MVP persistence).
- **Source tree components to touch:**
  - AI: `app/services/gap_analyzer.py`, `app/models/gap.py`.
  - Backend: `src/controllers/analysisController.ts` (new).
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

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- 2025-12-06: Updated status to ready-for-dev after generating context.
- 2025-12-06: Initial draft created.
