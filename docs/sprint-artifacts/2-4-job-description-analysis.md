# Story 2.4: Job Description Analysis

Status: ready-for-dev

## Story

As a developer,
I want to analyze the job description to identify key skills, qualifications, and keywords,
so that I can compare them with the user's CV.

## Acceptance Criteria

1.  Given a job description has been submitted
    When the analysis process is triggered
    Then a list of key skills, qualifications, and keywords is extracted.

## Tasks / Subtasks

- [ ] Task 1: AI Service JD Analysis Logic (AC: 1)
  - [ ] Subtask 1.1: Define the prompt template for the LLM to extract skills, qualifications, and keywords from a job description.
  - [ ] Subtask 1.2: Create a Pydantic model to structure the LLM output (e.g., `class JobAnalysisResult(BaseModel): skills: list[str], qualifications: list[str], keywords: list[str]`).
  - [ ] Subtask 1.3: Implement the analysis function in the Python AI Service using `pydantic-ai` and the Gemini model.
- [ ] Task 2: Integration with JD Input Flow (AC: 1)
  - [ ] Subtask 2.1: Implement `POST /ai/analyze-job-description` endpoint in the FastAPI service.
  - [ ] Subtask 2.2: Update the Node.js backend to call this endpoint (likely triggered after Story 2.3's save, or on a separate "Analyze" button click). *Decision:* Trigger on user request ("Analyze" button) to allow them to review/edit JD first.
  - [ ] Subtask 2.3: Store the analysis results (skills, keywords) in the `JobDescription` table (add JSONB column `analysis_results`) or a related table.
- [ ] Task 3: Testing (AC: 1)
  - [ ] Subtask 3.1: Unit test the prompt and Pydantic model with sample JDs.
  - [ ] Subtask 3.2: Integration test the API call from Node.js to Python.
  - [ ] Subtask 3.3: Verify the extracted data quality manually with a few real-world examples.

## Dev Notes

- **Relevant architecture patterns and constraints:**
  - **AI Service:** Python, FastAPI, Pydantic AI, Gemini 2.5.
  - **Backend:** Node.js (orchestrator).
  - **Database:** PostgreSQL.
  - **Communication:** REST API.
- **Source tree components to touch:**
  - AI Service: `app/services/jd_analyzer.py` (new), `app/models/jd.py` (new schema).
  - Backend: `src/services/aiService.ts` (update), `src/controllers/jobController.ts` (update).
  - Database: Migration to add `analysis_results` to `job_descriptions`.
- **Testing standards summary:**
  - Focus on the structure of the returned JSON. The LLM might hallucinate, so validation of the *format* is more critical than 100% semantic accuracy for unit tests.

### Learnings from Previous Story

- **From Story 2.3 (JD Input):**
  - Story 2.3 handled the raw input. This story (2.4) adds intelligence to it.
  - As with CV parsing (Story 2.2), the pattern is: Node receives input -> Saves to DB -> Calls Python AI Service -> AI Service processes -> Returns result -> Node saves result.
  - *Refinement:* The prompt engineering here is critical. We need distinct lists for "skills" (hard skills like Python, React), "qualifications" (degrees, years of exp), and "keywords" (soft skills, domain terms).

### Project Structure Notes

- Alignment with unified project structure:
  - Python AI service structure: `app/services`, `app/routers`, `app/models`.
  - Node Backend structure: `src/services`, `src/controllers`.
- Detected conflicts or variances:
  - None.

### References

- [Source: docs/epics.md#Story-2.4-Job-Description-Analysis]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#AI-Service]
- [Source: docs/sprint-artifacts/2-3-job-description-input.md]

## Dev Agent Record

### Context Reference

- `docs/sprint-artifacts/2-4-job-description-analysis.context.xml`

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- 2025-12-06: Updated status to ready-for-dev after generating context.
- 2025-12-06: Initial draft created.
