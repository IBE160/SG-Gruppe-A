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

## User Stories (Optional)
1. As a student, I want to upload my CV and a job ad so the AI can generate a custom cover letter.
2. As a job seeker, I want to see which skills I am missing for a specific job so I can improve my CV.
3. As a returning user, I want to compare my previous applications to track my progress over time.

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
