# Product Requirements Document: AI CV & Job Application Assistant

**Date:** 2025-11-04
**Author:** John (Product Manager)
**Status:** Version 1.0

---

### Goals

*   Significantly increase the interview-to-application ratio for users.
*   Empower users with the knowledge and tools to confidently navigate the modern, AI-driven job market.
*   Establish the platform as the leading, hyper-localized solution for job seekers in Norway.
*   Achieve high user satisfaction and a strong Net Promoter Score (NPS).
*   Build a foundation for future B2B offerings and expansion into other Nordic markets.

### Background Context

The Norwegian job market is increasingly competitive, with many companies relying on Applicant Tracking Systems (ATS) to filter the high volume of applications they receive. This creates a significant hurdle for job seekers, particularly students, recent graduates, and those unfamiliar with the nuances of the Norwegian hiring landscape. Many qualified candidates are automatically rejected because their CVs and cover letters are not optimized for the keywords and criteria these systems look for.

The AI CV & Job Application Assistant directly addresses this problem by acting as an intelligent coach. It empowers users by analyzing their CV against specific job descriptions, generating tailored cover letters, and providing actionable feedback to bridge qualification gaps. By offering a solution that is hyper-localized for the Norwegian market—understanding its language, cultural norms, and recruitment practices—we provide a distinct advantage that generic, international tools cannot match. This project aims to level the playing field, giving every candidate the best possible chance to be seen by a human recruiter.

### Functional Requirements

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

### Non-Functional Requirements

*   **NFR001:** All user data, including CVs and personal information, must be encrypted at rest and in transit.
*   **NFR002:** The platform must comply with GDPR and Norwegian privacy regulations.
*   **NFR003:** The system shall generate a cover letter in under 120 seconds.
*   **NFR004:** The platform shall be available 99.5% of the time.

### User Journeys

#### Journey 1: First-Time User - Creating a Tailored Application

*   **Persona:** A recent university graduate in Norway, applying for their first full-time job.
*   **Goal:** To create a compelling, ATS-optimized application for a specific job posting.

1.  **Onboarding:** The user lands on the homepage and is prompted to create an account. They register using their email and a password. (FR001, FR002)
2.  **CV Upload:** After logging in, the user is guided to upload their current CV (`.doc` or `.docx`). The system parses the document and confirms the extraction of their education, skills, and work history. (FR003, FR004)
3.  **Job Description Input:** The user pastes the full text of a job description from any source (e.g., Finn.no, LinkedIn, company website) into a provided text field. (FR005)
4.  **Generation:** The user clicks "Generate Cover Letter." The AI analyzes both the CV and the job ad. (FR006, FR007)
5.  **Review & Insight:** The system presents a generated cover letter draft. Alongside it, a "Gap Analysis" panel appears, highlighting:
    *   **Missing Skills:** Key qualifications from the job ad that are not in the user's CV (e.g., "Project Management Software"). (FR009)
    *   **ATS Score:** A percentage score indicating how well the CV matches the job description's keywords. (FR010)
6.  **Iteration:** The user edits their CV details directly within the application to address the identified gaps. They regenerate the cover letter, and the ATS score updates in real-time, showing clear improvement. (FR011)
7.  **Finalize:** Satisfied with the result, the user copies the cover letter text and downloads their newly optimized CV. (FR012, FR013)

#### Journey 2: Career Changer - Optimizing an Existing CV

*   **Persona:** A professional with 10 years of experience looking to pivot into a new industry.
*   **Goal:** To understand how their existing skills translate to a new role and optimize their CV accordingly.

