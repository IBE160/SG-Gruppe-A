import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from app.services.job_service import save_job_description
from app.models.job import JobDescriptionDB
import uuid
import asyncio

# Helper to run async function
def run_async(coro):
    return asyncio.run(coro)

# To ensure the UUID is predictable for testing, we can patch uuid.uuid4()
@patch("uuid.uuid4", return_value=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"))
# To ensure datetime is predictable for testing
@patch("app.services.job_service.datetime")
def test_save_job_description_success(mock_datetime, mock_uuid4):
    # Mock datetime.now(timezone.utc)
    mock_now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = mock_now
    mock_datetime.timezone = timezone # Mock timezone attribute as well
    mock_datetime.utc = timezone.utc

    test_content = "This is a test job description."
    test_user_id = "test-user-id-123"
    expected_title = f"Job Description - {mock_now.strftime('%Y-%m-%d %H:%M')}"

    with patch("app.services.job_service.supabase") as mock_supabase:
        mock_insert = MagicMock()
        mock_execute = MagicMock()
        mock_supabase.table.return_value.insert.return_value = mock_insert
        mock_insert.execute.return_value = mock_execute
        mock_execute.data = None # Simulate Supabase returning no data on insert

        result = run_async(save_job_description(test_content, test_user_id))

        assert result["id"] == uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        assert result["title"] == expected_title

        mock_supabase.table.assert_called_with("job_descriptions")
        mock_supabase.table.return_value.insert.assert_called_once()
        
        # Verify the data sent to Supabase
        args, kwargs = mock_supabase.table.return_value.insert.call_args
        inserted_data = args[0]
        
        assert inserted_data["id"] == "123e4567-e89b-12d3-a456-426614174000"
        assert inserted_data["user_id"] == test_user_id
        assert inserted_data["title"] == expected_title
        assert inserted_data["content"] == test_content
        assert inserted_data["created_at"] == mock_now.isoformat()


@patch("uuid.uuid4", return_value=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"))
@patch("app.services.job_service.datetime")
def test_save_job_description_db_error(mock_datetime, mock_uuid4):
    mock_now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = mock_now
    mock_datetime.timezone = timezone
    mock_datetime.utc = timezone.utc

    test_content = "This is a test job description."
    test_user_id = "test-user-id-123"

    with patch("app.services.job_service.supabase") as mock_supabase:
        mock_supabase.table.return_value.insert.side_effect = Exception("DB connection error")

        with pytest.raises(Exception, match="DB connection error"):
            run_async(save_job_description(test_content, test_user_id))

        mock_supabase.table.assert_called_with("job_descriptions")
        mock_supabase.table.return_value.insert.assert_called_once()
