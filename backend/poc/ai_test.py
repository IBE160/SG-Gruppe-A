import os
import sys
from dotenv import load_dotenv
from docx import Document
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def check_connection():
    """Verify API connection (AC1)."""
    if not API_KEY or API_KEY == "change_me" or API_KEY == "your_api_key_here":
        print("❌ Error: GEMINI_API_KEY not found or invalid in .env")
        return False
    
    print(f"✅ API Key found: {API_KEY[:4]}...{API_KEY[-4:]}")
    
    try:
        # Using GoogleModel directly
        # Note: apiKey is passed via client configuration or env var 'GEMINI_API_KEY' if supported,
        # but typically GoogleModel uses 'GOOGLE_API_KEY' env var or explicit config.
        # Let's try passing it explicitly if the library allows, or setting the env var the lib expects.
        
        # Newer pydantic-ai versions often look for GOOGLE_API_KEY. 
        # We will manually set it in os.environ to be safe if we are using GEMINI_API_KEY in .env
        os.environ["GOOGLE_API_KEY"] = API_KEY
        
        model = GoogleModel('gemini-2.5-flash')
        agent = Agent(model)
        
        print("Attempting to connect to Gemini API...")
        result = agent.run_sync("Hello, are you online? Reply with 'Yes'.")
        
        response_text = result.output

        print(f"Response: {response_text}")
        if response_text is None:
             response_text = getattr(result, 'content', None) # Legacy/Alternative

        print(f"Response: {response_text}")
        
        if response_text:
            print("✅ AC1: Connection successful.")
            return True
        else:
            print("❌ AC1: Connection failed (Empty response).")
            return False
            
    except Exception as e:
        print(f"❌ AC1: Connection failed with error: {e}")
        return False

def read_cv(file_path):
    """Read content from .docx file."""
    try:
        doc = Document(file_path)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n".join(text)
    except Exception as e:
        print(f"Error reading CV: {e}")
        return None

def generate_cover_letter(cv_text, job_desc):
    """Generate cover letter using AI (AC2)."""
    if not API_KEY:
        return None
        
    try:
        os.environ["GOOGLE_API_KEY"] = API_KEY
        model = GoogleModel('gemini-2.5-flash')
        agent = Agent(model, system_prompt="You are a helpful career assistant. Generate a cover letter based on the CV and Job Description provided.")
        
        prompt = f"CV:\n{cv_text}\n\nJob Description:\n{job_desc}\n\nPlease write a cover letter."
        
        print("\nSending request to AI...")
        result = agent.run_sync(prompt)
        return result.output
    except Exception as e:
        print(f"Error generating cover letter: {e}")
        return None

def main():
    print("--- Starting AI POC ---")
    
    if not check_connection():
        print("Skipping AC2 due to connection failure.")
        # We exit with success code to allow build/test to pass in CI even if key missing, 
        # but print error. However, for 'development', we should fail.
        # But since I need to proceed to ask the user, I will exit 1.
        sys.exit(1)
        
    cv_path = "poc/sample_cv.docx"
    cv_text = read_cv(cv_path)
    
    if not cv_text:
        print("❌ Failed to read CV.")
        sys.exit(1)
    print(f"✅ Read CV ({len(cv_text)} chars)")
        
    job_desc = "We are looking for a Senior Software Engineer with Python and React experience."
    
    cover_letter = generate_cover_letter(cv_text, job_desc)
    
    if cover_letter:
        print("\n✅ AC2: Cover Letter Generated:")
        print("-" * 40)
        print(cover_letter[:500] + "...") # Print first 500 chars
        print("-" * 40)
    else:
        print("❌ AC2: Failed to generate cover letter.")
        sys.exit(1)

if __name__ == "__main__":
    main()
