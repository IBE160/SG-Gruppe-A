from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from app.dependencies import get_current_user
import pytest

client = TestClient(app)

# Mock user object
class MockUser:
    id = "123e4567-e89b-12d3-a456-426614174001" # Valid UUID string

# Override dependency to simulate authenticated user
# app.dependency_overrides[get_current_user] = lambda: MockUser()

import pytest
@pytest.fixture(autouse=True)
def override_auth():
    app.dependency_overrides[get_current_user] = lambda: MockUser()
    yield
    app.dependency_overrides = {}

def test_create_job_description_success():
    # Mock save_job_description service call
    with patch("app.routers.jobs.save_job_description") as mock_save:
        mock_save.return_value = {"id": "123e4567-e89b-12d3-a456-426614174000", "title": "Test Job Description"}
        
        response = client.post(
            "/api/job-description/",
            json={"content": "This is a test job description with enough characters."}
        )
        
        assert response.status_code == 200
        assert response.json()["id"] == "123e4567-e89b-12d3-a456-426614174000"
        assert response.json()["title"] == "Test Job Description"
        
        mock_save.assert_called_once_with(
                            "This is a test job description with enough characters.",
                            "123e4567-e89b-12d3-a456-426614174001"
                        )
def test_create_job_description_validation_error_min_length():
    response = client.post(
        "/api/job-description/",
                    json={"content": "abc"}    )
    
    assert response.status_code == 422 # Unprocessable Entity
    assert "content" in response.json()["detail"][0]["loc"]
    assert "at least 5 characters" in response.json()["detail"][0]["msg"]

def test_create_job_description_internal_error():
    with patch("app.routers.jobs.save_job_description") as mock_save:
        mock_save.side_effect = Exception("DB connection failed")
        
        response = client.post(
            "/api/job-description/",
            json={"content": "This is a valid job description."}
        )
        
        assert response.status_code == 500
        assert "Failed to save job description" in response.json()["detail"]
