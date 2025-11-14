# ibe160 - Epic Breakdown

**Author:** BIP
**Date:** 2025-11-04
**Project Level:** 3

---

## Overview

This document provides the detailed epic breakdown for ibe160, expanding on the high-level epic list in the [PRD](./PRD.md).

Each epic includes:

- Expanded goal and value proposition
- Complete story breakdown with user stories
- Acceptance criteria for each story
- Story sequencing and dependencies

**Epic Sequencing Principles:**

- Epic 1 establishes foundational infrastructure and initial functionality
- Subsequent epics build progressively, each delivering significant end-to-end value
- Stories within epics are vertically sliced and sequentially ordered
- No forward dependencies - each story builds only on previous work

---

### Epic 1: Foundation & Core Application

**Expanded Goal:** This epic focuses on establishing the complete technical infrastructure for the project. It includes setting up the frontend and backend applications, creating the basic user interface structure, and implementing the initial, non-AI functionality for uploading a CV and submitting a job description for analysis. By the end of this epic, the core data pipeline will be in place, ready for the AI components in Epic 2.

---

**Story 1.1: Project Scaffolding & Deployment**

As a developer,
I want to set up the initial frontend and backend project structures with automated deployment,
So that we have a stable foundation for building and testing features.

**Related FRs:** FR014

**Acceptance Criteria:**
1.  A Next.js frontend application is initialized and linked to a new Git repository.
2.  A FastAPI backend application is initialized in the same repository.
3.  A basic "Hello World" page on the frontend is successfully deployed to Vercel.
4.  A basic health check endpoint on the backend is successfully deployed to Render.
5.  The repository contains a clear README with setup instructions.
6.  The deployment setup is configured for high availability to meet the 99.5% uptime requirement (NFR004).

**Prerequisites:** None

---

**Story 1.2: Implement Basic UI Layout**

As a user,
I want to see a clean, professional, and consistent layout with a header, footer, and main content area,
So that I can easily navigate the application and understand its structure.

**Related FRs:** FR014

**Acceptance Criteria:**
1.  A main layout component is created and applied to all pages.
2.  A header is present containing the application name/logo.
3.  A footer is present with basic links (e.g., "About," "Contact").
4.  The layout is responsive and functions correctly on desktop and mobile screen sizes.

**Prerequisites:** Story 1.1

---

**Story 1.3: CV Upload Interface**

As a user,
I want a simple interface to upload my CV document,
So that the system can begin to analyze it.

**Related FRs:** FR003

**Acceptance Criteria:**
1.  The main workspace displays a clearly marked "Upload CV" button or drag-and-drop area.
2.  Clicking the upload area opens the system's file selection dialog.
3.  The interface restricts file selection to `.doc` and `.docx` formats.
4.  An error message is displayed if the user attempts to upload an unsupported file type.
5.  Upon selecting a valid file, the name of the file is displayed in the UI.

**Prerequisites:** Story 1.2

---

**Story 1.4: Backend Endpoint for CV Upload**

As a developer,
I want to create a secure backend endpoint that accepts a CV file upload,
So that the frontend can send the user's document for processing.

**Related FRs:** FR003

**Acceptance Criteria:**
1.  A new POST endpoint (e.g., `/api/v1/cv/upload`) is created in the FastAPI backend.
2.  The endpoint is configured to accept `multipart/form-data` file uploads.
3.  The endpoint successfully receives and temporarily saves the uploaded `.doc` or `.docx` file.
4.  The endpoint returns a unique identifier for the uploaded file upon success.
5.  The endpoint is connected to the frontend, and the file from Story 1.3 can be successfully sent to it.
6.  All data in transit to and from the endpoint is encrypted using HTTPS (NFR001).

**Prerequisites:** Story 1.3

---

**Story 1.5: CV Parsing Service**

As a developer,
I want to create a service that extracts the raw text content from an uploaded CV document,
So that it can be used as input for the AI analysis in the next epic.

**Related FRs:** FR004

**Acceptance Criteria:**
1.  A new service or function is created that takes a file path as input.
2.  The service uses the `python-docx` library to open and read the content of the `.doc` or `.docx` file.
3.  The service successfully extracts all text from the document into a single string.
4.  The service is integrated with the endpoint from Story 1.4, processing the file after it's uploaded.
5.  The extracted text is temporarily stored or cached, associated with the file's unique identifier.

**Prerequisites:** Story 1.4

