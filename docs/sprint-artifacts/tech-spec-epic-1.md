# Epic Technical Specification: Foundation & Core Application

Date: 2025-12-05
Author: BIP
Epic ID: 1
Status: Draft

---

## Overview

The "Foundation & Core Application" epic focuses on establishing the essential technical infrastructure and implementing the foundational functionalities of the AI CV & Job Application Assistant. This includes user authentication (account creation, login/logout), CV upload and initial parsing, and the input mechanism for job descriptions. This epic lays the groundwork for all subsequent AI-powered features by ensuring the core data ingestion and user management capabilities are robust and functional, aligning with the project's goal to significantly improve the interview-to-application ratio for users in the Norwegian job market.

## Objectives and Scope

**In-Scope:**
*   User account creation and secure authentication (FR001, FR002).
*   User login and logout functionality (FR002).
*   Ability for users to upload CVs in `.doc` or `.docx` format (FR003).
*   Initial parsing of uploaded CVs to extract basic information like work experience, education, and skills (FR004).
*   Provision of a text area for users to input or paste job descriptions (FR005).
*   Responsive and accessible user interface for all core functionalities across desktop and mobile devices (FR014).

**Out-of-Scope (for this epic):**
*   AI-powered analysis of job descriptions (FR006).
*   Generation of tailored cover letters (FR007).
*   Display of generated cover letters (FR008).
*   Identification of missing skills or gap analysis (FR009).
*   ATS compatibility score calculation (FR010).
*   Actionable suggestions for improving ATS score (FR011).
*   Copy or download functionality for generated cover letters (FR012, FR013).
*   Advanced security features beyond basic authentication and data encryption at rest/in transit (NFR001, NFR002).

## System Architecture Alignment

This epic primarily engages with the **Frontend Application** (Next.js, React, Tailwind CSS) for user interface and interaction, and the **Backend API** (Node.js, Express.js, PostgreSQL) for user management, authentication, and initial CV storage. The initial CV parsing will likely be a basic text extraction on the backend, preparing for the more advanced AI Service integration in subsequent epics. It establishes the basic data flow and user interaction patterns required before integrating the specialized **AI Service**.

## Detailed Design

### Services and Modules

*   **Frontend (Next.js Application)**:
    *   **User Authentication Module**: Handles UI for account creation, login, and logout. Interacts with Backend API for authentication.
    *   **CV Upload Component**: Provides UI for file selection and upload, including progress indicators.
    *   **Job Description Input Component**: Offers a text area for pasting job descriptions.
    *   **Core Layout/Navigation**: Responsive design, header, footer, and routing for main application pages.
    *   **`GapAnalysisDisplay`**: (Placeholder component - not active in this epic, but foundation may be laid).
    *   **`ATSScoreGauge`**: (Placeholder component - not active in this epic, but foundation may be laid).

*   **Backend (Node.js/Express.js API)**:
    *   **User Service**: Manages user registration, login, session management (JWT), and user profile data storage in PostgreSQL.
    *   **Authentication Middleware**: Protects API routes, validates JWT tokens.
    *   **CV Handling Service**: Receives uploaded CV files, stores them securely, and performs initial text extraction/parsing using a basic `python-docx` integration (potentially via a lightweight child process or early AI Service interaction if determined feasible for basic parsing).
    *   **Job Description Service**: Stores and retrieves job descriptions linked to user accounts.

### Data Models and Contracts

*   **User Model (PostgreSQL)**:
    *   `id` (UUID, PK)
    *   `email` (VARCHAR, UNIQUE, NOT NULL)
    *   `password_hash` (VARCHAR, NOT NULL)
    *   `created_at` (TIMESTAMP, NOT NULL)
    *   `updated_at` (TIMESTAMP, NOT NULL)

*   **CV Model (PostgreSQL / File Storage)**:
    *   `id` (UUID, PK)
    *   `user_id` (UUID, FK to User, NOT NULL)
    *   `filename` (VARCHAR, NOT NULL)
    *   `file_path` (VARCHAR, NOT NULL) - Path to stored file (e.g., S3 URL)
    *   `extracted_text` (TEXT) - Raw text extracted from CV
    *   `uploaded_at` (TIMESTAMP, NOT NULL)

*   **JobDescription Model (PostgreSQL)**:
    *   `id` (UUID, PK)
    *   `user_id` (UUID, FK to User, NOT NULL)
    *   `title` (VARCHAR)
    *   `content` (TEXT, NOT NULL) - Full job description text
    *   `created_at` (TIMESTAMP, NOT NULL)

