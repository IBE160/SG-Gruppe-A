## Case Title
AI CV & Job Application Assistant

## Background
Many job seekers spend hours tailoring their CVs and cover letters without knowing how to make them stand out or pass automated screening systems. Recruiters increasingly rely on AI-based Applicant Tracking Systems (ATS) that filter applications by keywords and relevance, causing qualified candidates to be rejected before human review.

## Purpose
To create an AI-powered web application that analyzes CVs and job postings to generate optimized, personalized cover letters. The system identifies missing qualifications, suggests improvements, and helps users understand how AI evaluates applications in modern recruitment.

## Target Users
Students, graduates, and professionals who want to improve their job applications, increase their chances of passing ATS filters, and gain insight into AI-driven hiring processes.

## Core Functionality

### Must Have (MVP)
- Upload & Parsing: Users upload CVs (DOC format), and the system extracts key information.
- Job Ad Analysis: Users paste a job description, and the AI analyzes required skills and keywords.
- Cover Letter Generation: AI creates a tailored cover letter based on both the CV and job posting.
- Gap Analysis: Highlights missing qualifications or weak points compared to the job requirements.
- ATS Optimization: Rates CVs and letters based on keyword matching and basic formatting checks.

### Nice to Have (Optional Extensions)
- Tone & Style Control: Choose between formal, creative, or concise writing styles.
- Multilingual Support: Generate applications in English, Spanish, Norwegian or a different language.
- Saved Applications Dashboard: Store and compare past applications and ATS scores.
- LinkedIn Integration: Import job listings and experience directly from LinkedIn.
- Feedback Module: Allow mentors or recruiters to comment on generated applications.
- Adjusting CVs: Adjust CVs and letters for compatibility with automated systems.

## Data Requirements
- Users: name, email, encrypted password, account preferences
- CV Data: education, work experience, skills, uploaded document content
- Job Data: title, description, keywords, company name
- Generated Output: cover letter, improvement suggestions, ATS score, gap analysis summary

### Database
- Type: PostgreSQL
- Schema Overview: 
-   users (id, name, email, password_hash, created_at)
-   cv_files (id, user_id, raw_text, parsed_data, created_at)
-   job_posts (id, user_id, job_text, keywords)
-   results (id, user_id, ats_score, gap_summary, cover_letter_text)
  
## User Flows

### Flow 1: Upload CV and Job Ad → Generate Custom Cover Letter

**Entry point:**  
A new or returning user lands on the homepage.

1. **Landing page**
   - The homepage presents a brief introduction to the service — “AI Cover Letter and CV Assistant” — and a clear CTA button: “Create my cover letter.”  
   - The homepage presents a "Log in / Sign up" button for returning users and new users wanting to access other functions than the cover letter creation.
   - The button leads to the authentication flow.

2. **Login / Sign-up:**  
   - If the user already has an account, they log in using email and password.  
   - New users can register by providing a name, email, and password.  
   - Authentication is handled securely, and the user is automatically signed in.  
   - Once authenticated, the user is redirected to their personal workspace.

3. **Upload CV:**  
   - The user is prompted to upload their CV in `.doc` or `.docx` format.  
   - The system performs immediate client-side validation to ensure the correct file type.  
   - On upload, a progress indicator shows the parsing status.  
   - The file is processed, and relevant information (experience, education, skills) is extracted and stored temporarily.  
   - If the file type is invalid, an error message appears: "Please upload a .doc or .docx file.”

4. **Add Job Ad:**  
   - The user pastes the job description text or adds a link to the job posting.  
   - The system analyzes the job ad, identifying keywords, skill requirements, and tone of language.  
   - A short preview confirms that the job ad has been successfully parsed.

5. **Generate Cover Letter:**  
   - The user selects tone (Formal / Concise / Creative).  
   - After confirming inputs, the user clicks “Generate Cover Letter.”  
   - The AI model processes both the CV data and the job ad to create a tailored cover letter draft.  
   - The letter appears in a dual-view editor, showing both the generated text and key insights (e.g., how well the content matches the job ad).

6. **Review and Edit:**  
   - The user can manually edit the text directly in the editor.  
   - The interface highlights important keywords and shows where skills or experience from the CV have been referenced.  
   - The user can switch tone or regenerate the letter if needed.

7. **Finalize and Save:**  
   - The user can copy, download, or save the generated letter.  
   - Saved letters appear in the user’s personal dashboard, linked to the specific job ad and CV.  
   - A confirmation message appears: “Your cover letter has been saved to your applications.”

**Exit point:**  
The user downloads or saves the cover letter and returns to the dashboard to view or manage it later.
  
---

### Flow 2: Identify Skill Gaps and Improve CV

**Entry point:**  
The user lands on the homepage and logs in or signs up via the “Log in / Sign up” button.

1. **Login:**  
   - The user clicks “Log in / Sign up” on the homepage and enters their credentials.  
   - Once authenticated, they are redirected to their dashboard, where previous applications and CVs are listed.  
   - New users are prompted to upload a CV if none exists yet.

2. **Accessing the Analysis Tool:**  
   - The user selects “Analyze My CV” from the dashboard.  
   - They can choose an existing CV or upload a new one in `.doc` or `.docx` format.  
   - They then paste or upload a job description to compare against.

