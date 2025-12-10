from fastapi import Header, HTTPException, status
from supabase import Client, create_client
import os
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
# Using the service role key would be better for admin tasks, but for getting user from token, 
# standard anon key + token is how client works. 
# However, here we are the backend.
# If we use the anon key, we are just a proxy.
supabase: Client = create_client(url, key)

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authentication token")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    token = authorization.split(" ")[1]
    
    try:
        # This calls Supabase Auth API to validate the JWT
        response = supabase.auth.get_user(token)
        if not response or not response.user:
             raise HTTPException(status_code=401, detail="Invalid token or user not found")
        return response.user
    except Exception as e:
        # Log the error for debug
        print(f"Auth error: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