### APIs and Interfaces

*   **Authentication API**:
    *   `POST /api/auth/register`: User registration.
        *   Request: `{ email, password }`
        *   Response: `{ token, user: { id, email } }`
    *   `POST /api/auth/login`: User login.
        *   Request: `{ email, password }`
        *   Response: `{ token, user: { id, email } }`
    *   `POST /api/auth/logout`: User logout (invalidate token server-side or client-side clear).
*   **CV API**:
    *   `POST /api/cv/upload`: Upload a CV file.
        *   Request: `multipart/form-data` with `file`
        *   Response: `{ cv_id, filename }`
    *   `GET /api/cv/{cv_id}`: Retrieve CV details.
*   **Job Description API**:
    *   `POST /api/job-description`: Save a job description.
        *   Request: `{ content }`
        *   Response: `{ jd_id, title }`
    *   `GET /api/job-description/{jd_id}`: Retrieve job description content.

### Workflows and Sequencing

1.  **User Registration:**
    *   Frontend sends `POST /api/auth/register`.
    *   Backend hashes password, stores user in DB, generates JWT.
    *   Backend returns JWT to Frontend.
    *   Frontend stores JWT and redirects to Workspace.

2.  **CV Upload:**
    *   User selects `.doc` or `.docx` file in Frontend.
    *   Frontend sends `POST /api/cv/upload` with file and JWT.
    *   Backend receives file, stores it (e.g., locally or S3), performs basic text extraction, saves metadata to DB.
    *   Backend returns `cv_id` to Frontend.

3.  **Job Description Input:**
    *   User pastes text into Frontend text area.
    *   Frontend sends `POST /api/job-description` with content and JWT.
    *   Backend saves job description to DB.
    *   Backend returns `jd_id` to Frontend.

## Non-Functional Requirements

### Performance

*   **NFR003 (partial):** User registration and login shall complete within 2 seconds under normal load. CV upload (excluding file transfer time) and job description saving shall complete within 3 seconds.
*   The system should maintain responsiveness with up to 100 concurrent users.

### Security

*   **NFR001:** All user data, including CVs and personal information (email, password hashes), must be encrypted at rest (PostgreSQL encryption) and in transit (HTTPS/TLS for all API communication).
*   **NFR002:** The platform must comply with GDPR and Norwegian privacy regulations regarding the collection and storage of personal data. This implies secure storage and appropriate access controls for CVs and user profiles.
*   Password hashing (e.g., bcrypt) will be used for user passwords.
*   JWTs will be used for session management, with appropriate expiry and secure storage (e.g., HttpOnly cookies).

### Reliability/Availability

*   **NFR004 (partial):** Frontend and Backend API services shall be available 99.5% of the time, excluding scheduled maintenance.
*   The system should gracefully handle failed file uploads or database connection issues, providing informative error messages to the user.

### Observability

*   **Logging:** Frontend and Backend will implement structured logging for critical events (user registration, login, API calls, errors).
*   **Monitoring:** Basic application performance monitoring (APM) will be integrated to track API response times and error rates.

## Dependencies and Integrations

### Frontend:
*   **React/Next.js**: Core framework.
*   **Tailwind CSS**: Styling.
*   **shadcn/ui**: Component library.
*   **Zustand/React Context**: State management.
*   **Axios/Fetch API**: For interacting with the Backend API.

### Backend:
*   **Node.js/Express.js**: Core framework.
*   **PostgreSQL**: Database.
*   **`bcrypt`**: For password hashing.
*   **`jsonwebtoken`**: For JWT generation and verification.
*   **`multer`**: For handling multipart/form-data (file uploads).
*   **`python-docx` (or similar library via interop)**: For basic text extraction from `.doc/.docx` files. This may involve invoking a Python script or a lightweight microservice.

## Acceptance Criteria (Authoritative)

1.  **AC1.1:** Users can successfully create a new account using a unique email and a password meeting complexity requirements. (FR001)
2.  **AC1.2:** Registered users can successfully log in with their credentials. (FR002)
3.  **AC1.3:** Authenticated users can successfully log out, invalidating their session. (FR002)
4.  **AC1.4:** Authenticated users can upload a CV in `.doc` or `.docx` format via the user interface. (FR003)
5.  **AC1.5:** The system successfully parses the text content from an uploaded `.doc` or `.docx` CV file. (FR004)
6.  **AC1.6:** Authenticated users can input/paste a job description into a dedicated text area. (FR005)
7.  **AC1.7:** All core user interface components (registration, login, CV upload, JD input) are fully responsive across desktop, tablet, and mobile browsers. (FR014)
8.  **AC1.8:** All user data (email, password hashes, CV text, JD text) is stored encrypted at rest in the database. (NFR001)
9.  **AC1.9:** All communication between the frontend and backend occurs over HTTPS/TLS. (NFR001)

