from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint__returns_greeting__status_200_and_greeting_message():
    """
    Unit test: verify root endpoint returns HTML landing page with 200 status.

    Test structure (AAA pattern):
    - Arrange: Prepare test inputs (none needed for root GET)
    - Act: Make the HTTP request
    - Assert: Verify response status and content type
    """
    # ARRANGE
    # Nothing to set up in this simple example

    # ACT
    response = client.get("/")

    # ASSERT
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Facility Location" in response.text
