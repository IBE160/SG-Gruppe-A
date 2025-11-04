# Brainstorming Session Results: AI CV & Job Application Assistant User Flows

**Date:** October 29, 2025
**Project:** ibe160 - AI CV & Job Application Assistant
**Focus:** User Flows and Potential Deviations

## 1. Main User Flows Identified

The core user flows for the "AI CV & Job Application Assistant" were identified and detailed:

*   **Uploading CV:** User uploads CV (DOC/DOCX), system validates, parses, and stores data.
*   **Job Ad Analysis:** User provides job description, AI extracts keywords and requirements.
*   **Cover Letter Generation:** AI crafts personalized cover letter based on CV and job ad, user can edit.
*   **Gap Analysis:** System compares CV and job ad, highlights missing skills, and provides recommendations.
*   **ATS Scoring and Optimization:** AI rates CV/cover letter alignment with job ad and suggests improvements.

## 2. Detailed Deviations (Categorized)

## 2.1. Five Whys Analysis

**Deviation Investigated:** AI produces a draft that doesn’t meet the user’s expectations (too generic, too long, or wrong tone).

1.  **Why does the AI produce a draft that doesn’t meet the user’s expectations (too generic, too long, or wrong tone)?**
    *   Because it is too long and has the wrong tone.
2.  **Why is it too long and has the wrong tone?**
    *   Because it has too many words.
3.  **Why does it have too many words?**
    *   Because the AI thinks it's necessary.
4.  **Why does the AI "think it's necessary" to generate too many words or an inappropriate tone, even when it doesn't meet user expectations?**
    *   Because it doesn't understand the task.
5.  **Why does the AI not understand the task of generating a cover letter that meets user expectations regarding length and tone?**
    *   Because it has been updated a long time ago.

**Root Cause:** The AI model used for cover letter generation is outdated and has not been recently updated or fine-tuned to meet current user expectations for length and tone.

We explored potential deviations and unexpected scenarios within each flow, grouped into the following categories:

### 1. User Input/Behavior Issues

*   **Uploading CV:**
    *   Users uploading the wrong file type (PDF or image).
    *   System may ask whether to replace or save a new version (multiple CVs).
*   **Job Ad Analysis:**
    *   User provides a poorly written or incomplete job description.
    *   User might paste text containing formatting errors, links, or unrelated content.
    *   Users might paste duplicate ads or change the job description midway.
*   **Cover Letter Generation:**
    *   User may repeatedly regenerate the letter or manually edit sections.
    *   Users might skip tone selection altogether or close the editor before saving their letter.
*   **Gap Analysis:**
    *   Some users might only review the results briefly without making changes.
    *   Others may over-edit their CV based on suggestions, potentially reducing clarity or coherence.
    *   Users might exit the process early, forgetting to save their progress.
    *   Rerun the analysis multiple times expecting different results without significantly updating their CV content.
*   **ATS Scoring and Optimization:**
    *   Some may ignore optimization suggestions altogether.
    *   Others might over-optimize by stuffing keywords unnaturally.
    *   Users might rerun the optimization repeatedly without making meaningful changes.
    *   Close the app before saving improvements.

### 2. System/Technical Limitations

*   **Uploading CV:**
    *   CV might be corrupted, empty, or poorly formatted, causing incomplete or inaccurate data extraction.
    *   Uploads could fail due to slow internet or large files.
*   **Job Ad Analysis:**
    *   Internet or API issues could cause the analysis to fail.
*   **Cover Letter Generation:**
    *   Technical issues like API timeouts or token limits could interrupt the generation process.
*   **Gap Analysis:**
    *   Technical issues could arise if certain keywords aren’t detected correctly.
*   **ATS Scoring and Optimization:**
    *   Technical issues, such as delayed score updates or API errors.

### 3. AI Accuracy/Expectation Mismatch

*   **Uploading CV:**
    *   If the parser cannot extract information accurately, the system should prompt the user to review or manually correct the extracted data.
*   **Cover Letter Generation:**
    *   AI produces a draft that doesn’t meet the user’s expectations (too generic, too long, or wrong tone).
    *   If the job ad or CV data is incomplete, the AI’s output may be less accurate.
*   **Gap Analysis:**
    *   Users disagree with the AI’s assessment or feel the results are inaccurate.
*   **ATS Scoring and Optimization:**
    *   Users misunderstand or overreact to a low score, becoming frustrated or distrusting the system’s accuracy.

### 4. User Education/Guidance Needs