## Traceability Mapping

| Acceptance Criteria | Spec Section(s)                                 | Component(s)/API(s)                  | Test Idea                                              |
| :------------------ | :---------------------------------------------- | :----------------------------------- | :----------------------------------------------------- |
| AC1.1               | Detailed Design (User Model, Auth API)          | Backend User Service, Frontend Auth UI | Register new user via UI, verify DB entry.             |
| AC1.2               | Detailed Design (User Model, Auth API)          | Backend User Service, Frontend Auth UI | Login with valid credentials, verify JWT received.     |
| AC1.3               | Detailed Design (Auth API)                      | Backend Auth Middleware, Frontend Auth UI | Logout, attempt to access protected route (should fail).|
| AC1.4               | Detailed Design (CV API, Frontend Components)   | Frontend CV Upload, Backend CV Service | Upload sample .doc/.docx, verify success message.      |
| AC1.5               | Detailed Design (CV Handling Service)           | Backend CV Service                   | Upload .doc/.docx, verify extracted text in DB.        |
| AC1.6               | Detailed Design (JobDescription API, Frontend Components) | Frontend JD Input, Backend JD Service | Paste sample JD, verify save success.                  |
| AC1.7               | UX Design Spec (Responsive Strategy)            | Frontend Application                 | Manual testing across device emulators/real devices.   |
| AC1.8               | Non-Functional (Security), Detailed Design (DB) | PostgreSQL                           | Database configuration review, data inspection.        |
| AC1.9               | Non-Functional (Security)                       | Nginx/Load Balancer, Express.js      | Network traffic inspection (ensure HTTPS).             |

## Risks, Assumptions, Open Questions

### Risks:
*   **R1:** Complexity of accurate `.doc/.docx` parsing for diverse CV formats.
    *   **Mitigation:** Start with a basic text extraction. Iteratively improve parsing and consider dedicated libraries or microservices if initial approach proves insufficient.
*   **R2:** Security vulnerabilities related to file uploads (e.g., malicious files).
    *   **Mitigation:** Implement strict file type validation, size limits, and robust sanitization/scanning of uploaded content. Store files in isolated, non-executable locations.
*   **R3:** Performance bottlenecks with large CVs or high concurrent uploads.
    *   **Mitigation:** Implement asynchronous processing for CV parsing. Monitor performance metrics closely and scale backend services as needed.

### Assumptions:
*   **A1:** Users will provide valid `.doc` or `.docx` files for CV uploads.
*   **A2:** The chosen LLM (Gemini/GPT-4) will be able to perform robust CV parsing and text extraction required for later epics.
*   **A3:** Standard cloud services (AWS RDS, S3) will provide sufficient encryption at rest and in transit.

### Open Questions:
*   **Q1:** What is the specific strategy for handling rich text formatting (bold, italics, lists) during CV parsing? Will it be preserved or converted to plain text?
*   **Q2:** How will rate limiting be implemented for authentication and file upload endpoints to prevent abuse?
*   **Q3:** Are there any specific localization requirements for error messages or UI elements beyond basic English/Norwegian?

## Test Strategy Summary

The test strategy for Epic 1 will focus on ensuring the fundamental stability, security, and usability of the core application.

*   **Unit Tests:** Extensive unit tests will be written for all backend services (authentication, user management, CV/JD handling) and critical frontend components (form validation, API integration).
*   **Integration Tests:** Integration tests will verify the communication between frontend and backend, particularly for user authentication flows, CV upload, and JD submission.
*   **End-to-End (E2E) Tests:** E2E tests (using tools like Cypress or Playwright) will simulate a user's journey through registration, login, CV upload, and JD input to ensure the entire flow functions correctly.
*   **Security Testing:** Manual penetration testing and automated security scans will be conducted on authentication endpoints and file upload mechanisms.
*   **Performance Testing:** Load tests will be executed on key endpoints (login, CV upload) to identify performance bottlenecks and validate NFRs.
*   **Accessibility Testing:** Automated (Lighthouse, axe DevTools) and manual (keyboard navigation, screen reader) accessibility testing will be performed.
*   **Manual Exploratory Testing:** Human testers will explore the application to uncover edge cases and usability issues not caught by automated tests.