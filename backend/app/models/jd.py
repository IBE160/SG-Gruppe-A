from pydantic import BaseModel
from typing import List

class JobAnalysisResult(BaseModel):
    skills: List[str]
    qualifications: List[str]
    keywords: List[str]
