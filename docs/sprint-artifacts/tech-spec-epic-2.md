# Epic Technical Specification: AI-Powered Generation & Analysis

Date: Friday, December 5, 2025
Author: BIP
Epic ID: 2
Status: Draft

---

## Overview

This epic, "AI-Powered Generation & Analysis," is central to the AI CV & Job Application Assistant. It focuses on implementing the core AI features that enable the system to act as an intelligent coach for job seekers in the competitive Norwegian market. The goal is to significantly increase users' interview-to-application ratio by leveraging AI to analyze CVs against job descriptions, generate tailored cover letters, identify skill gaps, and provide actionable feedback, thereby helping users navigate ATS and optimize their applications for local nuances.

## Objectives and Scope

**In-Scope:**
*   Analyze pasted job descriptions to identify key skills and qualifications (FR006).
*   Generate tailored cover letters in Norwegian based on user's CV and job description (FR007).
*   Present generated cover letters in an editable text area (FR008).
*   Identify and display missing skills from the user's CV compared to the job description (FR009).
*   Provide a basic ATS compatibility score (FR010).
*   Offer actionable suggestions for improving the ATS score (FR011).
*   Allow copying (FR012) and downloading (FR013) of generated cover letters.

**Out-of-Scope (for this epic):**
*   Advanced CV/Resume editing features.
*   Direct integration with external job boards.

## System Architecture Alignment

This epic aligns with the dedicated **AI Service** component outlined in the system architecture. This specialized microservice, built with **Python and FastAPI**, will encapsulate all AI/ML functionality. It will interface with a third-party Large Language Model (LLM) API (e.g., GPT-4, Gemini) to implement the core AI analysis and generation tasks, including extracting keywords, performing gap analysis, calculating ATS compatibility scores, and generating tailored cover letters. This separation ensures scalability and maintainability, allowing for independent development and deployment of AI features.

## Detailed Design

### Services and Modules

*   **AI Service (Python/FastAPI):**
    *   **Responsibilities:** CV parsing, job description analysis, gap analysis, ATS score calculation, tailored cover letter generation.
    *   **Inputs:** User's CV (text content from parsed .doc/.docx), Job Description (text).
    *   **Outputs:** Generated Cover Letter (text), Missing Skills (list), ATS Score (percentage), Actionable Suggestions (text).
    *   **Owner:** Development Team (Backend/AI Specialists)

### Data Models and Contracts

*   **CV Data:** Text content extracted from `.doc`/`.docx` files.
*   **Job Description Data:** Raw text content provided by the user.
*   **Generated Cover Letter:** Text content.
*   **Missing Skills:** List of strings (e.g., `["Project Management Software", "Agile Methodology"]`).
*   **ATS Score:** Integer/Float (e.g., `75`).
*   **Actionable Suggestions:** Text content.

### APIs and Interfaces

*   **Endpoint:** `/ai/analyze-and-generate` (example)
    *   **Method:** `POST`
    *   **Request Body:**
        ```json
        {
          "cv_content": "string", // Text content of the user's CV
          "job_description": "string", // Text content of the job description
          "user_id": "string" // Optional: for logging/personalization
        }
        ```
    *   **Response Body (200 OK):**
        ```json
        {
          "generated_cover_letter": "string",
          "missing_skills": ["string"],
          "ats_score": "integer",
          "actionable_suggestions": "string"
        }
        ```
    *   **Error Codes:**
        *   `400 Bad Request`: Invalid input (e.g., empty CV/job description).
        *   `500 Internal Server Error`: AI processing failure.

### Workflows and Sequencing

1.  **User uploads CV:** Frontend sends CV file to backend.
2.  **Backend parses CV:** If needed, a dedicated parsing module (potentially within AI service or a separate utility) extracts text from `.doc`/`.docx`.
3.  **User pastes Job Description:** Frontend captures text.
4.  **User clicks "Generate & Analyze":** Frontend sends CV text content and Job Description text to `/ai/analyze-and-generate` endpoint of the AI Service.
5.  **AI Service processes request:**
    *   Extracts keywords/requirements from Job Description.
    *   Analyzes user's CV against Job Description.
    *   Identifies missing skills.
    *   Calculates ATS score.
    *   Generates tailored cover letter.
