from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.gap_analyzer import analyze_gap
from app.models.gap import GapAnalysisResult
from app.models.result import AnalysisResultDB
from app.dependencies import get_current_user
from supabase import create_client, Client
import os
import uuid
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["analysis"])

url: str = os.environ.get("SUPABASE_URL")
# Use Service Role Key to bypass RLS for backend operations
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class AnalyzeGapRequest(BaseModel):
    cv_text: str
    job_description: str

@router.post("/analyze-gap", response_model=GapAnalysisResult)
async def analyze_gap_endpoint(
    request: AnalyzeGapRequest,
    current_user = Depends(get_current_user)
):
    logger.info(f"Received analyze-gap request from user: {current_user.id}")
    try:
        # Call AI Logic
        logger.info("Calling AI service...")
        result = await analyze_gap(request.cv_text, request.job_description)
        logger.info("AI service returned result")
        
        # Store in DB
        user_id = current_user.id
        
        result_db = AnalysisResultDB(
            id=uuid.uuid4(),
            user_id=user_id,
            ats_score=int(result.match_percentage),
            gap_summary=result.model_dump(),
            cover_letter_text=None,
            created_at=datetime.now(timezone.utc)
        )
        
        data_to_insert = result_db.model_dump()
        data_to_insert["id"] = str(data_to_insert["id"])
        data_to_insert["created_at"] = data_to_insert["created_at"].isoformat()
        
        # Insert into results table
        supabase.table("results").insert(data_to_insert).execute()
        
        return result

    except Exception as e:
        logger.error(f"Error in analyze-gap: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
