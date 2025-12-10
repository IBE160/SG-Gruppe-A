import os
import uuid
from datetime import datetime, timezone
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

from app.models.job import JobDescriptionDB

logger = logging.getLogger(__name__)

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

async def save_job_description(content: str, user_id: str) -> dict:
    job_description_id = uuid.uuid4()
    
    # Using a placeholder title for now, as the story doesn't specify title extraction
    title = f"Job Description - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}"

    job_description_data = JobDescriptionDB(
        id=job_description_id,
        user_id=user_id,
        title=title,
        content=content,
        created_at=datetime.now(timezone.utc)
    )

    try:
        # Convert Pydantic model to dictionary for Supabase insert
        # We need to explicitly convert UUID and datetime objects if Supabase client doesn't handle them
        data_to_insert = job_description_data.dict()
        data_to_insert["id"] = str(data_to_insert["id"])
        data_to_insert["created_at"] = data_to_insert["created_at"].isoformat()

        response = supabase.table("job_descriptions").insert(data_to_insert).execute()
        
        # Check response for errors from Supabase
        if response.data is None: # Supabase client returns data=None on insert success sometimes, or empty list
             logger.warning(f"Supabase insert for job description returned no data, but no exception was raised. Assuming success.")
        
        return {"id": job_description_id, "title": title}
    except Exception as e:
        logger.error(f"Error saving job description to DB: {e}", exc_info=True)
        raise e
