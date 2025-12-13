import pytest
from app.services.ats_scorer import calculate_ats_score
from app.models.ats import ATSScoreResult

# Mock the agent run to avoid real API calls during unit tests
# In a real scenario, we might want to mock the Agent class or use a VCR cassette
# But for now, we'll try to rely on the real service if the environment is set up, 
# OR use a mock if we want to ensure isolation.
# Given the instructions often prefer integration tests or using the real AI (if keys are there),
# I'll check if I can run a simple test with mock data first.

@pytest.mark.asyncio
async def test_ats_suggestions_schema_validation():
    # This test verifies that if the AI returns the correct structure, it parses correctly.
    # We are not testing the AI itself here, but the pydantic model and parsing logic.
    
    # Mocking the AI response (conceptually)
    mock_json_response = """
    {
        "score": 85,
        "summary": "Good match but missing some key soft skills.",
        "actionable_suggestions": [
            "Add 'leadership' to your skills section.",
            "Quantify your project management experience.",
            "Include the certification 'PMP' if you have it."
        ]
    }
    """
    
    result = ATSScoreResult.model_validate_json(mock_json_response)
    
    assert result.score == 85
    assert len(result.actionable_suggestions) == 3
    assert "leadership" in result.actionable_suggestions[0]

@pytest.mark.asyncio
async def test_ats_scorer_integration_mock(monkeypatch):
    # Mock the Agent.run method to return a predefined response
    
    class MockResult:
        output = """
        {
            "score": 75,
            "summary": "Decent match.",
            "actionable_suggestions": ["Suggestion 1", "Suggestion 2"]
        }
        """
        
    class MockAgent:
        def __init__(self, model, system_prompt):
            pass
        async def run(self, prompt):
            return MockResult()

    # Apply the mock to the module
    import app.services.ats_scorer
    monkeypatch.setattr(app.services.ats_scorer, "Agent", MockAgent)
    # We also need to update the instantiated 'agent' object in the module
    app.services.ats_scorer.agent = MockAgent(None, None)

    cv_text = "Sample CV Content"
    jd_text = "Sample Job Description"
    
    result = await calculate_ats_score(cv_text, jd_text)
    
    assert isinstance(result, ATSScoreResult)
    assert result.score == 75
    assert len(result.actionable_suggestions) == 2