6.  **AI Service returns response:** Frontend receives generated content, missing skills, ATS score, and suggestions.
7.  **Frontend displays results:** Generated cover letter in editable area, gap analysis, ATS score.
8.  **User interaction:** User can copy/download cover letter.

## Non-Functional Requirements

### Performance

*   **Cover Letter Generation:** The system shall generate a tailored cover letter in under 120 seconds (NFR003). This applies directly to the AI Service's core function within this epic.

### Security

*   All user data, including CVs and personal information processed by the AI Service, must be encrypted at rest and in transit (NFR001, Architecture: Data Encryption).
*   The platform must comply with GDPR and Norwegian privacy regulations, particularly regarding the handling of sensitive personal data within the AI processing pipeline (NFR002, Architecture: Compliance).
*   API keys for external LLMs and other credentials used by the AI Service must be stored securely using services like AWS Secrets Manager or environment variables, and not hardcoded (Architecture: Secrets Management).

### Reliability/Availability

*   **Availability:** The platform, including the AI Service, shall be available 99.5% of the time (NFR004).
*   **Resilience:** The AI Service should be designed to be resilient to failures of external LLM APIs, with appropriate error handling and retry mechanisms.

### Observability

*   The AI Service should implement comprehensive logging for requests, responses, and internal processing steps to facilitate debugging and monitoring.
*   Key metrics (e.g., response times, error rates, number of successful generations) should be exposed for monitoring the performance and health of the AI Service.
*   Consider implementing tracing for requests that flow through the AI Service to aid in troubleshooting complex issues.

## Dependencies and Integrations

*   **Primary Dependencies (AI Service):**
    *   **Python:** Programming language for the AI Service.
    *   **FastAPI:** Web framework for building the AI Service API.
    *   **python-docx:** Library for parsing `.doc` and `.docx` files for CV content extraction.
*   **External Integrations:**
    *   **Large Language Model (LLM) API:** Integration with a third-party LLM provider (e.g., GPT-4, Gemini) for AI analysis, gap identification, ATS scoring, and cover letter generation. API keys and authentication will be required.

## Acceptance Criteria (Authoritative)

1.  **AC-EL2.1 (FR006):** Given a pasted job description, the system shall accurately identify and extract key skills, qualifications, and keywords.
2.  **AC-EL2.2 (FR007):** Given a user's CV content and a job description, the system shall generate a tailored cover letter in Norwegian (Bokmål/Nynorsk) that aligns with both inputs.
3.  **AC-EL2.3 (FR008):** The generated cover letter shall be displayed to the user in an editable text area within the user interface.
4.  **AC-EL2.4 (FR009):** The system shall identify and display a list of key skills and qualifications present in the job description but missing from the user's CV.
5.  **AC-EL2.5 (FR010):** The system shall calculate and display a basic ATS compatibility score (percentage) based on keyword matching between the CV and the job description.
6.  **AC-EL2.6 (FR011):** The system shall provide actionable suggestions to the user for improving their displayed ATS score.
7.  **AC-EL2.7 (FR012):** The user shall be able to copy the generated cover letter text to their clipboard.
8.  **AC-EL2.8 (FR013):** The user shall be able to download the generated cover letter as a text file.

## Traceability Mapping

