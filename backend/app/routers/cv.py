from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from app.services.cv_service import save_cv, get_latest_cv
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/cv", tags=["cv"])

@router.post("/upload")
async def upload_cv(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):
    # Validate file type
    if file.content_type not in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only .doc and .docx are allowed."
        )
    
    # Save file and metadata
    try:
        # user object from supabase has 'id' attribute
        result = await save_cv(file, user.id)
        return result
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/latest")
async def get_latest_cv_endpoint(user = Depends(get_current_user)):
    try:
        cv = await get_latest_cv(user.id)
        if not cv:
            raise HTTPException(status_code=404, detail="No CV found")
        return cv
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))