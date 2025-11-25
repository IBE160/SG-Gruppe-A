# ibe160 UX Design Specification

_Created on 2025-11-14 by BIP_
_Generated using BMad Method - Create UX Design Workflow v1.0_

---

## Executive Summary

The AI CV & Job Application Assistant is a web application designed to empower job seekers in the Norwegian market by streamlining the creation of tailored and effective job applications. It addresses the critical problem of applicants being filtered out by Applicant Tracking Systems (ATS) due to poorly optimized CVs and cover letters. The platform's core value proposition lies in its AI-powered ability to analyze job descriptions, generate personalized cover letters, and identify skill gaps, thereby significantly increasing users' chances of securing interviews and advancing their careers. The Norwegian market presents a significant opportunity for a hyper-localized solution that understands Norwegian language nuances and cultural expectations.

### Target Users
*   **Primary:** Students and young professionals in Norway seeking their first job or internship.
*   **Secondary:** Professionals in Norway looking to change careers or re-enter the job market, and foreign job seekers adapting to the Norwegian context.

### Desired Emotional Response
Users should feel **Efficient and productive** when using the application.

### Inspiration and UX Patterns
No specific apps or examples were provided for inspiration. The design will focus on established best practices for efficiency and productivity.

---

## Project Synthesis

**Vision:** To create an AI-powered web application that analyzes CVs and job postings to generate optimized, personalized cover letters, identifies missing qualifications, suggests improvements, and helps users understand how AI evaluates applications in modern recruitment.

**Users:**
*   **Primary:** Students and young professionals in Norway seeking their first job or internship.
*   **Secondary:** Professionals in Norway looking to change careers or re-enter the job market, and foreign job seekers adapting to the Norwegian context.

**Core Experience:** The one thing users will do most is create good cover letters and CVs. Uploading a CV should be effortless. The page should clearly guide the user to different functionalities.

**Desired Feeling:** Users should feel Efficient and productive.

**Platform:** Primarily a website in a browser on desktop, with mobile browser as secondary.

**Inspiration:** No specific apps or examples were provided for inspiration. The design will focus on established best practices for efficiency and productivity.

**UX Complexity:** Medium.

---

## 1. Design System Foundation

### 1.1 Design System Choice

**System:** shadcn/ui (v0.8.0)
**Rationale:** The user chose shadcn/ui for its balance of speed, aesthetics, and customization, especially given the project's use of Tailwind CSS. It allows for rapid development of a polished UI while retaining full control over the code and ensuring accessibility.
**Provides:** A collection of pre-styled, accessible components built on Radix UI and styled with Tailwind CSS.
**Customization needs:** Components are owned by the project, allowing for full customization.


---

## 2. Core User Experience

### 2.1 Defining Experience

**Defining Experience:** The app is a simple web page where users are prompted to upload their CV and job descriptions to receive improved feedback and cover letters.

### 2.2 Novel UX Patterns

**AI-Assisted Critique Panel**

To elevate the user experience beyond simple generation, a novel UX pattern called the "AI-Assisted Critique Panel" will be introduced. This is a real-time feedback mechanism that analyzes the user's cover letter as they type.

*   **Purpose:** To provide immediate, actionable suggestions that help users refine their writing, align it with the job description, and improve its overall quality and effectiveness.
*   **Interaction:** As the user types in the cover letter editor, the Critique Panel on the side provides color-coded highlights and suggestions directly on the text. On hover, a small pop-up explains the suggestion.
*   **Feedback Categories:** The panel will provide feedback on:
    *   **Tone:** Is the tone professional, confident, and appropriate for the role?
    *   **Keyword Alignment:** Does the letter incorporate key skills and terms from the job description?
    *   **Clarity and Conciseness:** Are there sentences that are too long, confusing, or contain jargon?
    *   **Impact:** Does the user effectively communicate their accomplishments and value?

### 2.3 Core Experience Principles

**Speed:** Key actions (upload, generate, receive feedback) should feel instantaneous or very fast, with clear progress indicators for longer processes.
**Guidance:** Users need clear, concise guidance, especially for first-time use and understanding AI feedback. The interface should be intuitive and self-explanatory.
**Flexibility:** The system should offer a balance of control (editing generated content) and simplicity (one-click generation). Users should feel empowered to refine the AI's output.
**Feedback:** Feedback should be immediate, clear, and actionable, especially for gap analysis and ATS scoring. It should reinforce efficiency and productivity.

