from unittest.mock import AsyncMock, MagicMock, patch
from app.services.ats_scorer import calculate_ats_score
from app.models.ats import ATSScoreResult
import pytest

@pytest.mark.asyncio
@patch("app.services.ats_scorer.agent")
async def test_calculate_ats_score_perfect_match(mock_agent):
    # Mock for perfect match
    mock_result = MagicMock()
    mock_result.output = '''
    {
        "score": 100,
        "summary": "Perfect match.",
        "actionable_suggestions": []
    }
    '''
    mock_agent.run = AsyncMock(return_value=mock_result)

    cv_text = "Perfect CV"
    jd_text = "Perfect Job"
    
    result = await calculate_ats_score(cv_text, jd_text)

    assert isinstance(result, ATSScoreResult)
    assert result.score == 100
    assert result.summary == "Perfect match."

@pytest.mark.asyncio
@patch("app.services.ats_scorer.agent")
async def test_calculate_ats_score_zero_match(mock_agent):
    # Mock for zero match
    mock_result = MagicMock()
    mock_result.output = '''
    {
        "score": 0,
        "summary": "No match found.",
        "actionable_suggestions": ["Rewrite CV completely"]
    }
    '''
    mock_agent.run = AsyncMock(return_value=mock_result)

    cv_text = "Irrelevant CV"
    jd_text = "Specific Job"
    
    result = await calculate_ats_score(cv_text, jd_text)

    assert result.score == 0
    assert result.summary == "No match found."

@pytest.mark.asyncio
@patch("app.services.ats_scorer.agent")
async def test_calculate_ats_score_json_parsing(mock_agent):
    # Mock with markdown code block
    mock_result = MagicMock()
    mock_result.output = '''
    ```json
    {
        "score": 85,
        "summary": "Good match.",
        "actionable_suggestions": ["Tweaks"]
    }
    ```
    '''
    mock_agent.run = AsyncMock(return_value=mock_result)

    result = await calculate_ats_score("cv", "jd")
    assert result.score == 85
    assert result.summary == "Good match."
