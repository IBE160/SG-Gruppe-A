import pytest
from unittest.mock import patch, MagicMock
from fastapi import UploadFile
from app.services.cv_service import save_cv
from docx import Document
import os
import asyncio

# Helper to run async function
def run_async(coro):
    return asyncio.run(coro)

def test_save_cv_integration_sync(tmp_path):
    # Setup a dummy docx
    d = tmp_path / "integration_test.docx"
    doc = Document()
    doc.add_paragraph("Integration Test Content")
    doc.save(d)
    
    with open(d, "rb") as f:
        # UploadFile expects 'file' to be file-like
        upload_file = UploadFile(filename="integration_test.docx", file=f)
        
        # Mock Supabase
        with patch("app.services.cv_service.supabase") as mock_supabase:
            mock_insert = MagicMock()
            mock_execute = MagicMock()
            mock_supabase.table.return_value.insert.return_value = mock_insert
            mock_insert.execute.return_value = mock_execute
            
            # Mock UPLOAD_DIR
            with patch("app.services.cv_service.UPLOAD_DIR", str(tmp_path)):
                # Run async function
                run_async(save_cv(upload_file, "user-123"))
                
                # Check assertions
                mock_supabase.table.assert_called_with("cvs")
                
                # Check insert was called
                mock_supabase.table.return_value.insert.assert_called_once()
                
                args, _ = mock_supabase.table.return_value.insert.call_args
                data = args[0]
                
                assert "extracted_text" in data
                assert "Integration Test Content" in data["extracted_text"]
                assert data["filename"] == "integration_test.docx"