1.  **Dashboard:** The user, who has an existing account, logs in and navigates to their dashboard. (FR002)
2.  **Start New Analysis:** They choose to start a new application analysis, uploading their existing, generic CV. (FR003)
3.  **Target Job:** They paste the description of a job in their target industry. (FR005)
4.  **Analyze & Discover:** Instead of generating a cover letter immediately, the user focuses on the "Gap Analysis" feature. The system highlights that while they have strong "Team Leadership" skills, the job requires "Agile Methodology," which is missing from their CV. (FR009)
5.  **Actionable Suggestions:** The system provides suggestions, such as "Consider rephrasing your project management experience to highlight agile practices you may have used." (FR011)
6.  **Refine and Re-run:** The user edits their CV content within the tool, adding details about their experience with agile-like processes. They re-run the analysis and see their ATS score improve significantly.
7.  **Save for Later:** The user saves the optimized version of their CV to their dashboard, ready to be used for future applications in their new target industry.

### UX and UI Vision

#### UX Principles

1.  **Transparency and Trust:** The AI is not a black box. The interface will be designed to be educational, clearly explaining *why* it makes certain suggestions, thereby empowering the user and building their trust in the system.
2.  **Simplicity and Focus:** The user journey will be streamlined and intuitive, guiding the user step-by-step without overwhelming them. The focus is on getting them to a high-quality application with minimal friction.
3.  **Empowerment through Interaction:** The user is always in control. The platform provides intelligent suggestions, but the user makes the final decisions, with interactive elements that make it easy to accept, reject, or modify the AI's output.

#### Platform & Screens

*   **Platform:** A responsive web application with a mobile-first design, ensuring a seamless experience on desktops, tablets, and smartphones.
*   **Core Screens:**
    1.  **Landing Page:** A clean, modern page with a clear value proposition and a single, prominent call-to-action.
    2.  **Authentication:** Simple and secure screens for user registration and login.
    3.  **Workspace/Dashboard:** The main hub where users can start a new application analysis or view their saved applications and progress.
    4.  **Generation & Analysis View:** A dual-pane or split-screen interface where the user can see their input (CV/Job Ad), the AI-generated output (Cover Letter), and the analysis (Gap Analysis, ATS Score) all in one view.

#### Design Constraints

*   **Technology:** The frontend will be built with React/Next.js and styled with Tailwind CSS. The backend will be developed using Python with FastAPI.
*   **Branding:** The design will need to establish a new, clean, and professional brand identity. (No existing design system to adhere to).

### Epic List

Here is a proposed sequence for development.

*   **Epic 1: Foundation & Core Application**
    *   **Goal:** Establish the project's technical foundation and deliver the core functionality of CV parsing and job ad analysis.
    *   **Estimated Stories:** 8-12

*   **Epic 2: AI-Powered Generation & Analysis**
    *   **Goal:** Implement the core AI features, including cover letter generation, gap analysis, and the initial ATS score.
    *   **Estimated Stories:** 10-15

*   **Epic 3: User Dashboard & Iteration Loop**
    *   **Goal:** Build the user authentication, dashboard for managing applications, and the interactive feedback loop for improving documents.
    *   **Estimated Stories:** 7-10

### Out of Scope

The following features and capabilities are explicitly out of scope for the initial MVP release. They may be considered for future versions.

#### Immediate Exclusions:

*   **Advanced CV/Resume Editing:** The platform will not provide tools for deep CV formatting or design. The focus is on content optimization, not visual presentation.
*   **Direct Job Board Integration:** There will be no direct API integration with LinkedIn, Finn.no, or other job boards for importing listings or profiles in the MVP.
*   **Multi-language Support (beyond Norwegian/English):** The AI and UI will be optimized for Norwegian and English only.
*   **Mentor/Recruiter Feedback Module:** A feature for external users (like mentors or recruiters) to leave comments is not included.
*   **Personal Portfolio Dashboard:** While the system will process applications, a comprehensive dashboard for tracking application status, interview dates, etc., is post-MVP.

#### Future Considerations (Post-MVP):

*   **Tone and Style Control:** Allowing users to select different writing styles (e.g., formal, creative) for the AI-generated content.
*   **Expanded File Support:** Support for additional file formats like PDF for CV uploads.
*   **B2B Offerings:** A separate product offering for recruitment agencies or HR departments.
*   **Interview Preparation Tools:** AI-powered tools to help users prepare for interviews.
