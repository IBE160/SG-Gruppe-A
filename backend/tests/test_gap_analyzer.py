from unittest.mock import AsyncMock, MagicMock, patch
from app.services.gap_analyzer import analyze_gap
from app.models.gap import GapAnalysisResult
import pytest

@pytest.mark.asyncio
@patch("app.services.gap_analyzer.agent")
async def test_analyze_gap_success(mock_agent):
    # Mock the agent's run method
    mock_result = MagicMock()
    # Return JSON string as the service parses it manually
    mock_result.output = '''
    {
        "missing_skills": ["Java"],
        "missing_qualifications": ["Master's Degree"],
        "match_percentage": 75.0
    }
    '''
    mock_agent.run = AsyncMock(return_value=mock_result)

    cv_text = "I know Python and have a Bachelor's degree."
    jd_text = "We need Python and Java, and a Master's degree."
    
    result = await analyze_gap(cv_text, jd_text)

    assert isinstance(result, GapAnalysisResult)
    assert "Java" in result.missing_skills
    assert "Master's Degree" in result.missing_qualifications
    assert result.match_percentage == 75.0
