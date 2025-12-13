from unittest.mock import AsyncMock, MagicMock, patch
from app.services.cover_letter_generator import generate_cover_letter
from app.models.generation import CoverLetterGenerationResponse
from fastapi.testclient import TestClient
from main import app
from app.dependencies import get_current_user
import pytest

# --- Service Tests ---

@pytest.mark.asyncio
@patch("app.services.cover_letter_generator.agent")
async def test_generate_cover_letter_success(mock_agent):
    """
    Test ID: 3.1-UNIT-001
    Priority: P1
    """
    mock_result = MagicMock()
    # Mocking .output because that's what the service uses
    mock_result.output = '''
    {
        "cover_letter": "Dette er en test søknad."
    }
    '''
    mock_agent.run = AsyncMock(return_value=mock_result)

    cv_text = "CV"
    jd_text = "JD"
    
    result = await generate_cover_letter(cv_text, jd_text)

    assert isinstance(result, CoverLetterGenerationResponse)
    assert result.cover_letter == "Dette er en test søknad."

@pytest.mark.asyncio
@patch("app.services.cover_letter_generator.agent")
async def test_generate_cover_letter_json_parsing(mock_agent):
    """
    Test ID: 3.1-UNIT-002
    Priority: P1
    """
    mock_result = MagicMock()
    mock_result.output = '''
    ```json
    {
        "cover_letter": "Formatert søknad."
    }
    ```
    '''
    mock_agent.run = AsyncMock(return_value=mock_result)

    result = await generate_cover_letter("CV", "JD")
    assert result.cover_letter == "Formatert søknad."

# --- Endpoint Tests ---

client = TestClient(app)

class MockUser:
    id = "123e4567-e89b-12d3-a456-426614174001"

@pytest.fixture(name="override_auth")
def fixture_override_auth():
    app.dependency_overrides[get_current_user] = lambda: MockUser()
    yield
    app.dependency_overrides = {}

def test_generate_endpoint_success(override_auth):
    """
    Test ID: 3.1-API-001
    Priority: P1
    """
    with patch("app.routers.generation.generate_cover_letter", new_callable=AsyncMock) as mock_service:
        mock_service.return_value = CoverLetterGenerationResponse(cover_letter="Endpoint test cover letter")
        
        response = client.post("/api/v1/generation/cover-letter", json={
            "cv_text": "My CV",
            "job_description_text": "My JD"
        })
        
        assert response.status_code == 200
        assert response.json()["cover_letter"] == "Endpoint test cover letter"
        
        mock_service.assert_called_once_with("My CV", "My JD")

def test_generate_endpoint_missing_fields(override_auth):
    """
    Test ID: 3.1-API-002
    Priority: P2
    """
    response = client.post("/api/v1/generation/cover-letter", json={
        "cv_text": "Only CV"
    })
    assert response.status_code == 422 # Validation Error
