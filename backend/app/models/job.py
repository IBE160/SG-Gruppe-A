from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class JobDescriptionIn(BaseModel):
    content: str = Field(..., min_length=5, max_length=10000) # Assuming min/max lengths

class JobDescriptionOut(BaseModel):
    id: uuid.UUID
    title: str
    message: str = "Job description saved successfully"

class JobDescriptionDB(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: str # Supabase user ID is string
    title: str = "" # Default empty as per story 2.3 notes
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
