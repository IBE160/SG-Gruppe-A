import requests

url = "http://127.0.0.1:8000/ai/analyze-gap"
try:
    print(f"Testing {url}...")
    response = requests.post(url, json={"cv_text": "test", "job_description": "test"})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