---

**Story 1.6: Job Description Input Interface**

As a user,
I want a simple text area to paste the job description I'm interested in,
So that the system can analyze it against my CV.

**Related FRs:** FR005

**Acceptance Criteria:**
1.  The main workspace displays a large, clearly labeled text area for the job description.
2.  A "Submit for Analysis" or similar button is present below the text area.
3.  The text area is large enough to comfortably accommodate a typical job description.
4.  The interface is clean and free of distractions.

**Prerequisites:** Story 1.3

---

**Story 1.7: Backend Endpoint for Job Description**

As a developer,
I want to create a backend endpoint that accepts the job description text,
So that the frontend can send it for analysis.

**Related FRs:** FR005

**Acceptance Criteria:**
1.  A new POST endpoint (e.g., `/api/v1/job/analyze`) is created in the FastAPI backend.
2.  The endpoint accepts a JSON payload containing the raw text of the job description.
3.  The endpoint returns a unique identifier for the analysis job upon successful submission.
4.  The endpoint is connected to the frontend, and the text from the form in Story 1.6 can be successfully sent to it.
5.  All data in transit to and from the endpoint is encrypted using HTTPS (NFR001).

**Prerequisites:** Story 1.6

---

**Story 1.8: Initial Job Description Processing**

As a developer,
I want a basic service to receive the job description text and prepare it for analysis,
So that it's ready for the AI keyword extraction in the next epic.

**Related FRs:** FR006

**Acceptance Criteria:**
1.  A new service is created that takes the raw job description text as input.
2.  The service cleans and normalizes the text (e.g., removes excessive whitespace).
3.  The cleaned text is temporarily stored or cached, associated with the analysis job's unique identifier.
4.  The service is integrated with the endpoint from Story 1.7.

**Prerequisites:** Story 1.7

---

### Epic 2: AI-Powered Generation & Analysis

**Expanded Goal:** This epic brings the "smarts" to the application. We will integrate the Gemini AI model to analyze the data collected in Epic 1. This includes extracting structured information (skills, experience) from both the CV and the job description, performing a gap analysis, calculating an initial ATS score, and generating the first draft of a tailored cover letter.

---

**Story 2.1: AI Service Integration**

As a developer,
I want to establish a secure and reliable connection to the Gemini API,
So that the backend can send requests and receive responses from the AI model.

**Related FRs:** FR006, FR007, FR009, FR010, FR011

**Acceptance Criteria:**
1.  A new service or module is created to handle all interactions with the Gemini API.
2.  API keys and other sensitive configuration are securely managed (e.g., using environment variables).
3.  A basic "ping" function is implemented to test the connection to the Gemini API and returns a successful response.
4.  Error handling is implemented to gracefully manage API connection failures or errors.

**Prerequisites:** Story 1.1

---

**Story 2.2: AI-Powered Job Description Analysis**

As a developer,
I want to use the AI to analyze the job description text and extract a structured list of required skills and qualifications,
So that we have a clear, machine-readable list of requirements to compare against the user's CV.

**Related FRs:** FR006

**Acceptance Criteria:**
1.  A new function is created that sends the job description text to the Gemini API.
2.  The prompt is engineered to request a structured output (e.g., JSON) containing a list of skills, technologies, and years of experience required.
3.  The service successfully parses the AI's response into a structured data object.
4.  The extracted skills and qualifications are stored and associated with the analysis job.
5.  The process is integrated with the service from Story 1.8.

**Prerequisites:** Story 1.8, Story 2.1

---

**Story 2.3: AI-Powered CV Analysis**

As a developer,
I want to use the AI to analyze the user's CV text and extract a structured list of their skills, experiences, and qualifications,
So that we have a clear, machine-readable list of the user's qualifications to compare against the job requirements.

**Related FRs:** FR004, FR006, FR007, FR009, FR010

**Acceptance Criteria:**
1.  A new function is created that sends the extracted CV text to the Gemini API.
2.  The prompt is engineered to request a structured output (e.g., JSON) containing lists of the user's skills, technologies, and a summary of their experience.
3.  The service successfully parses the AI's response into a structured data object.
4.  The extracted information is stored and associated with the user's CV.
5.  The process is integrated with the service from Story 1.5.

**Prerequisites:** Story 1.5, Story 2.1

---

**Story 2.4: Gap Analysis Service**

