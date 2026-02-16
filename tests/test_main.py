from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint__returns_greeting__status_200_and_greeting_message():
    """Unit test: verify root endpoint returns greeting message with 200 status."""
    # ARRANGE
    # Nothing to set up in this simple example

    # ACT
    response = client.get("/")

    # ASSERT
    assert response.status_code == 200
    assert response.json() == {"greeting": "Hello, World!"}
