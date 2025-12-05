# Epic Technical Specification: {{epic_title}}

Date: {{date}}
Author: {{user_name}}
Epic ID: {{epic_id}}
Status: Draft

---

## Overview

This epic focuses on the core AI-powered content generation capabilities of the application. It covers the functionality required to take the user's analyzed CV and a target job description and produce a tailored, high-quality cover letter in Norwegian. This is a critical part of the user journey, delivering the primary value proposition of the product.

## Objectives and Scope

**In Scope:**
*   Generating a tailored cover letter in Norwegian (Bokmål/Nynorsk) based on the user's CV and the job description.
*   Displaying the generated cover letter in an editable text area for the user to review and modify.
*   Allowing the user to copy the full text of the generated cover letter to their clipboard.
*   Allowing the user to download the generated cover letter as a `.txt` file.

**Out of Scope:**
*   Advanced text editing features beyond a simple textarea.
*   Generating cover letters in languages other than Norwegian.
*   Saving multiple versions of a cover letter.

## System Architecture Alignment

This epic will be primarily implemented within the **AI Service**, as defined in the Architecture Specification. The functionality relies on the Python/FastAPI service to interface with a third-party LLM for the heavy lifting of text generation.

- **Frontend Application:** Will provide the UI for the user to trigger the generation and to display, edit, copy, and download the resulting cover letter. It will communicate with the Backend API.
- **Backend API:** Will receive the request from the frontend and proxy it to the AI Service. It will handle the orchestration between the user-facing application and the internal AI capabilities.
- **AI Service:** This is the core component for this epic. It will receive the CV content and job description, format a prompt for the LLM, call the LLM's API, and return the generated cover letter to the Backend API.


## Detailed Design

### Services and Modules

| Service/Module | Responsibilities | Inputs | Outputs | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend Application** | - Render UI for cover letter generation.<br>- Capture user action (click "Generate").<br>- Display generated letter in an editable textarea.<br>- Handle copy and download actions. | User interactions | API requests to Backend | Frontend Team |
| **Backend API** | - Expose a secure endpoint for cover letter generation.<br>- Orchestrate the request to the AI Service.<br>- Handle authentication and authorization. | Request from Frontend | Generated cover letter (JSON) | Backend Team |
| **AI Service** | - Receive analysis data from the Backend API.<br>- Construct a detailed prompt for the LLM.<br>- Call the external LLM API.<br>- Return the generated text. | CV & Job Description text | Generated cover letter (text) | AI Team |

### Data Models and Contracts

The data contracts for this epic are straightforward, focusing on the text being processed and generated.

**Cover Letter Generation Request (Frontend -> Backend):**
```json
{
  "cv_text": "...",
  "job_description_text": "..."
}
```

**Cover Letter Generation Response (Backend -> Frontend):**
```json
{
  "cover_letter": "..."
}
```

### APIs and Interfaces

**Frontend -> Backend API:**
*   **Endpoint:** `POST /api/v1/generation/cover-letter`
*   **Description:** Initiates the cover letter generation process.
*   **Request Body:** `CoverLetterGenerationRequest`
*   **Response Body:** `CoverLetterGenerationResponse`
*   **Error Codes:**
    *   `401 Unauthorized`: If the user is not authenticated.
    *   `500 Internal Server Error`: If the generation process fails downstream.

**Backend API -> AI Service:**
*   **Endpoint:** `POST /generate/cover-letter`
*   **Description:** Internal endpoint to request cover letter generation from the AI service.
*   **Request Body:** Same as the request to the Backend API.
*   **Response Body:** Plain text response with the generated cover letter.

### Workflows and Sequencing

1.  **User Action:** The user, having already provided a CV and job description for analysis, clicks the "Generate Cover Letter" button in the **Frontend Application**.
2.  **Frontend Request:** The frontend sends a `POST` request to the `/api/v1/generation/cover-letter` endpoint on the **Backend API**, including the CV and job description text in the body.
3.  **Backend Orchestration:** The **Backend API** authenticates the user, validates the request, and then makes a `POST` request to the `/generate/cover-letter` endpoint of the **AI Service**.
4.  **AI Service Processing:** The **AI Service** receives the texts. It constructs a carefully-worded prompt for the configured LLM, instructing it to generate a cover letter in Norwegian that is tailored to the job description based on the strengths in the CV.
5.  **LLM Generation:** The **AI Service** sends the prompt to the external LLM's API and awaits the response.
6.  **Response Handling:** The generated text is received by the **AI Service**. It may perform light sanitization if necessary.
7.  **Return to Frontend:** The text is returned up the chain: AI Service -> Backend API -> Frontend Application.
8.  **Display to User:** The **Frontend Application** receives the JSON response and populates the `<textarea>` with the `cover_letter` content, making it visible and editable for the user.


## Non-Functional Requirements

### Performance

*   **NFR003:** The end-to-end time for generating a cover letter (from user click to text display) shall be under **120 seconds**. This is highly dependent on the external LLM's response time. The internal processing time of the Backend and AI Service should be less than 500ms.

### Security

*   **NFR001:** All data, specifically the CV and job description text, must be transmitted over HTTPS (encrypted in transit) between all services (Frontend, Backend, AI Service, and external LLM).
*   **NFR002:** The system must comply with GDPR. No user-identifiable data from the CV or job description should be logged or stored unnecessarily.
*   API endpoints must be protected, requiring a valid JWT for access.

### Reliability/Availability

*   **NFR004:** The platform's services (Frontend, Backend API) shall maintain **99.5% availability**.
*   The system must handle failures of the external LLM API gracefully. If the LLM is down or returns an error, the user should be shown a friendly error message and be able to retry.