As a developer,
I want to create a service that compares the skills extracted from the job description with the skills extracted from the user's CV,
So that we can identify what qualifications the user is missing.

**Related FRs:** FR009

**Acceptance Criteria:**
1.  A new service is created that takes the structured data from Story 2.2 (Job Analysis) and Story 2.3 (CV Analysis) as input.
2.  The service compares the two lists of skills and identifies which required skills are present in the CV and which are missing.
3.  The service outputs a structured list of "matched skills" and "missing skills."
4.  The results of the analysis are stored and associated with the analysis job.

**Prerequisites:** Story 2.2, Story 2.3

---

**Story 2.5: Basic ATS Score Calculation**

As a developer,
I want to create a service that calculates a basic ATS (Applicant Tracking System) score,
So that the user can get a simple metric of how well their CV matches the job description.

**Related FRs:** FR010

**Acceptance Criteria:**
1.  A new service is created that uses the output from the Gap Analysis service (Story 2.4).
2.  The service calculates a percentage score based on the ratio of matched skills to total required skills.
3.  The calculated score is stored and associated with the analysis job.
4.  The logic is simple, transparent, and ready to be displayed to the user.

**Prerequisites:** Story 2.4

---

**Story 2.6: AI Cover Letter Generation**

As a developer,
I want to use the AI to generate a tailored cover letter,
So that the user receives a high-quality first draft that highlights their relevant skills.

**Related FRs:** FR007

**Acceptance Criteria:**
1.  A new service is created that sends a comprehensive prompt to the Gemini API.
2.  The prompt includes the user's extracted CV data (Story 2.3), the job description's required skills (Story 2.2), and the identified gaps (Story 2.4).
3.  The prompt is engineered to produce a professional, well-structured cover letter in Norwegian.
4.  The generated cover letter text is received from the API and stored.
5.  The service is integrated to run as part of the main analysis job.
6.  The cover letter generation process consistently completes in under 120 seconds (NFR003).

**Prerequisites:** Story 2.4

---

**Story 2.7: Display Analysis Results**

As a user,
I want to see the results of the Gap Analysis and my ATS score in a clear, easy-to-understand format,
So that I can quickly identify my strengths and weaknesses for this job application.

**Related FRs:** FR009, FR010

**Acceptance Criteria:**
1.  A new component is created in the frontend to display the analysis results.
2.  The frontend fetches the Gap Analysis data (Story 2.4) and ATS score (Story 2.5) from the backend.
3.  The "missing skills" and "matched skills" are displayed in a visually distinct way (e.g., using lists with different colors or icons).
4.  The ATS score is displayed prominently, for example, as a percentage in a gauge or progress bar.
5.  The component is integrated into the main analysis view.

**Prerequisites:** Story 2.5

---

**Story 2.8: Display Generated Cover Letter**

As a user,
I want to see the generated cover letter in a text editor,
So that I can review it, make my own edits, and copy the final version.

**Related FRs:** FR008, FR012, FR013

**Acceptance Criteria:**
1.  A text editor component is added to the main analysis view on the frontend.
2.  The frontend fetches the generated cover letter text (Story 2.6) from the backend and displays it in the editor.
3.  The user can freely edit the text within the editor.
4.  A "Copy to Clipboard" button is implemented and functional.
5.  A "Download as .txt" button is implemented and functional.

**Prerequisites:** Story 2.6

---

**Story 2.9: Interactive Suggestions**

As a user,
I want to see interactive suggestions that connect the analysis to the generated cover letter,
So that I can understand *why* the AI made certain choices and how to improve my application.

**Related FRs:** FR011

**Acceptance Criteria:**
1.  When a user hovers over a "missing skill" in the analysis panel, the relevant sections in the job description could be highlighted.
2.  The system provides simple, actionable tooltips or suggestions next to the gap analysis results (e.g., "Consider adding this skill to your CV if you have it").
3.  The UI for these suggestions is clean, non-intrusive, and clearly educational.

**Prerequisites:** Story 2.7, Story 2.8

---

### Epic 3: User Dashboard & Iteration Loop

**Expanded Goal:** This epic transforms the tool from a one-off utility into a personalized platform. We will implement a secure user authentication system, create a personal dashboard where users can save and manage their application analyses, and enable them to track their progress over time. This creates the "iteration loop," allowing users to revisit, refine, and reuse their materials for different job opportunities.

---

**Story 3.1: User Registration**

As a new user,
I want to create a secure account with my email and a password,
So that I can save my work and access my personal dashboard.

