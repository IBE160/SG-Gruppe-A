# ibe160 - Epic Breakdown

**Author:** BIP
**Date:** 2025-11-26
**Project Level:** beginner


---

## Overview

This document provides the complete epic and story breakdown for ibe160, decomposing the requirements from the [PRD](./PRD.md) into implementable stories.

**Living Document Notice:** This is the initial version. It will be updated after UX Design and Architecture workflows add interaction and technical details to stories.

🆕 **INITIAL CREATION MODE**

No existing epics found - I'll create the initial epic breakdown.

**Available Context:**
- ✅ PRD (required)
- ✅ UX Design (will incorporate interaction patterns)
- ✅ Architecture (will incorporate technical decisions)

## Epic Summary

Here is the proposed epic structure for the project:

*   **Epic 1: Foundation & User Onboarding**
    *   **Value:** Establish the project's technical foundation and allow users to create an account and log in.
    *   **Scope:** Project setup, core infrastructure, deployment pipeline, user authentication.

*   **Epic 2: Core Analysis Engine**
    *   **Value:** Provide the core value proposition of the application: analyzing a user's CV against a job description.
    *   **Scope:** CV parsing, job description analysis, gap analysis, ATS score calculation.

*   **Epic 3: AI-Powered Content Generation**
    *   **Value:** Generate a tailored cover letter based on the analysis.
    *   **Scope:** Cover letter generation, displaying the letter, allowing users to copy and download it.

*   **Epic 4: Responsive & Accessible UI**
    *   **Value:** Ensure the application is usable and accessible on all modern devices.
    *   **Scope:** Responsive design, accessibility compliance.

---

## Functional Requirements Inventory

*   **FR001:** The system must allow users to create a secure account using an email and password.
*   **FR002:** The system must allow authenticated users to log in and log out.
*   **FR003:** The system must allow users to upload a CV in `.doc` or `.docx` format.
*   **FR004:** The system must parse the uploaded CV to extract key information, including work experience, education, and skills.
*   **FR005:** The system must provide a text area for users to paste a job description.
*   **FR006:** The system must analyze the pasted job description to identify key skills, qualifications, and keywords.
*   **FR007:** The system must generate a tailored cover letter in Norwegian (Bokmål/Nynorsk) based on the user's CV and the job description.
*   **FR008:** The system must present the generated cover letter to the user in an editable text area.
*   **FR009:** The system must identify and display a list of key skills and qualifications from the job description that are missing from the user's CV.
*   **FR010:** The system must provide a basic ATS compatibility score (e.g., a percentage) based on keyword matching between the CV and the job description.
*   **FR011:** The system must provide actionable suggestions to the user for improving their ATS score.
*   **FR012:** The system must allow users to copy the generated cover letter text to their clipboard.
*   **FR013:** The system must allow users to download the generated cover letter as a text file.
*   **FR014:** The user interface must be responsive and accessible on modern web browsers on both desktop and mobile devices.

---

## FR Coverage Map

*   **Epic 1 (Foundation & User Onboarding):** Covers FR001, FR002.
*   **Epic 2 (Core Analysis Engine):** Covers FR003, FR004, FR005, FR006, FR009, FR010, FR011.
*   **Epic 3 (AI-Powered Content Generation):** Covers FR007, FR008, FR012, FR013.
*   **Epic 4 (Responsive & Accessible UI):** Covers FR014.

---



## Epic 1: Foundation & User Onboarding

Establish the project's technical foundation and allow users to create an account and log in.



### Story 1.1: Project Setup

As a developer, I want to have a bootstrapped Next.js application with all the necessary dependencies, so that I can start building the frontend.

**Acceptance Criteria:**

**Given** a new project is created
**When** I run `npm install`
**Then** all dependencies are installed without errors

**And** when I run `npm run dev`
**Then** the Next.js development server starts successfully.

**Prerequisites:** None

**Technical Notes:** Use `create-next-app` to bootstrap the project. Include `tailwindcss`.

### Story 1.2: User Account Creation

As a new user, I want to be able to create a secure account with my email and password, so that I can access the application's features.

**Acceptance Criteria:**

**Given** a user is on the registration page
**When** they enter a valid email and a password that meets the security requirements (e.g., 8+ characters, 1 uppercase, 1 number, 1 special character)
**And** they click the "Sign Up" button
**Then** a new user account is created in the database
**And** the user is redirected to the login page or directly logged in.

**Prerequisites:** Story 1.1

**Technical Notes:** The backend API needs an endpoint for user registration (e.g., `POST /api/v1/auth/register`). Passwords must be hashed before being stored in the database.

### Story 1.3: User Login

As a registered user, I want to be able to log in with my email and password, so that I can access my account and saved data.

**Acceptance Criteria:**

