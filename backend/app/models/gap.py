from pydantic import BaseModel
from typing import List

class GapAnalysisResult(BaseModel):
    missing_skills: List[str]
    missing_qualifications: List[str]
    match_percentage: float
