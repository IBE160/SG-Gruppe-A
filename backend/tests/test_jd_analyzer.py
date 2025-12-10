from unittest.mock import AsyncMock, MagicMock, patch
from app.services.jd_analyzer import analyze_job_description
from app.models.jd import JobAnalysisResult
import pytest

@pytest.mark.asyncio
@patch("app.services.jd_analyzer.agent")
async def test_analyze_job_description_success(mock_agent):
    # Mock the agent's run method
    mock_result = MagicMock()
    mock_result.data = JobAnalysisResult(
        skills=["Python", "FastAPI"],
        qualifications=["Bachelor's Degree"],
        keywords=["Agile", "Scrum"]
    )
    mock_agent.run = AsyncMock(return_value=mock_result)

    jd_text = "We are looking for a Python developer with FastAPI experience and a Bachelor's degree. Must know Agile."
    result = await analyze_job_description(jd_text)

    assert isinstance(result, JobAnalysisResult)
    assert "Python" in result.skills
    assert "Bachelor's Degree" in result.qualifications
    assert "Agile" in result.keywords
