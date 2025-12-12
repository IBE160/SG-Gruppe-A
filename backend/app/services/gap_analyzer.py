from pydantic_ai import Agent
from app.models.gap import GapAnalysisResult
import os
from dotenv import load_dotenv
from google.generativeai import configure
import nest_asyncio
import logging

# Apply nest_asyncio to handle nested event loops if running in a context that requires it
nest_asyncio.apply()

logger = logging.getLogger(__name__)

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY is not set in environment variables.")

configure(api_key=api_key)

GAP_ANALYSIS_PROMPT = """
You are an expert career coach and ATS optimization specialist.
Your task is to compare a candidate's CV against a job description to identify gaps.

Job Description:
{job_description}

Candidate CV:
{cv_text}

Analyze the documents and provide:
1. A list of key skills present in the Job Description but MISSING or weak in the CV.
2. A list of specific qualifications (education, years of experience, certifications) required by the JD but not clearly met in the CV.
3. An estimated match percentage (0-100) indicating how well the CV fits the JD.

Be strict but fair. Synonyms should be considered matches (e.g., "React.js" matches "React").
"""

agent = Agent(
    'google-gla:gemini-flash-latest',
    system_prompt="You are a helpful assistant that performs gap analysis between CVs and Job Descriptions.",
)

async def analyze_gap(cv_text: str, job_description: str) -> GapAnalysisResult:
    logger.info("Starting AI Gap Analysis...")
    try:
        # Prompt explicitly asks for JSON
        prompt = GAP_ANALYSIS_PROMPT.format(job_description=job_description, cv_text=cv_text) + """

Return ONLY raw JSON matching this EXACT schema:
{
  "missing_skills": ["skill1", "skill2"],
  "missing_qualifications": ["qual1", "qual2"],
  "match_percentage": 50.0
}
"""
        
        # Run agent without result_type first, as it caused issues
        result = await agent.run(prompt)
        
        # Attempt to parse the result text as JSON into the model
        # We need to clean the response in case it has markdown code blocks
        clean_text = result.output.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        
        parsed_result = GapAnalysisResult.model_validate_json(clean_text.strip())
        
        logger.info("AI Gap Analysis completed successfully.")
        return parsed_result
    except Exception as e:
        logger.error(f"AI Gap Analysis Failed: {e}", exc_info=True)
        raise e