---

## 3. Visual Foundation

### 3.1 Color System

**Chosen Theme:** Trustworthy Professional (Option 1)
**Rationale:** Conveys trust and reliability, aligning with the professional nature of job applications.

**Color Palette:**
*   **Primary:** #2563eb (main actions, key elements)
*   **Secondary:** #4f46e5 (supporting actions)
*   **Accent:** #db2777 (highlights)
*   **Success:** #16a34a (positive feedback)
*   **Error:** #dc2626 (negative feedback)
*   **Neutral:** Grayscale (for backgrounds, text, borders)

**Color Accessibility:**
*   All text and UI elements will be checked to ensure they meet a minimum contrast ratio of 4.5:1 (WCAG AA) against their background.

**Typography System:**
*   **Font Families:** Clean sans-serif for body and headings (e.g., system font stack or a font like Inter/Roboto). Monospace for code/technical elements.
*   **Type Scale:** Standard hierarchical scale (h1-h6, body, small, tiny) for clear information architecture.
*   **Font Weights:** Regular, Medium, Semibold for emphasis and visual hierarchy.
*   **Line Heights:** Optimized for readability across all text sizes.
*   **Starting Point:** shadcn/ui default typography.

**Spacing and Layout Foundation:**
*   **Base Unit:** 4px (for fine-grained control and consistent scaling).
*   **Spacing Scale:** Consistent scale based on the 4px base unit (e.g., `p-1` = 4px, `p-2` = 8px, etc., compatible with Tailwind CSS).
*   **Layout Grid:** 12-column grid system for flexible and responsive content arrangement.
*   **Container Widths:** Responsive container widths (e.g., `max-w-screen-xl`) to ensure optimal readability and visual balance on various screen sizes.


**Interactive Visualizations:**

- Color Theme Explorer: [ux-color-themes.html](./ux-color-themes.html)

---

## 4. Design Direction

### 4.1 Chosen Design Approach

**Chosen Direction:** A hybrid approach was selected:
*   **Landing Page:** A combination of "Focused Hero" (Direction 1) and "Feature-rich Overview" (Direction 2). It will feature a strong hero section with a clear call to action, followed by sections explaining "How it Works" and "Key Benefits".
*   **Generation & Analysis View:** "Dual Pane" (Direction 3) for its efficiency and directness, with input on the left and output/feedback on the right.

**Rationale:** This approach provides a clear and direct landing page that also offers key information about the product's functionality and benefits. For the core functionality, a dual-pane view is preferred for its efficiency and directness.

**Layout Decisions:**
*   **Navigation pattern:** Top navigation bar with login/signup.
*   **Content structure:** Hero section with a clear CTA, followed by sections explaining "How it Works" and "Key Benefits".
*   **Generation/Analysis View:** Dual-pane layout with input on the left and output/feedback on the right.

**Hierarchy Decisions:**
*   **Visual density:** Balanced, with a clear focus on the primary CTA.
*   **Header emphasis:** Bold headers for sections.
*   **Content focus:** Text-focused with potential for icons in the "Key Benefits" section.

**Interaction Decisions:**
*   **Primary action pattern:** Prominent button in the hero section.
*   **Information disclosure:** Progressive disclosure (users see more details as they scroll).

**Visual Style Decisions:**
*   **Weight:** Balanced, professional.
*   **Depth cues:** Subtle shadows on cards/sections.
*   **Border style:** Subtle borders to define sections.


**Interactive Mockups:**

- Design Direction Showcase: [ux-design-directions.html](./ux-design-directions.html)

---

## 5. User Journey Flows

### 5.1 Critical User Paths

**Journey: First-Time User - Creating a Tailored Application**
**User Goal:** To create a compelling, ATS-optimized application for a specific job posting.
**Approach:** Single-Screen Approach (Dual Pane)

