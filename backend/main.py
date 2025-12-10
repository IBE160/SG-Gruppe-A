import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
from app.routers.cv import router as cv_router
from app.routers.jobs import router as jobs_router

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app.include_router(cv_router)
app.include_router(jobs_router)

@app.get("/")
def read_root():
    return {"Hello": "World Astrid"}

@app.get("/todos")
def get_todos():
    response = supabase.table("todos").select("*").execute()
    return response.data