| AC ID   | Spec Section(s)            | Component(s)/API(s)                  | Test Idea                                                                                                                                                                                                                                           |
| :------ | :------------------------- | :----------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC-EL2.1 | Detailed Design            | AI Service (`/ai/analyze-and-generate`) | Provide a job description; verify extracted skills match expected output.                                                                                                                                                               |
| AC-EL2.2 | Detailed Design            | AI Service (`/ai/analyze-and-generate`) | Provide a sample CV and job description; verify generated cover letter content and language are appropriate and tailored.                                                                                                              |
| AC-EL2.3 | Detailed Design            | Frontend UI                          | Generate a cover letter; verify it appears in an editable text area.                                                                                                                                                                  |
| AC-EL2.4 | Detailed Design            | AI Service (`/ai/analyze-and-generate`), Frontend UI | Provide CV/job description with known skill gaps; verify missing skills are accurately identified and displayed.                                                                                                                   |
| AC-EL2.5 | Detailed Design            | AI Service (`/ai/analyze-and-generate`), Frontend UI | Provide CV/job description pairs with varying keyword matches; verify ATS score is calculated and displayed correctly.                                                                                                                |
| AC-EL2.6 | Detailed Design            | AI Service (`/ai/analyze-and-generate`), Frontend UI | Generate low ATS score; verify relevant actionable suggestions are provided and displayed.                                                                                                                                              |
| AC-EL2.7 | Detailed Design, APIs/Interfaces | Frontend UI                          | Generate a cover letter; click copy button; verify text is copied to clipboard.                                                                                                                                                       |
| AC-EL2.8 | Detailed Design, APIs/Interfaces | Frontend UI                          | Generate a cover letter; click download button; verify a text file containing the cover letter is downloaded.                                                                                                                           |

## Risks, Assumptions, Open Questions

*   **Risk:** Quality of LLM output. The accuracy and relevance of generated cover letters, identified missing skills, and ATS score are highly dependent on the chosen LLM's capabilities.
    *   **Mitigation:** Implement robust evaluation metrics for LLM output (human review, A/B testing). Allow for easy switching between LLM providers if one performs poorly.
*   **Risk:** Cost of LLM usage. Frequent API calls to a third-party LLM can become expensive, especially with high user volume.
    *   **Mitigation:** Implement caching for common prompts/responses. Explore cost-effective LLM models or fine-tuning open-source models. Educate users on optimal usage patterns.
*   **Assumption:** Availability and reliability of third-party LLM API.
    *   **Next Step:** Monitor LLM API status and build in retry mechanisms with exponential backoff.
*   **Question:** How will the system handle parsing of highly-formatted or image-based CVs beyond simple `.doc`/`.docx` text extraction?
    *   **Next Step:** Research advanced CV parsing libraries or consider integrating OCR for image-based content if this becomes a user requirement.
*   **Question:** What are the legal implications of using AI to generate application materials, particularly regarding potential biases in LLM output?
    *   **Next Step:** Conduct thorough bias testing on LLM output and implement safeguards to promote fairness and ethical AI usage. Consult legal counsel regarding AI-generated content disclosures.

## Test Strategy Summary

*   **Unit Tests:** Develop comprehensive unit tests for the AI Service components (e.g., CV text extraction, job description keyword parsing, API endpoint logic). Use frameworks like `pytest` for Python.
*   **Integration Tests:** Test the integration between the Frontend, Backend API, and AI Service, particularly the `analyze-and-generate` endpoint. Ensure data is correctly transmitted and received across service boundaries.
*   **LLM Output Validation:** Implement a strategy to validate the quality, relevance, and accuracy of LLM-generated content. This may involve:
    *   **Automated Content Checks:** Basic checks for length, presence of keywords, and grammatical correctness.
    *   **Human-in-the-Loop Review:** Manual review of a subset of generated cover letters and gap analyses to ensure quality.
    *   **Golden Set Testing:** Maintain a set of predefined CV/job description pairs with expected AI outputs, and regularly run tests against these to detect regressions or changes in LLM behavior.
*   **Performance Testing:** Conduct load testing on the AI Service to ensure it can handle expected concurrency and meet the 120-second cover letter generation SLA.
*   **Security Testing:** Perform penetration testing and vulnerability assessments on the AI Service API, paying close attention to data encryption, access controls, and secure handling of LLM API keys.
*   **UI Acceptance Tests:** Use frameworks like `Cypress` or `Playwright` to test the frontend display of generated content, gap analysis, ATS score, and the functionality of copy/download buttons.

## Post-Review Follow-ups

*   Move API base URL to NEXT_PUBLIC_API_URL environment variable in frontend (Ref: Story 2.5).
