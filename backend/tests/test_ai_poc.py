import sys
import os
from unittest.mock import MagicMock, patch
import pytest

# Add backend to sys.path to allow importing poc.ai_test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from poc.ai_test import read_cv, check_connection, generate_cover_letter

def test_read_cv():
    # Setup mock docx
    with patch('poc.ai_test.Document') as mock_doc:
        mock_instance = MagicMock()
        mock_para = MagicMock()
        mock_para.text = "Test Content"
        mock_instance.paragraphs = [mock_para]
        mock_doc.return_value = mock_instance
        
        content = read_cv("dummy.docx")
        assert content == "Test Content"

@patch('poc.ai_test.API_KEY', 'fake_key')
@patch('poc.ai_test.Agent')
@patch('poc.ai_test.GoogleModel')
def test_check_connection_success(mock_model, mock_agent):
    # Mock successful connection
    mock_agent_instance = MagicMock()
    mock_agent_instance.run_sync.return_value.data = "Yes"
    mock_agent.return_value = mock_agent_instance
    
    assert check_connection() is True

@patch('poc.ai_test.API_KEY', None)
def test_check_connection_no_key():
    assert check_connection() is False

@patch('poc.ai_test.API_KEY', 'fake_key')
@patch('poc.ai_test.Agent')
@patch('poc.ai_test.GoogleModel')
def test_generate_cover_letter_success(mock_model, mock_agent):
    mock_agent_instance = MagicMock()
    mock_agent_instance.run_sync.return_value.output = "Dear Hiring Manager..."
    mock_agent.return_value = mock_agent_instance
    
    result = generate_cover_letter("CV", "Job")
    assert result == "Dear Hiring Manager..."