**Given** a user is on the login page
**When** they enter their correct email and password
**And** they click the "Log In" button
**Then** the system authenticates the user
**And** a JWT token is returned to the client
**And** the user is redirected to their dashboard.

**Prerequisites:** Story 1.2

**Technical Notes:** The backend API needs an endpoint for user login (e.g., `POST /api/v1/auth/login`). The JWT token should be stored securely on the client (e.g., in an HttpOnly cookie).

### Story 1.4: User Logout

As an authenticated user, I want to be able to log out of the application, so that my session is terminated and my account is secure.

**Acceptance Criteria:**

**Given** an authenticated user is in the application
**When** they click the "Log Out" button
**Then** their session is terminated
**And** they are redirected to the homepage.

**Prerequisites:** Story 1.3

**Technical Notes:** The client should discard the JWT token. If using server-side sessions, the session should be invalidated.

### Story 1.5: AI Service Integration and Proof-of-Concept

As a developer, I want to establish a connection to the AI service and validate its core functionalities, so that we can de-risk the project and ensure the AI-powered features can be built.

**Acceptance Criteria:**

*   **Given** the project is set up
*   **When** a connection to the chosen LLM's API is attempted
*   **Then** the connection is successful.
*   **And when** a sample CV and job description are sent to the AI service
*   **Then** the service can successfully parse the CV, analyze the job description, and generate a basic cover letter.

**Prerequisites:** Story 1.1

**Technical Notes:** This story involves selecting the LLM provider (e.g., OpenAI, Gemini), setting up API keys securely, and creating a basic Python script or service to interact with the API. The focus is on a proof-of-concept, not a production-ready implementation. This story is a critical prerequisite for Epic 2 and Epic 3.



---



---

## Epic 2: Core Analysis Engine

Provide the core value proposition of the application: analyzing a user's CV against a job description.

### Story 2.1: CV Upload

As a user, I want to upload my CV in `.doc` or `.docx` format, so that the system can analyze it.

**Acceptance Criteria:**

**Given** a user is on the dashboard
**When** they select a `.doc` or `.docx` file to upload
**And** they click "Upload"
**Then** the file is successfully uploaded to the server.

**Prerequisites:** Story 1.3

**Technical Notes:** The frontend needs a file input component. The backend needs an endpoint to handle file uploads.

### Story 2.2: CV Parsing

As a developer, I want to parse the uploaded CV file, so that I can extract the text content for analysis.

**Acceptance Criteria:**

**Given** a CV file has been uploaded
**When** the parsing process is triggered
**Then** the text content of the CV is extracted and stored.

**Prerequisites:** Story 2.1

**Technical Notes:** Use a library like `python-docx` in the AI service to parse the CV content.

### Story 2.3: Job Description Input

As a user, I want to paste a job description into a text area, so that the system can analyze it.

**Acceptance Criteria:**

**Given** a user is on the dashboard
**When** they paste text into the job description text area
**Then** the text is successfully captured by the application.

**Prerequisites:** Story 1.3

**Technical Notes:** A simple `<textarea>` element on the frontend will suffice.

### Story 2.4: Job Description Analysis

As a developer, I want to analyze the job description to identify key skills, qualifications, and keywords, so that I can compare them with the user's CV.

**Acceptance Criteria:**

**Given** a job description has been submitted
**When** the analysis process is triggered
**Then** a list of key skills, qualifications, and keywords is extracted.

**Prerequisites:** Story 2.3

**Technical Notes:** Use an LLM in the AI service to analyze the job description.

### Story 2.5: Gap Analysis

As a user, I want to see a list of key skills and qualifications from the job description that are missing from my CV, so that I can improve my CV.

**Acceptance Criteria:**

**Given** a CV and job description have been analyzed
**When** the gap analysis is displayed
**Then** the user can see a clear list of missing skills and qualifications.

**Prerequisites:** Story 2.2, Story 2.4

**Technical Notes:** The AI service will compare the extracted skills from the CV and job description and return the differences.

### Story 2.6: ATS Score Calculation

As a user, I want to see a basic ATS compatibility score, so that I can understand how well my CV matches the job description.

**Acceptance Criteria:**

**Given** a CV and job description have been analyzed
**When** the ATS score is displayed
**Then** the user sees a percentage score representing the match between their CV and the job description.

**Prerequisites:** Story 2.2, Story 2.4

**Technical Notes:** The AI service will calculate a score based on keyword matching.

### Story 2.7: Actionable Suggestions

As a user, I want to receive actionable suggestions for improving my ATS score, so that I can make my CV more competitive.

**Acceptance Criteria:**

**Given** an ATS score has been calculated
**When** the suggestions are displayed
**Then** the user sees a list of concrete actions they can take to improve their score.

**Prerequisites:** Story 2.6

**Technical Notes:** The AI service will generate suggestions based on the gap analysis.