**Related FRs:** FR001

**Acceptance Criteria:**
1.  A registration page is created with fields for name, email, and password.
2.  Client-side validation provides immediate feedback on password strength and email format.
3.  A backend endpoint is created to handle new user registration.
4.  The user's password is securely hashed before being stored in the database.
5.  Upon successful registration, the user is automatically logged in and redirected to their new dashboard.
6.  The user's password is securely hashed before being stored in the database (NFR001).
7.  The registration process is compliant with GDPR and Norwegian privacy regulations (NFR002).

**Prerequisites:** Story 1.1

---

**Story 3.2: User Login & Logout**

As a returning user,
I want to log in securely with my email and password and be able to log out,
So that I can access my saved application history and protect my account.

**Related FRs:** FR002

**Acceptance Criteria:**
1.  A login page is created with fields for email and password.
2.  A backend endpoint is created to authenticate users against the stored credentials.
3.  Upon successful login, a secure session (e.g., using JWT) is created, and the user is redirected to their dashboard.
4.  An appropriate error message is shown for invalid login attempts.
5.  A "Logout" button is available within the application, which, when clicked, terminates the user's session and redirects them to the homepage.

**Prerequisites:** Story 3.1

---

**Story 3.3: Authenticated Endpoints**

As a developer,
I want to protect sensitive backend endpoints,
So that only authenticated users can access their own data.

**Related FRs:** FR001, FR002

**Acceptance Criteria:**
1.  Backend middleware is implemented to check for a valid session token on protected routes.
2.  Endpoints for uploading CVs, analyzing jobs, and viewing history are protected.
3.  Requests to protected endpoints without a valid token are rejected with a `401 Unauthorized` error.
4.  A user can only access data that is associated with their own user ID.
5.  All data in transit is encrypted using HTTPS (NFR001).
6.  The authentication and authorization mechanisms are compliant with GDPR and Norwegian privacy regulations (NFR002).

**Prerequisites:** Story 3.2

---

**Story 3.4: Personal Dashboard UI**

As a user,
I want a personal dashboard page,
So that I have a central place to view my saved applications and start new ones.

**Acceptance Criteria:**
1.  A new page is created for the user dashboard, accessible only to logged-in users.
2.  The dashboard contains a clear "Start New Application Analysis" button.
3.  The main area of the dashboard is designated for a list of saved applications.
4.  If the user has no saved applications, a helpful message is displayed encouraging them to start one.

**Prerequisites:** Story 3.2

---

**Story 3.5: Save Application Analysis**

As a user,
I want to be able to save the results of a complete application analysis,
So that I can review it later without re-running the entire process.

**Acceptance Criteria:**
1.  A "Save" button is added to the main analysis view (from Epic 2).
2.  A new backend endpoint is created to save the state of an analysis job to the database.
3.  The saved data includes the original CV text, the job description, the generated cover letter, the gap analysis results, and the ATS score.
4.  Each saved analysis is linked to the authenticated user's ID.
5.  The user receives a confirmation message after the analysis is successfully saved.
6.  All saved data is encrypted at rest (NFR001).
7.  The data saving process is compliant with GDPR and Norwegian privacy regulations (NFR002).

**Prerequisites:** Story 2.8, Story 3.3

---

**Story 3.6: Display Saved Applications on Dashboard**

As a user,
I want to see a list of my previously saved applications on my dashboard,
So that I can quickly find and access my past work.

**Acceptance Criteria:**
1.  The dashboard frontend fetches the list of saved applications for the logged-in user from a new backend endpoint.
2.  Each item in the list displays key information, such as the job title (extracted from the job description), the date it was saved, and the ATS score.
3.  The list is ordered with the most recently saved applications at the top.
4.  Each item in the list is a clickable link or button.

**Prerequisites:** Story 3.4, Story 3.5

---

**Story 3.7: View Saved Application Details**

As a user,
I want to click on a saved application from my dashboard and see all of its details,
So that I can review my past work and reuse it.

**Acceptance Criteria:**
1.  Clicking on a saved application in the dashboard (from Story 3.6) navigates the user to a detailed view.
2.  This view re-populates the main analysis interface with the saved data, including the cover letter, gap analysis, and ATS score.
3.  All the information is presented in the same familiar layout as the original analysis view.
4.  The user can copy the cover letter or other details from this view.

**Prerequisites:** Story 3.6

