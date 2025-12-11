from pydantic import BaseModel
from typing import List, Optional

class GapAnalysisResult(BaseModel):
    missing_skills: List[str]
    missing_qualifications: List[str]
    match_percentage: float
    ats_score_summary: Optional[str] = None
    actionable_suggestions: List[str] = []
