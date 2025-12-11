from pydantic import BaseModel, Field
from typing import List

class ATSScoreResult(BaseModel):
    score: int = Field(..., description="The calculated ATS compatibility score (0-100)", ge=0, le=100)
    summary: str = Field(..., description="A brief explanation of the score")
    actionable_suggestions: List[str] = Field(..., description="List of concrete actions the user can take to improve their ATS score")