**Flow Steps:**
1.  **Entry:** User lands on the homepage, which has a simple description of the service and a "Get Started" link.
    *   **User sees:** A clean landing page with a clear value proposition.
    *   **User does:** Clicks "Get Started", "Log In", or "Sign Up".
    *   **System responds:** Presents a simple login/signup form.
2.  **Authentication:** User provides an email and password to sign up or log in.
    *   **User sees:** A form with fields for email and password.
    *   **User does:** Enters their credentials and submits the form.
    *   **System responds:** Authenticates the user and redirects them to the main workspace/dashboard.
3.  **Workspace Interaction:** The user is on the main dual-pane workspace.
    *   **User sees:** An interface split into two main sections: an input area on the left and an output area on the right (initially empty or with placeholder text).
    *   **User does:** Uploads their CV and pastes a job description into the respective fields in the input area. Clicks "Generate & Analyze".
    *   **System responds:** Shows a loading indicator while processing. The output area is then populated with the generated cover letter, a gap analysis, and an ATS score.
4.  **Review and Success:** The user reviews the generated content and feedback.
    *   **User sees:** A tailored cover letter, a list of missing skills, and a percentage-based ATS score.
    *   **User does:** Can edit the generated text, copy it, or download it.
    *   **Success State:** The user has successfully received a tailored cover letter and actionable feedback, achieving their goal.

**Error States:**
*   **Invalid File Upload:** If the user uploads a file that is not a `.doc` or `.docx`, the system will show an inline error message and prevent submission.
*   **API/Generation Failure:** If the AI fails to generate content, a user-friendly error message will appear in the output area with a "Retry" button.

**Mermaid Diagram:**
```mermaid
graph TD
    A[Start: Homepage] --> B{User clicks "Get Started"};
    B --> C[Login/Sign Up Page];
    C --> D{User enters credentials};
    D --> E[Workspace: Dual Pane View];
    E --> F{User uploads CV & pastes job description};
    F --> G[Clicks "Generate & Analyze"];
    G --> H((Processing...));
    H --> I[Output Pane Populated];
    I --> J{Review Cover Letter & Feedback};
    J --> K[Success: Copy/Download Content];
    K --> L[End];

    D -- Invalid Credentials --> C;
    F -- Invalid File Type --> E;
    H -- Generation Fails --> E;
```

**Journey: Career Changer - Optimizing an Existing CV**
**User Goal:** To understand how their existing skills translate to a new role and optimize their CV accordingly.
**Approach:** Single-Screen Approach (Dual Pane)

**Flow Steps:**
1.  **Entry:** User lands on the homepage, logs in/signs up, and is redirected to the dashboard.
    *   **User sees:** A clean landing page with login/signup options, then a dashboard with an option to upload CV.
    *   **User does:** Logs in/signs up, then navigates to the CV upload section.
    *   **System responds:** Authenticates the user and presents the dashboard.
2.  **Input:** User uploads their existing CV and pastes a job description.
    *   **User sees:** The dual-pane workspace with fields for CV upload and job description input.
    *   **User does:** Uploads their CV and pastes the job description. Clicks "Generate & Analyze".
    *   **System responds:** Shows a loading indicator. The output pane displays the gap analysis, ATS score, and actionable suggestions.
3.  **Review and Iteration:** User reviews the analysis and suggestions.
    *   **User sees:** A detailed gap analysis, ATS score, and specific recommendations for improving their CV.
    *   **User does:** Edits their CV content (either directly in the app or externally and re-uploads) to address gaps. Re-runs the analysis.
    *   **System responds:** Updates the ATS score and gap analysis in real-time, showing improvement.
4.  **Success:** User is satisfied with the optimized CV.
    *   **User sees:** An improved ATS score and relevant suggestions.
    *   **User does:** Saves the optimized CV or downloads it.
    *   **Success State:** The user has successfully optimized their CV for a new role based on AI suggestions.

**Error States:**
*   **Invalid File Upload:** If the user uploads a file that is not a `.doc` or `.docx`, the system will show an inline error message and prevent submission.
*   **API/Analysis Failure:** If the AI fails to perform the analysis, a user-friendly error message will appear in the output area with a "Retry" button.

