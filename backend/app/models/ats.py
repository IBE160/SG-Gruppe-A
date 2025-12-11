from pydantic import BaseModel, Field

class ATSScoreResult(BaseModel):
    score: int = Field(..., description="The calculated ATS compatibility score (0-100)", ge=0, le=100)
    summary: str = Field(..., description="A brief explanation of the score")
