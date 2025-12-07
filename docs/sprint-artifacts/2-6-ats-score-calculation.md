# Story 2.6: ATS Score Calculation

Status: drafted

## Story

As a user,
I want to see a basic ATS compatibility score,
so that I can understand how well my CV matches the job description.

## Acceptance Criteria

1.  **Given** a CV and job description have been analyzed, **When** the ATS score is displayed, **Then** the system shall calculate and display a basic ATS compatibility score (percentage) based on keyword matching between the CV and the job description.

## Tasks / Subtasks

- [ ] Task 1: AI Service Scoring Logic (AC: 1)
  - [ ] Subtask 1.1: Define scoring criteria prompt (e.g., keyword match weight, skills weight).
  - [ ] Subtask 1.2: Implement scoring function in `app/services/ats_scorer.py` using `pydantic-ai`.
  - [ ] Subtask 1.3: Ensure output is a normalized integer (0-100).
- [ ] Task 2: Backend Integration (AC: 1)
  - [ ] Subtask 2.1: Add ATS scoring call to the existing analysis flow (or create `POST /ai/score-ats`).
  - [ ] Subtask 2.2: Store the score in the `Results` table.
- [ ] Task 3: Frontend Display (AC: 1)
  - [ ] Subtask 3.1: Create `ATSScoreGauge` component (e.g., a radial progress bar).
  - [ ] Subtask 3.2: Integrate score display into the main analysis view.
- [ ] Task 4: Testing (AC: 1)
  - [ ] Subtask 4.1: Unit test scoring logic with perfect match vs. zero match inputs.
  - [ ] Subtask 4.2: Integration test frontend display of score.

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - **Backend:** Python, FastAPI.
  - **Frontend:** Next.js, Tailwind.
- **Source tree components to touch:**
  - Backend: `app/services/ats_scorer.py`.
  - Frontend: `src/components/analysis/ATSScoreGauge.tsx` (new).
- **Testing standards summary:**
  - Verify that identical texts yield 100 (or near 100) and completely unrelated texts yield low scores.

### Learnings from Previous Story

- **From Story 2.5 (Gap Analysis):**
  - The data pipelines are established. We can reuse the parsed CV and analyzed JD data.
  - Storing results in the `Results` table is the consistent pattern.

### Project Structure Notes

- Alignment with unified project structure:
  - Standard.
- Detected conflicts or variances:
  - None.

### References

- [Source: docs/epics.md#Story-2.6-ATS-Score-Calculation]
- [Source: docs/sprint-artifacts/2-5-gap-analysis.md]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#AC-EL2.5]
- [Source: docs/architecture.md]

## Dev Agent Record

### Context Reference

- `docs/sprint-artifacts/2-6-ats-score-calculation.context.xml`

### Agent Model Used

gemini-2.5-flash

### Debug Log References

- None

### Completion Notes List

- Story drafted and validated against Tech Spec.

### File List

- docs/sprint-artifacts/2-6-ats-score-calculation.md

## Change Log

- 2025-12-06: Updated status to ready-for-dev after generating context.
- 2025-12-06: Initial draft created.
- 2025-12-06: Fixed validation issues (Status, AC match, Architecture citation, Dev Agent Record).