### Observability

*   **Logging:** The AI Service should log the start and end of each generation request, including the time taken for the external LLM call. No PII should be logged.
*   **Metrics:** Key metrics to track include:
    *   `generation_requests_total`: A counter for every time a generation is requested.
    *   `generation_duration_seconds`: A histogram of the end-to-end generation time.
    *   `llm_api_errors_total`: A counter for errors from the external LLM API.
*   **Tracing:** Distributed tracing should be implemented to track a single request from the Frontend through the Backend and AI Service to identify bottlenecks.


## Dependencies and Integrations

### Internal Dependencies
*   **Backend API:** The frontend will depend on the Backend API for all data and functionality.
*   **AI Service:** The Backend API will depend on the AI Service for the generation logic.

### External Services
*   **LLM Provider (e.g., OpenAI, Google AI):** The AI Service will make API calls to an external Large Language Model. This is the most critical external dependency for this epic.

### Libraries & Frameworks

**Frontend Application (Next.js):**
*   `next`: Core framework for React.
*   `react`, `react-dom`: UI library.
*   `tailwindcss`: CSS styling.
*   `shadcn/ui`: Component library.
    *   `class-variance-authority`, `clsx`, `tailwind-merge`: Utilities for styling.
*   `lucide-react`: Icon library for `shadcn/ui`.

**Backend API (Node.js/Express):**
*   `express`: Web server framework.
*   `jsonwebtoken`: For handling JWT authentication.
*   `pg`: PostgreSQL client.
*   `axios` or `node-fetch`: For making HTTP requests to the AI Service.

**AI Service (Python/FastAPI):**
*   `fastapi`: Web framework for the service.
*   `uvicorn`: ASGI server to run FastAPI.
*   `openai` or `google-generativeai`: Client library for the chosen LLM.
*   `pydantic`: For data validation.


## Acceptance Criteria (Authoritative)

1.  **Given** a CV and job description have been analyzed, **when** the user clicks "Generate Cover Letter", **then** a cover letter is generated in Norwegian (Bokmål/Nynorsk). (from Story 3.1)
2.  **Given** a cover letter has been generated, **when** it is displayed to the user, **then** the user sees the full text of the cover letter in a text area where they can make changes. (from Story 3.2)
3.  **Given** a cover letter is displayed, **when** the user clicks the "Copy" button, **then** the text of the cover letter is copied to their clipboard. (from Story 3.3)
4.  **Given** a cover letter is displayed, **when** the user clicks the "Download" button, **then** a `.txt` file containing the cover letter is downloaded to their device. (from Story 3.4)

## Traceability Mapping

| AC # | Spec Section(s) | Component(s) / API(s) | Test Idea |
| :--- | :--- | :--- | :--- |
| 1 | Detailed Design, NFRs | - Frontend (UI Button)<br>- Backend (`POST /api/v1/generation/cover-letter`)<br>- AI Service (`/generate/cover-letter`)<br>- External LLM API | **Integration Test:** Simulate a click, mock the LLM response, and verify the generated text is passed back to the frontend. |
| 2 | Detailed Design | - Frontend (UI Textarea) | **UI Test:** After generation, assert that the textarea component is populated with the expected text and is editable. |
| 3 | Detailed Design | - Frontend (UI Button, Clipboard API) | **UI Test:** Click the "Copy" button and assert that the clipboard content matches the text in the textarea. |
| 4 | Detailed Design | - Frontend (UI Button, Blob creation) | **UI Test:** Click the "Download" button and verify that a file download is initiated with the correct content and `.txt` extension. |


## Risks, Assumptions, Open Questions

*   **Risk:** The quality of the generated Norwegian cover letter from the LLM may be poor, contain factual errors, or sound unnatural. **Mitigation:** Extensive testing with various prompts and models. Allow users to edit the output.
*   **Risk:** The latency of the external LLM API may exceed the 120-second NFR, leading to a poor user experience. **Mitigation:** Choose a performant model and region. Implement clear loading states in the UI.
*   **Risk:** The cost of the LLM API calls could be higher than anticipated, impacting operational budget. **Mitigation:** Implement rate limiting or quotas. Monitor usage closely.
*   **Assumption:** A suitable third-party LLM with a robust API and strong Norwegian language capabilities is available and affordable.
*   **Assumption:** The data passed to the LLM (CV and job description) is handled securely and in compliance with the provider's terms of service and GDPR.
*   **Question:** Which specific LLM and model will be used for the generation (e.g., GPT-4, Gemini Pro)?
*   **Question:** What is the prompt engineering strategy to ensure the tone and content are consistently high quality?

## Test Strategy Summary

*   **Unit Testing:**
    *   **Frontend:** Test individual React components for the generation view (buttons, textarea) in isolation.
    *   **Backend:** Test the `/api/v1/generation/cover-letter` endpoint logic, including authentication and request validation, by mocking the AI service.
    *   **AI Service:** Test the prompt construction logic and the client used to call the external LLM.
*   **Integration Testing:**
    *   Test the full flow from the Backend API to the AI Service, mocking the external LLM API to ensure the services communicate correctly.
*   **End-to-End Testing:**
    *   Use a framework like Cypress or Playwright to simulate the full user journey: logging in, providing input, clicking "Generate", and verifying the output is displayed.
*   **Manual & Qualitative Testing:**
    *   Crucial for this epic. A human must review a wide variety of generated cover letters to assess their quality, tone, and relevance. This should be done with sample CVs and real-world job ads.

