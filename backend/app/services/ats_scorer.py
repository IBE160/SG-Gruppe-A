from pydantic_ai import Agent
from app.models.ats import ATSScoreResult
import os
from dotenv import load_dotenv
from google.generativeai import configure
import nest_asyncio
import logging
import json

# Apply nest_asyncio to handle nested event loops if running in a context that requires it
nest_asyncio.apply()

logger = logging.getLogger(__name__)

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY is not set in environment variables.")

configure(api_key=api_key)

ATS_SCORING_PROMPT = """
You are an expert ATS (Applicant Tracking System) algorithm.
Your task is to calculate a compatibility score (0-100) between a candidate's CV and a Job Description, and provide actionable suggestions for improvement.

Job Description:
{job_description}

Candidate CV:
{cv_text}

Scoring Criteria:
1. Keyword Matching (40%): Presence of specific keywords and industry terminology from the JD in the CV.
2. Skills Matching (30%): Match between required hard/soft skills and those listed in the CV.
3. Experience Relevance (20%): Relevance of past job titles, responsibilities, and years of experience.
4. Education & Certifications (10%): Alignment with educational requirements and certifications.

Output:
Provide the final calculated score as an integer (0-100), a brief one-sentence summary explaining the main factor influencing the score, and a list of 3-5 specific, actionable suggestions for the candidate to improve their CV for this specific job.
Return ONLY raw JSON matching the ATSScoreResult schema. Do not include markdown formatting (like ```json).
Schema:
{{
  "score": integer,
  "summary": string,
  "actionable_suggestions": [string]
}}
"""

agent = Agent(
    'google-gla:gemini-flash-latest',
    system_prompt="You are a strict ATS scoring engine. Return valid JSON only.",
)

async def calculate_ats_score(cv_text: str, job_description: str) -> ATSScoreResult:
    logger.info("Starting ATS Score Calculation...")
    try:
        # Prompt explicitly asks for JSON
        prompt = ATS_SCORING_PROMPT.format(job_description=job_description, cv_text=cv_text)
        
        # Run agent
        result = await agent.run(prompt)
        
        # Attempt to parse the result text as JSON into the model
        clean_text = result.output.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        
        clean_text = clean_text.strip()
        
        try:
             # Validate JSON before passing to model
             json.loads(clean_text)
        except json.JSONDecodeError as e:
             logger.error(f"Invalid JSON returned from AI: {clean_text}")
             raise ValueError(f"AI returned invalid JSON: {e}")

        parsed_result = ATSScoreResult.model_validate_json(clean_text)
        
        logger.info(f"ATS Score Calculation completed: {parsed_result.score}")
        return parsed_result
    except Exception as e:
        logger.error(f"ATS Score Calculation Failed: {e}", exc_info=True)
        # Return a fallback/error result or raise
        raise e
