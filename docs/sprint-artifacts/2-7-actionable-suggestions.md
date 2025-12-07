# Story 2.7: Actionable Suggestions

**Epic:** 2: Core Analysis Engine
**Status:** drafted
**Effort:** S

## User Story
As a user, I want to receive actionable suggestions for improving my ATS score, so that I can make my CV more competitive.

## Acceptance Criteria
1.  **Given** an ATS score has been calculated, **When** the suggestions are displayed, **Then** the system shall provide actionable suggestions to the user for improving their displayed ATS score.

## Tasks / Subtasks

- [ ] Task 1: AI Service Suggestion Generation (AC: 1)
  - [ ] Subtask 1.1: Design AI prompt to generate "actionable suggestions" based on identified gaps and the job description.
  - [ ] Subtask 1.2: Implement suggestion logic in `app/services/ats_scorer.py` (or similar service module) ensuring response aligns with the `Actionable Suggestions` data contract (Text content).
  - [ ] Subtask 1.3: Update the `/ai/analyze-and-generate` endpoint response model to include `actionable_suggestions`.
- [ ] Task 2: Backend Integration (AC: 1)
  - [ ] Subtask 2.1: Ensure the backend handles the `actionable_suggestions` field from the AI service response.
  - [ ] Subtask 2.2: Store the suggestions in the `Results` table (as `actionable_suggestions`).
- [ ] Task 3: Frontend Display (AC: 1)
  - [ ] Subtask 3.1: Create a display component (e.g., `SuggestionsList.tsx` or similar) to present the suggestions clearly (e.g., bulleted list).
  - [ ] Subtask 3.2: Integrate this component into the results view, adjacent to the ATS score and Gap Analysis.
- [ ] Task 4: Testing (AC: 1)
  - [ ] Subtask 4.1: Unit test the AI prompt/logic to ensure it produces relevant suggestions for test inputs.
  - [ ] Subtask 4.2: Integration test to verify suggestions flow from AI Service -> Backend -> Frontend.

## Dev Notes

### Architecture patterns and constraints
- **AI Service:** Follow the pattern of `app/services` modules. Ensure the prompt context includes both the CV gaps and the JD to make suggestions specific.
- **Backend:** Python/FastAPI. Update the `Results` model if necessary to store this text field.
- **Frontend:** Next.js/Tailwind. Use consistent styling with the existing Gap Analysis display.

### Learnings from Previous Story
- **From Story 2.6 (ATS Score Calculation):**
  - We are building on the `analyze-and-generate` flow. The data (gaps, score) is already present; this is an additional output from the analysis.
  - [Source: docs/sprint-artifacts/2-6-ats-score-calculation.md]

### Project Structure Notes
- **Alignment:** Standard usage of `app/services` (AI), `models` (Backend), and `components` (Frontend).
- **Variances:** None expected.

### References
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#AC-EL2.6] (Tech Spec AC)
- [Source: docs/epics.md#Story-2.7-Actionable-Suggestions] (Epic Story)
- [Source: docs/architecture.md#3.3-AI-Service] (Architecture - AI Service responsibilities)

## Dev Agent Record

### Context Reference
- `docs/sprint-artifacts/2-7-actionable-suggestions.context.xml`

### Agent Model Used
- gemini-2.5-flash

### Debug Log References
- (None)

### Completion Notes List
- (None)

### File List
- (None)

## Change Log
- 2025-12-06: Initial draft created and revised based on validation feedback.