from pydantic_ai import Agent, RunContext
from app.models.jd import JobAnalysisResult
import os
from dotenv import load_dotenv
from google.generativeai import configure

load_dotenv()

# Configure Gemini
configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Define the prompt template
JD_ANALYSIS_PROMPT = """
You are an expert HR analyst. Your task is to analyze the following job description and extract three distinct lists:
1. Skills: Hard and soft skills required for the job (e.g., Python, Communication, Project Management).
2. Qualifications: Education, certifications, and experience requirements (e.g., Bachelor's degree, 5+ years of experience).
3. Keywords: Important domain-specific terms and buzzwords found in the description that would be useful for ATS optimization.

Job Description:
{job_description}

Return the result as a structured JSON object.
"""

# Initialize the agent
agent = Agent(
    'google-gla:gemini-flash-latest', # Or appropriate model
    system_prompt="You are a helpful assistant that analyzes job descriptions.",
)

async def analyze_job_description(job_description: str) -> JobAnalysisResult:
    result = await agent.run(JD_ANALYSIS_PROMPT.format(job_description=job_description), output_type=JobAnalysisResult)
    return result.output