---

## Epic 3: AI-Powered Content Generation

Generate a tailored cover letter based on the analysis.

### Story 3.1: Cover Letter Generation

As a user, I want the system to generate a tailored cover letter in Norwegian based on my CV and the job description, so that I can have a strong starting point for my application.

**Acceptance Criteria:**

**Given** a CV and job description have been analyzed
**When** the user clicks "Generate Cover Letter"
**Then** a cover letter is generated in Norwegian (Bokmål/Nynorsk).

**Prerequisites:** Story 2.2, Story 2.4

**Technical Notes:** The AI service will use an LLM to generate the cover letter.

### Story 3.2: Display Generated Cover Letter

As a user, I want to see the generated cover letter in an editable text area, so that I can review and modify it.

**Acceptance Criteria:**

**Given** a cover letter has been generated
**When** it is displayed to the user
**Then** the user sees the full text of the cover letter in a text area where they can make changes.

**Prerequisites:** Story 3.1

**Technical Notes:** A `<textarea>` element on the frontend will be used to display the cover letter.

### Story 3.3: Copy Cover Letter

As a user, I want to be able to copy the generated cover letter text to my clipboard, so that I can easily paste it into an email or another application.

**Acceptance Criteria:**

**Given** a cover letter is displayed
**When** the user clicks the "Copy" button
**Then** the text of the cover letter is copied to their clipboard.

**Prerequisites:** Story 3.2

**Technical Notes:** Use the browser's Clipboard API.

### Story 3.4: Download Cover Letter

As a user, I want to be able to download the generated cover letter as a text file, so that I can save it for my records.

**Acceptance Criteria:**

**Given** a cover letter is displayed
**When** the user clicks the "Download" button
**Then** a `.txt` file containing the cover letter is downloaded to their device.

**Prerequisites:** Story 3.2

**Technical Notes:** The frontend will create a blob with the cover letter content and trigger a download.

---

## Epic 4: Responsive & Accessible UI

Ensure the application is usable and accessible on all modern devices.

### Story 4.1: Responsive Design

As a user, I want to be able to use the application on my mobile phone, tablet, or desktop computer, so that I can work on my job applications from anywhere.

**Acceptance Criteria:**

**Given** a user is accessing the application on a mobile, tablet, or desktop device
**When** they view any page
**Then** the layout adapts to the screen size and all content is readable and accessible.

**Prerequisites:** Story 3.2

**Technical Notes:** Use `tailwindcss` responsive design features to create a mobile-first layout.

### Story 4.2: Accessibility Compliance

As a user with disabilities, I want to be able to use the application with assistive technologies like screen readers, so that I can have the same opportunities as other users.

**Acceptance Criteria:**

**Given** a user is navigating the application with a keyboard
**When** they move between interactive elements
**Then** all elements are focusable and have clear focus indicators.

**And** given a user is using a screen reader
**When** they navigate the application
**Then** all images have alt text, and all form elements have labels.

**Prerequisites:** Story 4.1

**Technical Notes:** Follow WCAG 2.1 AA guidelines. Use semantic HTML and ARIA attributes where necessary.

---



---

## FR Coverage Matrix

| FR | Description | Epic | Story |
|---|---|---|---|
| FR001 | Create secure account | 1 | 1.2 |
| FR002 | Authenticated login/logout | 1 | 1.3, 1.4 |
| FR003 | Upload CV | 2 | 2.1 |
| FR004 | Parse CV | 2 | 2.2 |
| FR005 | Paste job description | 2 | 2.3 |
| FR006 | Analyze job description | 2 | 2.4 |
| FR007 | Generate cover letter | 3 | 3.1 |
| FR008 | Present cover letter | 3 | 3.2 |
| FR009 | Identify missing skills | 2 | 2.5 |
| FR010 | Provide ATS score | 2 | 2.6 |
| FR011 | Provide actionable suggestions | 2 | 2.7 |
| FR012 | Copy cover letter | 3 | 3.3 |
| FR013 | Download cover letter | 3 | 3.4 |
| FR014 | Responsive and accessible UI | 4 | 4.1, 4.2 |

---

## Summary

This document provides a complete epic and story breakdown for the AI CV & Job Application Assistant. The project has been decomposed into four value-driven epics, and each epic has been broken down into a series of user stories with clear acceptance criteria. All functional requirements from the PRD have been mapped to stories, ensuring complete coverage.

The epic breakdown is as follows:
*   **Epic 1: Foundation & User Onboarding**
*   **Epic 2: Core Analysis Engine**
*   **Epic 3: AI-Powered Content Generation**
*   **Epic 4: Responsive & Accessible UI**

This breakdown provides a clear path for iterative development and delivery of value to the user.

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._

_This document will be updated after UX Design and Architecture workflows to incorporate interaction details and technical decisions._
