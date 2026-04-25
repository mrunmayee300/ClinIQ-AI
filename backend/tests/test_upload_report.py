from io import BytesIO

from fastapi.testclient import TestClient

from main import app


def test_upload_report_rejects_invalid_content_type() -> None:
    client = TestClient(app)
    file_obj = BytesIO(b"fake image bytes")
    response = client.post(
        "/api/v1/upload-report",
        files={"file": ("report.png", file_obj, "image/png")},
    )
    assert response.status_code == 400
    assert "Only PDF or plain text files are allowed." in response.json()["detail"]
