from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from app.dependencies import get_current_user

client = TestClient(app)

# Mock user object
class MockUser:
    id = "test-user-id"

# Override dependency
app.dependency_overrides[get_current_user] = lambda: MockUser()

def test_upload_cv_success():
    # Mock save_cv to avoid hitting DB and FS
    with patch("app.routers.cv.save_cv") as mock_save:
        mock_save.return_value = {"id": "123", "filename": "test.docx", "message": "File uploaded successfully"}
        
        file_content = b"fake doc content"
        files = {"file": ("test.docx", file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        
        response = client.post("/api/cv/upload", files=files)
        
        assert response.status_code == 200
        assert response.json()["id"] == "123"
        
        # Check arguments passed to save_cv
        mock_save.assert_called_once()
        args, _ = mock_save.call_args
        uploaded_file = args[0]
        user_id = args[1]
        
        assert uploaded_file.filename == "test.docx"
        assert user_id == "test-user-id"

def test_upload_invalid_file_type():
    file_content = b"fake pdf content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}
    response = client.post("/api/cv/upload", files=files)
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

def test_upload_no_file():
    response = client.post("/api/cv/upload")
    assert response.status_code == 422  # Validation error for missing field
