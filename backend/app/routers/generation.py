from fastapi import APIRouter, HTTPException, Depends
from app.models.generation import CoverLetterGenerationRequest, CoverLetterGenerationResponse
from app.services.cover_letter_generator import generate_cover_letter
from app.dependencies import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/generation", tags=["generation"])

@router.post("/cover-letter", response_model=CoverLetterGenerationResponse)
async def generate_cover_letter_endpoint(
    request: CoverLetterGenerationRequest,
    current_user = Depends(get_current_user)
):
    logger.info(f"Received cover letter generation request from user: {current_user.id}")
    try:
        result = await generate_cover_letter(request.cv_text, request.job_description_text)
        return result
    except Exception as e:
        logger.error(f"Error in generate-cover-letter: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