**Mermaid Diagram:**
```mermaid
graph TD
    A[Start: Homepage] --> B{User logs in/signs up};
    B --> C[Dashboard];
    C --> D[Workspace: Dual Pane View];
    D --> E{User uploads CV & pastes job description};
    E --> F[Clicks "Generate & Analyze"];
    F --> G((Processing...));
    G --> H[Output Pane Populated with Analysis];
    H --> I{Review Gap Analysis & Suggestions};
    I --> J{User edits CV / Re-runs Analysis};
    J --> G;
    I --> K[Success: Optimized CV];
    K --> L[End];

    B -- Invalid Credentials --> A;
    E -- Invalid File Type --> D;
    G -- Analysis Fails --> D;
```

---

## 6. Component Library

### 6.1 Component Strategy

Our strategy is to leverage the `shadcn/ui` component library as the primary source for all UI elements to ensure consistency, accessibility, and development speed. Custom components will only be created when a specific need is not met by the existing library.

**Primary Source:**
*   **Library:** `shadcn/ui`
*   **Usage:** All standard UI elements (buttons, forms, modals, etc.) will be sourced directly from this library.

**Custom Components:**
The following custom components have been identified as necessary for the application's unique features:

1.  **`GapAnalysisDisplay`**
    *   **Purpose:** To visually represent the skills and qualifications that the user is missing for a specific job.
    *   **Functionality:** This component will display a list of missing keywords and skills, potentially with a visual indicator (e.g., a red 'x') next to each. It may also suggest ways to incorporate these skills into the user's CV.

2.  **`ATSScoreGauge`**
    *   **Purpose:** To provide a visual representation of the user's ATS score.
    *   **Functionality:** This component will display a circular gauge or progress bar that shows the calculated ATS score as a percentage. The color of the gauge will change based on the score (e.g., red for low, yellow for medium, green for high) to provide immediate visual feedback.

---

## 7. UX Pattern Decisions

### 7.1 Consistency Rules

**UX Pattern Decisions:**

*   **Button Hierarchy:**
    *   **Primary Action:** Solid, high-contrast button (e.g., "Generate & Analyze"). Used for the main success action on a page.
    *   **Secondary Action:** Outline or subtle button (e.g., "Save Draft"). For less important, alternative actions.
    *   **Destructive Action:** Red outline or ghost button (e.g., "Delete"). Clearly indicates a potentially permanent action.

*   **Feedback Patterns:**
    *   **Success:** A temporary, auto-dismissing "toast" notification at the top of the screen (e.g., "CV uploaded successfully!").
    *   **Error:** An inline error message next to the field that caused it (e.g., "Invalid file type"). For form-level errors, a summary `Alert` at the top.
    *   **Loading:** A subtle spinner or pulsing animation on the element that is loading (e.g., the "Generate" button or the output panel).

*   **Form Patterns:**
    *   **Label Position:** Labels above their input fields for clarity and scannability.
    *   **Validation Timing:** Validate user input `onBlur` (when they click out of a field) to provide feedback without being intrusive.
    *   **Error Display:** A clear, concise error message displayed directly below the problematic field.

*   **Modal Patterns:**
    *   **Dismiss Behavior:** Allow users to close modals by clicking a dedicated "Close" (X) button, pressing the Escape key, or clicking the semi-transparent overlay.
    *   **Focus Management:** Automatically trap focus inside the modal so keyboard users can't accidentally tab to elements behind it.


---

## 8. Responsive Design & Accessibility

### 8.1 Responsive Strategy

**Responsive Design:**

1.  **Desktop (1200px and up):**
    *   **Layout:** Multi-column, dual-pane layout for the core analysis screen.
    *   **Extra Space Usage:** Used for clear labeling, contextual help text (e.g., tooltips explaining ATS scores), and a spacious, uncluttered feel.

2.  **Tablet (approx. 768px to 1199px):**
    *   **Layout:** Similar to desktop on larger tablets (landscape). Gracefully collapses to a single-column, tabbed interface on smaller tablets or in portrait mode.
    *   **Interaction:** Touch-optimized interactions.

3.  **Mobile (up to 767px):**
    *   **Layout:** Single-column, stacked layout. Dual-pane view becomes a tabbed or segmented control at the top, allowing users to switch between "Input" (CV/Job Ad) and "Output" (Cover Letter/Analysis).
    *   **Touch Targets:** Enlarged for easy interaction.

