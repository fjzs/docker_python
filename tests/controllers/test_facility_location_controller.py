"""
Test suite for facility location controller API endpoints.
Tests the POST /api/generate-instance endpoint.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Fixture to provide a FastAPI test client."""
    return TestClient(app)


class TestGenerateInstanceEndpoint:
    """Test the /api/generate-instance POST endpoint."""

    def test_generate_instance__valid_request__returns_200_and_instance(self, client):
        """
        Arrange: Valid request with 10 customers and 3 facilities
        Act: POST to /api/generate-instance
        Assert: Returns 200 with FacilityLocationInstance data
        """
        # Arrange
        request_data = {
            "n_customers": 10,
            "n_facilities": 3,
        }

        # Act
        response = client.post("/api/generate-instance", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["n_customers"] == 10
        assert data["n_facilities"] == 3
        assert len(data["customers"]) == 10
        assert len(data["facilities"]) == 3

    def test_generate_instance__valid_request__returns_customers_with_coordinates(self, client):
        """
        Arrange: Valid request
        Act: POST to /api/generate-instance
        Assert: Returned customers have x and y coordinates
        """
        # Arrange
        request_data = {
            "n_customers": 5,
            "n_facilities": 2,
        }

        # Act
        response = client.post("/api/generate-instance", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        for customer in data["customers"]:
            assert "x" in customer
            assert "y" in customer
            assert 0 <= customer["x"] <= 100
            assert 0 <= customer["y"] <= 100

    def test_generate_instance__valid_request__returns_facilities_with_coordinates(self, client):
        """
        Arrange: Valid request
        Act: POST to /api/generate-instance
        Assert: Returned facilities have x and y coordinates
        """
        # Arrange
        request_data = {
            "n_customers": 5,
            "n_facilities": 2,
        }

        # Act
        response = client.post("/api/generate-instance", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        for facility in data["facilities"]:
            assert "x" in facility
            assert "y" in facility
            assert 0 <= facility["x"] <= 100
            assert 0 <= facility["y"] <= 100

    def test_generate_instance__invalid_zero_customers__returns_422(self, client):
        """
        Arrange: Request with 0 customers (invalid)
        Act: POST to /api/generate-instance
        Assert: Returns 422 Unprocessable Entity
        """
        # Arrange
        request_data = {
            "n_customers": 0,
            "n_facilities": 3,
        }

        # Act
        response = client.post("/api/generate-instance", json=request_data)

        # Assert
        assert response.status_code == 422

    def test_generate_instance__invalid_zero_facilities__returns_422(self, client):
        """
        Arrange: Request with 0 facilities (invalid)
        Act: POST to /api/generate-instance
        Assert: Returns 422 Unprocessable Entity
        """
        # Arrange
        request_data = {
            "n_customers": 10,
            "n_facilities": 0,
        }

        # Act
        response = client.post("/api/generate-instance", json=request_data)

        # Assert
        assert response.status_code == 422

    def test_generate_instance__missing_customers_field__returns_422(self, client):
        """
        Arrange: Request missing n_customers field
        Act: POST to /api/generate-instance
        Assert: Returns 422 Unprocessable Entity
        """
        # Arrange
        request_data = {
            "n_facilities": 3,
        }

        # Act
        response = client.post("/api/generate-instance", json=request_data)

        # Assert
        assert response.status_code == 422

    def test_generate_instance__large_instance__generates_correctly(self, client):
        """
        Arrange: Request with 100 customers and 20 facilities
        Act: POST to /api/generate-instance
        Assert: Returns correct counts
        """
        # Arrange
        request_data = {
            "n_customers": 100,
            "n_facilities": 20,
        }

        # Act
        response = client.post("/api/generate-instance", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["n_customers"] == 100
        assert data["n_facilities"] == 20
        assert len(data["customers"]) == 100
        assert len(data["facilities"]) == 20


class TestRootEndpoint:
    """Test the root endpoint serves the landing page."""

    def test_root_endpoint__returns_200_and_html(self, client):
        """
        Arrange: Request to root endpoint
        Act: GET /
        Assert: Returns 200 with HTML content
        """
        # Act
        response = client.get("/")

        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_root_endpoint__contains_form_inputs(self, client):
        """
        Arrange: Request to root endpoint
        Act: GET /
        Assert: HTML contains form fields for customers and facilities
        """
        # Act
        response = client.get("/")
        html_content = response.text

        # Assert
        assert "n_customers" in html_content or "customers" in html_content.lower()
        assert "n_facilities" in html_content or "facilities" in html_content.lower()

    def test_root_endpoint__contains_generate_button(self, client):
        """
        Arrange: Request to root endpoint
        Act: GET /
        Assert: HTML contains a generate button
        """
        # Act
        response = client.get("/")
        html_content = response.text.lower()

        # Assert
        assert "generate" in html_content or "submit" in html_content

