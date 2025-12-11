import shutil
import os
import uuid
import re
from datetime import datetime
from fastapi import UploadFile
from supabase import create_client, Client
from dotenv import load_dotenv
from app.services.cv_parser import parse_cv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

url: str = os.environ.get("SUPABASE_URL")
# Use Service Role Key to bypass RLS for backend operations
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def sanitize_filename(filename: str) -> str:
    # Remove path information
    filename = os.path.basename(filename)
    # Replace anything that isn't alphanumeric, dash, dot, or underscore
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

async def save_cv(file: UploadFile, user_id: str):
    file_id = str(uuid.uuid4())
    
    safe_filename = sanitize_filename(file.filename)
    # Prefix with ID to avoid collisions
    storage_filename = f"{file_id}_{safe_filename}"
    file_path = os.path.join(UPLOAD_DIR, storage_filename)

    # Save to local disk
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Error saving file to disk: {e}", exc_info=True)
        raise e

    # Extract text from the saved file
    extracted_text = parse_cv(file_path)

    # Prepare metadata
    data = {
        "id": file_id,
        "filename": safe_filename, # Store original (sanitized) name for display
        "title": safe_filename,    # Use filename as default title to satisfy Not Null constraint
        "file_path": file_path,
        "uploaded_at": datetime.now().isoformat(),
        "user_id": user_id,
        "extracted_text": extracted_text
    }

    # Save metadata to Supabase 'cvs' table
    try:
        response = supabase.table("cvs").insert(data).execute()
    except Exception as e:
        logger.error(f"Error saving to DB: {e}", exc_info=True)
        # If DB save fails, we should probably delete the uploaded file to keep state consistent
        if os.path.exists(file_path):
            os.remove(file_path)
        raise e

async def get_latest_cv(user_id: str) -> dict:
    try:
        logger.info(f"Fetching latest CV for user_id: {user_id}")
        response = supabase.table("cvs") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("uploaded_at", desc=True) \
            .limit(1) \
            .execute()
            
        logger.info(f"Supabase response: {response}")
        
        if not response.data:
            logger.warning(f"No CV found for user_id: {user_id}")
            return None
            
        return response.data[0]
    except Exception as e:
        logger.error(f"Error fetching latest CV: {e}", exc_info=True)
        raise e