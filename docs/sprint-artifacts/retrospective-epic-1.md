# Retrospective - Epic 1: Foundation & User Onboarding

**Date:** 2025-12-13
**Facilitator:** Bob (Scrum Master)
**Participants:** Alice (PO), Charlie (Senior Dev), Dana (QA), Elena (Junior Dev), BIP (Project Lead)

---

## 1. Epic Summary

**Goal:** Establish the project's technical foundation, user authentication, and AI service connectivity.

**Delivery Metrics:**
*   **Stories Completed:** 5/5 (100%)
*   **Velocity:** Foundations established.
*   **Quality:** High (after review iterations).
*   **Blockers:** 1 significant blocker (missing files in 1.2) resolved.

**Business Outcomes:**
*   ✅ User Registration & Login functional (Supabase).
*   ✅ Modern UI Foundation (Next.js 16 + Tailwind v4).
*   ✅ AI Connectivity Verified (Gemini 2.5 Flash POC).

---

## 2. What Went Well (Successes)

*   **Modern Stack Adoption:** Successfully bootstrapped Next.js 16 and Tailwind v4, despite them being cutting-edge versions.
*   **Server Actions:** Adopted Next.js Server Actions for form handling (Registration, Login), simplifying the architecture compared to traditional API routes.
*   **AI Proof-of-Concept:** Story 1.5 proved we can connect to Gemini 2.5 and parse documents using `pydantic-ai`, de-risking Epic 2.
*   **Inline Error Handling:** Shifted from redirect-based errors to inline form errors in Story 1.3, improving UX significantly.

---

## 3. Challenges & Lessons Learned

### 3.1. The "Missing Tests" Pattern
*   **Observation:** Stories 1.3 (Login) and 1.4 (Logout) were initially submitted without unit tests for the logic.
*   **Impact:** Required "Changes Requested" reviews, slowing down velocity.
*   **Root Cause:** focus on implementation over verification during initial draft.
*   **Lesson:** "Done" includes tests. We cannot submit for review without `__tests__` covering the core logic.

### 3.2. Missing Files in Review
*   **Observation:** Story 1.2 was submitted with missing files (metadata said "complete", files didn't exist).
*   **Impact:** Immediate blocker and rejection.
*   **Lesson:** Automated checks or self-review must verify file existence before marking tasks complete.

### 3.3. AI Rate Limits & Attributes
*   **Observation:** During Story 1.5 POC, we hit 429 Rate Limits and had confusion over `pydantic-ai` response attributes (`result.output` vs `result.data`).
*   **Lesson:** Epic 2 must implement robust error handling (retries/backoff) for the AI service.

---

## 4. Action Items

### Process Improvements
1.  **"Tests Required" Gate:**
    *   **Action:** All future stories (starting Epic 2) must include unit tests for logic before being marked "ready for review".
    *   **Owner:** Dev Team
    *   **Check:** SM will reject stories without `__tests__` folder/files.

2.  **File Verification:**
    *   **Action:** Double-check file presence against the "File List" in the story before submission.
    *   **Owner:** Dev Team

### Technical Debt / Refactoring
1.  **Refactor AI POC to Service:**
    *   **Action:** Convert the script from Story 1.5 into a proper FastAPI Service Class / Dependency Injection pattern for Epic 2.
    *   **Owner:** Backend Dev
    *   **Priority:** High (Pre-requisite for Epic 2).

---

## 5. Next Epic Preparation (Epic 2: Core Analysis Engine)

**Focus:** CV Upload, Parsing, Job Analysis, Gap Analysis.

**Readiness Assessment:**
*   **Dependencies:** AI Service POC (Done), Auth (Done).
*   **Risks:**
    *   **Parsing Robustness:** `python-docx` works for simple files, but complex layouts might fail. Need generous testing time.
    *   **AI Cost/Limits:** Heavy analysis might hit quotas.
*   **Critical Path:**
    *   Implement `AIService` class (refactor from POC).
    *   Implement `CVParser` service.

**Commitment:**
The team is ready to start Epic 2. We will prioritize the AI Service refactoring as the first technical task.

---

## 6. Closing Thoughts

**Bob:** "Solid start. We ironed out the workflow wrinkles (tests, file checks). The foundation is strong."
**Alice:** "Love seeing the AI connect. Now let's make it actually analyze something."
**Charlie:** "I'll make sure the AI service is robust for Epic 2."

**Status:** RETROSPECTIVE COMPLETE
