from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class AnalysisResultDB(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str
    ats_score: int
    gap_summary: Dict[str, Any]
    cover_letter_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