**Accessibility Strategy:**

**Compliance Target:** WCAG 2.1 Level AA
**Rationale:** Provides a robust and inclusive experience for the vast majority of users, aligning with international best practices and legal standards.

**Key Requirements:**
*   **Color Contrast:** Sufficient contrast for readability.
*   **Keyboard Navigation:** All interactive elements fully usable with only a keyboard.
*   **Screen Reader Support:** Proper HTML semantics and ARIA labels for screen reader understanding and navigation.
*   **Alt Text:** Descriptive alternative text for all meaningful images.
*   **Clear Focus Indicators:** Visually clear focus states for keyboard navigation.
*   **Form Labels:** Proper label associations.
*   **Error Identification:** Clear, descriptive error messages.
*   **Touch Target Size:** Adequate size for mobile interaction.

**Testing Strategy:**
*   **Automated:** Tools like Lighthouse, axe DevTools.
*   **Manual:** Keyboard-only navigation testing.
*   **Screen Reader:** Testing with common screen reader tools.


---

## 9. Implementation Guidance

### 9.1 Completion Summary

**What we created together:**

*   **Design System:** `shadcn/ui` with 2 custom components (`GapAnalysisDisplay`, `ATSScoreGauge`).
*   **Visual Foundation:** "Trustworthy Professional" color theme with a clean, sans-serif typography system and a 4px-based spacing system.
*   **Design Direction:** A hybrid approach with a "Focused Hero" landing page and a "Dual Pane" analysis view.
*   **User Journeys:** 2 critical user journeys designed with a focus on efficiency and a single-screen approach.
*   **UX Patterns:** 4 key consistency rules established for a cohesive user experience.
*   **Responsive Strategy:** 3 breakpoints with adaptation patterns for all device sizes.
*   **Accessibility:** WCAG 2.1 Level AA compliance requirements defined.

**Your Deliverables:**

*   **UX Design Document:** `docs/ux-design-specification.md`
*   **Interactive Color Themes:** `docs/ux-color-themes.html`
*   **Design Direction Mockups:** `docs/ux-design-directions.html`
*   **Key Screens Showcase:** `docs/final-app-showcase.html`

**What happens next:**

*   Designers can create high-fidelity mockups from this foundation.
*   Developers can implement with clear UX guidance and rationale.
*   All your design decisions are documented with reasoning for future reference.


---

## Appendix

### Related Documents

- Product Requirements: `docs/PRD.md`
- Product Brief: `docs/product-brief-ibe160-2025-11-04.md`
- Brainstorming: `docs/brainstorming user flows - 2025-10-29.md`

### Core Interactive Deliverables

This UX Design Specification was created through visual collaboration:

- **Color Theme Visualizer**: [ux-color-themes.html](./ux-color-themes.html)
  - Interactive HTML showing all color theme options explored
  - Live UI component examples in each theme
  - Side-by-side comparison and semantic color usage

- **Design Direction Mockups**: [ux-design-directions.html](./ux-design-directions.html)
  - Interactive HTML with 6-8 complete design approaches
  - Full-screen mockups of key screens
  - Design philosophy and rationale for each direction

### Optional Enhancement Deliverables

_This section will be populated if additional UX artifacts are generated through follow-up workflows._

<!-- Additional deliverables added here by other workflows -->

### Next Steps & Follow-Up Workflows

This UX Design Specification can serve as input to:

- **Wireframe Generation Workflow** - Create detailed wireframes from user flows
- **Figma Design Workflow** - Generate Figma files via MCP integration
- **Interactive Prototype Workflow** - Build clickable HTML prototypes
- **Component Showcase Workflow** - Create interactive component library
- **AI Frontend Prompt Workflow** - Generate prompts for v0, Lovable, Bolt, etc.
- **Solution Architecture Workflow** - Define technical architecture with UX context

### Version History

| Date     | Version | Changes                         | Author        |
| -------- | ------- | ------------------------------- | ------------- |
| 2025-11-14 | 1.0     | Initial UX Design Specification | BIP |

---

_This UX Design Specification was created through collaborative design facilitation, not template generation. All decisions were made with user input and are documented with rationale._
