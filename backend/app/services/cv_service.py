import shutil
import os
import uuid
import re
from datetime import datetime
from fastapi import UploadFile
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
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
        print(f"Error saving file to disk: {e}")
        raise e

    # Prepare metadata
    data = {
        "id": file_id,
        "filename": safe_filename, # Store original (sanitized) name for display
        "file_path": file_path,
        "uploaded_at": datetime.now().isoformat(),
        "user_id": user_id
    }

    # Save metadata to Supabase 'cvs' table
    try:
        response = supabase.table("cvs").insert(data).execute()
    except Exception as e:
        print(f"Error saving to DB: {e}")
        # If DB save fails, we should probably delete the uploaded file to keep state consistent
        if os.path.exists(file_path):
            os.remove(file_path)
        raise e

    return {"id": file_id, "filename": safe_filename, "message": "File uploaded successfully"}