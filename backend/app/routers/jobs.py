from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.models.job import JobDescriptionIn, JobDescriptionOut
from app.models.jd import JobAnalysisResult
from app.services.job_service import save_job_description, get_latest_job_description
from app.services.jd_analyzer import analyze_job_description
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/job-description", tags=["job-description"])

@router.post("/", response_model=JobDescriptionOut)
async def create_job_description(
    job_description: JobDescriptionIn,
    user = Depends(get_current_user)
):
    try:
        result = await save_job_description(job_description.content, user.id)
        return JobDescriptionOut(id=result["id"], title=result["title"])
    except Exception as e:
        logger.error(f"Error in create_job_description endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save job description"
        )

@router.get("/latest")
async def get_latest_job_description_endpoint(user = Depends(get_current_user)):
    try:
        jd = await get_latest_job_description(user.id)
        if not jd:
            raise HTTPException(status_code=404, detail="No job description found")
        return jd
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze", response_model=JobAnalysisResult)
async def analyze_jd(
    job_description: JobDescriptionIn,
    user = Depends(get_current_user)
):
    try:
        # First save the JD? Or just analyze? 
        # The story AC implies "Given a job description has been submitted", so it might be better to analyze an existing ID.
        # But for now, let's allow analyzing raw text as per typical flow (paste -> analyze).
        # We can also save it here if needed, but let's stick to analysis for this endpoint.
        
        # Actually, story says "Given a job description has been submitted... When the analysis process is triggered".
        # This usually means we analyze the one we just saved.
        # But passing the text directly is stateless and easier. 
        # Let's assume the frontend sends the text again or we fetch it.
        # Sending text is robust.
        
        result = await analyze_job_description(job_description.content)
        return result
    except Exception as e:
        logger.error(f"Error in analyze_jd endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze job description"
        )