3. **Skill and Keyword Analysis:**  
   - The system reads both inputs and performs a Gap Analysis, categorizing results into:  
     - **Matched skills (green)** – already covered in the CV.  
     - **Partially matched (yellow)** – mentioned indirectly.  
     - **Missing skills (red)** – not represented in the CV at all.  
   - Each skill includes examples or context from the job ad to show where it appears.

4. **Recommendations and Edits:**  
   - The user receives AI-driven suggestions for how to strengthen weak areas.  
   - Example tips:  
     - “Add your project management certification under Experience.”  
     - “Rephrase to include the term ‘data visualization’ from the job ad.”  
   - The CV becomes editable inline, allowing quick updates without re-uploading.

5. **Re-run Analysis:**  
   - After editing, the user clicks “Re-run Analysis.”  
   - The updated ATS match score appears, showing percentage improvement (e.g., “+15% skill match”).  
   - A visual progress bar indicates how close the CV is to full alignment with the job ad.

6. **Save or Export:**  
   - The user can save the improved CV to the dashboard or download it as a `.docx` file.  
   - Each version is timestamped and linked to the job it was optimized for.

**Exit point:**  
The user leaves the analysis screen or returns to the dashboard to view the improved score and saved versions.

---

### Flow 3: Compare Applications and Track Progress

**Entry point:**  
A logged-in user navigates to the **Dashboard → Applications** section.

1. **Dashboard Overview:**  
   - The dashboard lists all saved applications, displaying the job title, company name, creation date, and ATS score.  
   - A visual graph shows the user’s progress over time, such as average ATS score and total applications created.

2. **Opening an Application:**  
   - Clicking on any entry opens a detailed summary view.  
   - The summary shows:
     - The cover letter used.  
     - Associated CV version.  
     - Job description.  
     - Last recorded ATS score.  
     - List of key missing or improved skills.

3. **Version Comparison:**  
   - The user can select two versions of the same application for side-by-side comparison.  
   - The system highlights changes such as:
     - “+12 ATS score increase.”  
     - “2 new keywords added.”  
     - “Tone adjusted to formal.”  
   - A simple toggle lets the user switch between text and analytics views.

4. **Iterative Improvement:**  
   - The user can edit and resubmit older applications for re-analysis using updated CV data or new job ads.  
   - Each re-analysis creates a new version record stored under the same job entry.  
   - The dashboard keeps a changelog for reference.

5. **Performance Overview:**  
   - A “Progress Summary” tab aggregates statistics such as:
     - Average improvement rate.  
     - Number of applications generated.  
     - Top recurring missing skills.  
   - These insights help the user identify long-term growth areas.

6. **Reuse for New Jobs:**  
   - The user can duplicate a previous application and swap out the job description.  
   - The system re-runs analysis using the new data to produce a new cover letter.

**Exit point:**  
The user leaves the dashboard or starts a new application using improved materials.

---

## Technical Constraints
- Frontend will be built with React + Next.js and styled with Tailwind CSS for responsive, modern UI
- Must require secure user authentication (login system).
- All uploaded files must be encrypted and stored safely.
- Web app must be mobile-responsive and accessible on all devices.

### AI integration:
- CV parsing: OpenAI GPT-4 with structured output or dedicated parsing library
- Job analysis: GPT-4 for keyword extraction and requirement analysis
- Cover letter generation: GPT-4 with carefully crafted prompts
- ATS scoring: Rule-based algorithm + keyword matching

### File Parsing Implementation
- **Supported format:** DOC/DOCX only  
- **Library Used:** python-docx for text extraction and structured data parsing  
- **Strategy:**  
  - Restrict uploads to .doc and .docx for consistent formatting and reliable extraction  
  - Extract key fields (education, experience, skills) and feed them into AI analysis modules  
- **Purpose:**  
  - Simplify file handling, improve accuracy, and reduce complexity compared to multi-format parsing  

## Project Timeline & Milestones
 
### Week 1: Project Setup & Design
- Choose frontend (React with next.js) and backend (python/FastAPI) stack  
- Create wireframes and basic UI  
- Initialize Git repository and authentication prototype  
 
### Week 2: File Upload & Parsing
- Implement file upload for DOC FORMAT  
- Extract and store basic CV data  
- Connect parsing logic to backend  
 
### Week 3: Job Ad Analysis
- Create job description input interface  
- Implement AI-based keyword extraction  
 
### Week 4: Cover Letter Generation
- Integrate GPT-4 for cover letter creation  
- Display generated letters in UI  
 
### Week 5: Gap Analysis & ATS Scoring
- Build keyword comparison logic  
- Add scoring and feedback display  
 
### Week 6: Testing & Deployment
- Conduct full integration testing  
- Fix bugs, polish UI 

## Testing & Quality Assurance
- Unit Tests: File parsing, API endpoints
- Integration Tests: End-to-end generation pipeline
- User Acceptance: Feedback from 3–5 pilot users
- Error Handling: User notifications for failed uploads or API issues
- Deployment: Frontend on Vercel, backend on Render or Railway, and database hosted on Supabase

## Success Criteria
- Users can generate accurate, job-specific cover letters with minimal input.
- The system identifies missing qualifications with at least 85 % accuracy.
- All user data is stored securely and accessible only to the owner.
- Application runs efficiently on both desktop and mobile platforms.
