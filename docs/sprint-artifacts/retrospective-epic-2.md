# Retrospective - Epic 2: Core Analysis Engine

**Date:** 2025-12-13
**Facilitator:** Bob (Scrum Master)
**Participants:** Alice (PO), Charlie (Senior Dev), Dana (QA), Elena (Junior Dev), BIP (Project Lead)

---

## 1. Epic Summary

**Goal:** Implement the core value proposition: CV upload, parsing, job description analysis, gap analysis, and ATS scoring.

**Delivery Metrics:**
*   **Stories Completed:** 7/7 (100%)
*   **Velocity:** High. Delivered complex AI workflows rapidly.
*   **Quality:** Good. Security issues caught in review (Story 2.1) were fixed.
*   **Blockers:** None significant.

**Business Outcomes:**
*   ✅ **Core Engine Live:** Users can upload CVs and get AI-driven analysis.
*   ✅ **Value Delivered:** Gap analysis and ATS scoring are providing real insights (verified in 2.5/2.6).
*   ✅ **Secure Uploads:** Fixed initial security gaps in file handling.

---

## 2. What Went Well (Successes)

*   **Pydantic AI Adoption:** Using `pydantic-ai` for structured output (Stories 2.4, 2.5, 2.6) worked perfectly. It enforced type safety on LLM responses, preventing "hallucination formatting" errors.
*   **Parallel Execution:** Story 2.6 utilized `asyncio.gather` to run Scoring and Gap Analysis in parallel, optimizing performance.
*   **Component Reuse:** The Frontend components (`GapAnalysisDisplay`, `SuggestionsList`) are modular and clean.
*   **Testing Discipline:** The "Tests Required" gate from Epic 1 Retro was respected. Every story had unit and integration tests. Story 2.1's catch of insecure upload proved the value of review.

---

## 3. Challenges & Lessons Learned

### 3.1. Security Oversight in Draft
*   **Observation:** Story 2.1 (CV Upload) was initially submitted without authentication on the endpoint or `user_id` tracking.
*   **Impact:** "Changes Requested" review.
*   **Root Cause:** Rushing to "make it work" before "making it secure".
*   **Lesson:** Security (Auth/Authz) must be part of the *first* implementation pass, not a cleanup task.

### 3.2. Deferred Persistence
*   **Observation:** In Story 2.4 (JD Analysis), we deferred persistence of analysis results to Story 2.5.
*   **Impact:** It worked out, but created a temporary state where an endpoint existed but didn't "save" fully.
*   **Lesson:** Be careful with "stateless" intermediate steps. Ideally, every story should result in a complete state change.

### 3.3. UX Polish
*   **Observation:** We used `window.alert` in Story 2.3.
*   **Lesson:** While acceptable for MVP backend focus, we need to standardize on a Toast library (like `sonner`) for Epic 4 (UI Polish).

---

## 4. Action Items

### Process Improvements
1.  **Security-First Implementation:**
    *   **Action:** All new endpoints must have `Depends(get_current_user)` or equivalent in the *first draft*.
    *   **Owner:** Dev Team

### Technical Debt / Refactoring
1.  **UI Feedback Standardization:**
    *   **Action:** Replace all `window.alert` calls with a Toast component during Epic 4.
    *   **Owner:** Frontend Dev

2.  **Environment Variables:**
    *   **Action:** Move hardcoded frontend API URLs (`http://127.0.0.1:8000`) to `NEXT_PUBLIC_API_URL`.
    *   **Owner:** Frontend Dev

---

## 5. Next Epic Preparation (Epic 3: AI-Powered Content Generation)

**Focus:** Generating Cover Letters, Displaying, Copying/Downloading.

**Readiness Assessment:**
*   **Dependencies:** Core Analysis (Done) - we have the Gaps and CV data needed to generate the letter.
*   **Risks:**
    *   **LLM Latency:** Generating a full letter might take time. UI needs good loading states.
    *   **Quality:** The letter needs to sound human. Prompt engineering is key.
*   **Critical Path:**
    *   Design the prompt for Story 3.1 carefully to use the output from Epic 2 (Gaps/Skills).

**Commitment:**
The team is ready for Epic 3. The foundation from Epic 2 (structured AI responses) is exactly what we need for generating high-quality letters.

---

## 6. Closing Thoughts

**Bob:** "Excellent recovery on the security finding in 2.1. That's the system working."
**Charlie:** "Pydantic AI is a lifesaver. Handling those JSON responses manually would have been a nightmare."
**Alice:** "The Gap Analysis output is actually useful. I tried it on my own CV!"

**Status:** RETROSPECTIVE COMPLETE
