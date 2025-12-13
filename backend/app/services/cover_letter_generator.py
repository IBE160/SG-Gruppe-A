from pydantic_ai import Agent
from app.models.generation import CoverLetterGenerationResponse
import os
from dotenv import load_dotenv
from google.generativeai import configure
import nest_asyncio
import logging
import json

# Apply nest_asyncio
nest_asyncio.apply()

logger = logging.getLogger(__name__)

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY is not set in environment variables.")

configure(api_key=api_key)

COVER_LETTER_PROMPT = """
Du er en ekspert på karriererådgivning og jobbsøknader for det norske arbeidsmarkedet.
Din oppgave er å skrive en profesjonell, overbevisende og skreddersydd søknad (cover letter) på norsk (Bokmål).

Stillingsbeskrivelse:
{job_description}

Kandidatens CV:
{cv_text}

Instruksjoner:
1. Analyser stillingsbeskrivelsen for å identifisere nøkkelkvalifikasjoner og verdier.
2. Analyser CV-en for å finne relevant erfaring og kompetanse som matcher stillingen.
3. Skriv en søknad som fremhever hvorfor kandidaten er den rette for jobben.
4. Tonen skal være profesjonell, engasjert og høflig.
5. Unngå generiske fraser; vær spesifikk om kandidatens prestasjoner.
6. Søknaden skal være komplett med hilsen hvis passende, men fokusér på innholdet.

Output:
Returner KUN rå JSON som matcher følgende skjema. Ikke inkluder markdown-formatering.
{{
  "cover_letter": "Selve søknadsteksten her (bruk \\n for linjeskift)..."
}}
"""

agent = Agent(
    'google-gla:gemini-flash-latest',
    system_prompt="Du er en søknadsskriver-assistent. Returner kun gyldig JSON.",
)

async def generate_cover_letter(cv_text: str, job_description: str) -> CoverLetterGenerationResponse:
    logger.info("Starting Cover Letter Generation...")
    try:
        prompt = COVER_LETTER_PROMPT.format(job_description=job_description, cv_text=cv_text)
        
        result = await agent.run(prompt)
        
        # Robust JSON extraction
        clean_text = result.output.strip()
        
        # Find the first '{' and the last '}'
        start_idx = clean_text.find('{')
        end_idx = clean_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            clean_text = clean_text[start_idx:end_idx+1]
        else:
            # Fallback to simple stripping if braces not found (unlikely for valid JSON)
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

        parsed_result = CoverLetterGenerationResponse.model_validate_json(clean_text)
        
        logger.info("Cover Letter Generation completed.")
        return parsed_result
    except Exception as e:
        logger.error(f"Cover Letter Generation Failed: {e}", exc_info=True)
        raise e
