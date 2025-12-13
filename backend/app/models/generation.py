from pydantic import BaseModel, Field

class CoverLetterGenerationRequest(BaseModel):
    cv_text: str = Field(..., description="The full text of the user's CV")
    job_description_text: str = Field(..., description="The full text of the job description")

class CoverLetterGenerationResponse(BaseModel):
    cover_letter: str = Field(..., description="The generated cover letter in Norwegian")
