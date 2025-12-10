from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user
from app.models.job import JobDescriptionIn, JobDescriptionOut
from app.services.job_service import save_job_description
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