*   **Job Ad Analysis:**
    *   If the job description is too short or vague, the system may prompt the user to add more details or verify the input.
*   **ATS Scoring and Optimization:**
    *   Users misunderstand or overreact to a low score, becoming frustrated or distrusting the system’s accuracy.

## 3. Key Insights and Themes

*   **User Guidance and Feedback:** A consistent need for clear instructions, proactive validation messages, and effective feedback mechanisms to guide users and prevent common errors.
*   **AI Accuracy and Robustness:** The quality and reliability of AI outputs (parsing, generation, analysis) are crucial, as inaccuracies lead to user frustration and distrust.
*   **Error Handling and Recovery:** Robust mechanisms for handling technical issues, user mistakes, and providing clear paths for recovery (retries, manual corrections, autosave) are essential.
*   **User Control and Customization:** Users desire the ability to refine, edit, and customize AI-generated content, indicating a need for a balance between automation and user agency.
*   **Proactive Design is Key:** Many potential deviations can be prevented or significantly mitigated through thoughtful UI/UX design that anticipates user behavior and provides clear guidance upfront.
*   **Trust Through Transparency:** For AI-driven features, explaining *why* certain suggestions are made or scores are given will be vital for building user trust and encouraging adoption.
*   **Iterative Improvement for AI:** The AI models will require continuous monitoring and refinement, especially in areas like cover letter generation and gap analysis, to meet diverse user expectations.
*   **Strong Link between User Input/Behavior and Education:** Addressing user education can significantly reduce user behavior issues.
*   **AI Accuracy Impacts Trust:** AI Accuracy/Expectation Mismatch directly affects user engagement and trust in key features.

## 4. Action Plan

**Priority 1: Adding simple error messages for failed actions.**
*   **Why Priority:** Easy to implement, immediately enhances user experience, prevents confusion/frustration.
*   **Concrete Next Steps:** Identify common failure points (upload errors, failed AI generations, connection issues). Design clear, user-friendly error message templates with short explanations and retry options. Implement these messages in the frontend and ensure real-time appearance.
*   **Resource Needs:** 1 Frontend developer, 1 UI/UX designer, (Optional) QA tester.
*   **Realistic Timeline:** 3–4 days.

**Priority 2: Improving the clarity of AI-generated results so users better understand them.**
*   **Why Priority:** Easy to implement, immediately enhances user experience, prevents confusion/frustration.
*   **Concrete Next Steps:** Add short explanations or highlights showing how the AI generated results and what key factors influenced them.
*   **Resource Needs:** 1 AI prompt engineer, 1 Frontend developer.
*   **Realistic Timeline:** 4–5 days.

**Priority 3: Creating short tooltips or guides that explain each feature.**
*   **Why Priority:** Easy to implement, immediately enhances user experience, prevents confusion/frustration.
*   **Concrete Next Steps:** Identify key features needing clarification, write short tooltip text, and integrate them into the interface.
*   **Resource Needs:** 1 UX writer, 1 Frontend developer.
*   **Realistic Timeline:** 2–3 days.

**Priority 4: Update and fine-tune AI model for cover letter generation.**
*   **Why Priority:** Addresses the root cause of AI output not meeting user expectations regarding length and tone, directly impacting core functionality and user satisfaction.
*   **Concrete Next Steps:** Research latest AI models/techniques for text generation. Fine-tune the chosen model with specific data and instructions for cover letter length, tone, and content. Implement and test the updated model.
*   **Resource Needs:** 1 AI/ML Engineer, 1 Prompt Engineer, 1 QA Tester.
*   **Realistic Timeline:** 2-3 weeks (depending on complexity of fine-tuning).

## 5. Session Reflection

*   **What worked well:** The structured step-by-step approach helped organize ideas clearly, and grouping deviations by category made it easier to identify priorities. The short paragraph reflections also kept the discussion focused and productive.
*   **Areas to explore further:** Future sessions could look deeper into user feedback mechanisms and how AI-generated content can adapt to different job industries or formats.
*   **Follow-up techniques:** A short usability test or mock user walkthrough could help validate our ideas before implementation. Using a visual mind map or flowchart tool could also make relationships between features clearer.
*   **Emergent questions:** How can we measure user satisfaction with AI outputs, and what metrics will define a “successful” user experience?
*   **Next session planning:** In the next session, we could brainstorm the user feedback and evaluation system—how to collect, analyze, and use user insights to continuously improve the AI assistant.

---
_Status Version: 2.0_
