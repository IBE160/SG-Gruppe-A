from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from main import app
from app.models.gap import GapAnalysisResult
from app.models.result import AnalysisResultDB
import pytest

client = TestClient(app)

@patch("app.routers.analysis.supabase")
@patch("app.routers.analysis.analyze_gap")
def test_analyze_gap_endpoint(mock_analyze_gap, mock_supabase):
    # Mock AI response
    mock_analyze_gap.return_value = GapAnalysisResult(
        missing_skills=["Java"],
        missing_qualifications=[],
        match_percentage=80.0
    )

    # Mock Supabase
    mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock()

    # Mock Auth (Depends)
    # We can override the dependency
    from app.dependencies import get_current_user
    async def mock_get_current_user():
        user = MagicMock()
        user.id = "test-user-id"
        return user
    
    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.post(
        "/ai/analyze-gap",
        json={"cv_text": "Python dev", "job_description": "Need Java"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["match_percentage"] == 80.0
    assert "Java" in data["missing_skills"]
    
    # Verify DB insertion
    mock_supabase.table.assert_called_with("results")
    
    # Cleanup
    app.dependency_overrides = {}