---

**Story 3.8: Delete Saved Application**

As a user,
I want to be able to delete a saved application from my dashboard,
So that I can keep my workspace clean and organized.

**Acceptance Criteria:**
1.  Each saved application listed on the dashboard has a clearly marked "Delete" button or icon.
2.  Clicking the "Delete" button prompts the user with a confirmation dialog to prevent accidental deletion (e.g., "Are you sure you want to delete this application?").
3.  Upon confirmation, a request is sent to a new backend endpoint to delete the application record from the database.
4.  The item is immediately removed from the list on the dashboard without requiring a page reload.
5.  The deletion process is compliant with GDPR and Norwegian privacy regulations, ensuring data is properly removed (NFR002).

**Prerequisites:** Story 3.6

---

## Story Guidelines Reference

**Story Format:**

```
**Story [EPIC.N]: [Story Title]**

As a [user type],
I want [goal/desire],
So that [benefit/value].

**Acceptance Criteria:**
1. [Specific testable criterion]
2. [Another specific criterion]
3. [etc.]

**Prerequisites:** [Dependencies on previous stories, if any]
```

**Story Requirements:**

- **Vertical slices** - Complete, testable functionality delivery
- **Sequential ordering** - Logical progression within epic
- **No forward dependencies** - Only depend on previous work
- **AI-agent sized** - Completable in 2-4 hour focused session
- **Value-focused** - Integrate technical enablers into value-delivering stories

---

**For implementation:** Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown.

---

## Technical Unknowns and Spikes

This section identifies potential technical risks and proposes "spikes" (time-boxed research tasks) to address them before full implementation.

### 1. Gemini API for Structured Data Extraction

- **Unknown:** How reliably can the Gemini API consistently extract structured JSON data from unstructured CV and job description text? The format and quality of user-uploaded CVs and pasted job descriptions will vary significantly.
- **Risk:** If the AI cannot reliably provide structured data, the downstream services (Gap Analysis, ATS Score) will fail or produce inaccurate results.
- **Spike:**
    - **Goal:** Determine the optimal prompt engineering techniques and data cleaning strategies to ensure consistent and accurate JSON output from the Gemini API for a variety of sample CVs and job descriptions.
    - **Tasks:**
        1.  Gather a diverse set of 10-15 sample CVs and job descriptions (different formats, lengths, and industries).
        2.  Develop and test multiple prompt variations for Story 2.2 and Story 2.3.
        3.  Measure the success rate of parsing the AI's response into the required JSON structure.
        4.  Document the most effective prompt strategies and any pre-processing steps required.
    - **Timebox:** 8 hours.

### 2. CV Parsing Robustness

- **Unknown:** How robust is the `python-docx` library when handling a wide variety of `.doc` and `.docx` files, especially those with complex layouts, tables, columns, or embedded objects?
- **Risk:** The system may fail to parse certain CVs, leading to a poor user experience and inability to use the service.
- **Spike:**
    - **Goal:** Test the `python-docx` library against a corpus of challenging CV documents to identify potential failure points.
    - **Tasks:**
        1.  Collect a set of "difficult" CVs: old `.doc` formats, complex tables, multi-column layouts, headers/footers with important information, etc.
        2.  Write a script to run the parsing service from Story 1.5 against each document.
        3.  Log any errors or documents that result in incomplete or garbled text extraction.
        4.  Investigate and document potential workarounds or alternative libraries if `python-docx` proves insufficient for a significant percentage of cases.
    - **Timebox:** 4 hours.

### 3. End-to-End Analysis Performance

- **Unknown:** Can the entire analysis pipeline (CV parsing, job ad analysis, gap analysis, cover letter generation) consistently meet the <120 second performance requirement (NFR003)?
- **Risk:** If the process is too slow, users may become frustrated and abandon the service.
- **Spike:**
    - **Goal:** Create a proof-of-concept for the end-to-end analysis pipeline to measure its typical and worst-case performance.
    - **Tasks:**
        1.  Create a single script that simulates the full process: text extraction, calls to the Gemini API for job/CV analysis and cover letter generation, and gap analysis logic.
        2.  Run the script with a variety of input sizes (short and long CVs/job descriptions).
        3.  Measure the time taken for each step and the total time.
        4.  Identify any bottlenecks in the process.
        5.  Document the performance findings and any recommendations for optimization (e.g., parallelizing API calls).
    - **Timebox:** 6 hours.
