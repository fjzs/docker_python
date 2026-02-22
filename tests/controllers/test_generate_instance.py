"""
Tests for the generate instance controller.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Fixture to provide a FastAPI test client."""
    return TestClient(app)


def test__generate_instance__valid_request__returns_200(client):
    # Arrange
    request_data = {"n_customers": 10, "n_facilities": 3}

    # Act
    response = client.post("/api/generate-instance", json=request_data)

    # Assert
    assert response.status_code == 200


def test__generate_instance__valid_request__returns_correct_counts(client):
    # Arrange
    request_data = {"n_customers": 10, "n_facilities": 3}

    # Act
    response = client.post("/api/generate-instance", json=request_data)

    # Assert
    data = response.json()
    assert data["n_customers"] == 10
    assert data["n_facilities"] == 3
    assert len(data["customers"]) == 10
    assert len(data["facilities"]) == 3


def test__generate_instance__valid_request__customers_have_valid_coordinates(client):
    # Arrange
    request_data = {"n_customers": 5, "n_facilities": 2}

    # Act
    response = client.post("/api/generate-instance", json=request_data)

    # Assert
    data = response.json()
    for customer in data["customers"]:
        assert "x" in customer
        assert "y" in customer
        assert 0 <= customer["x"] <= 100
        assert 0 <= customer["y"] <= 100


def test__generate_instance__valid_request__facilities_have_valid_coordinates(client):
    # Arrange
    request_data = {"n_customers": 5, "n_facilities": 2}

    # Act
    response = client.post("/api/generate-instance", json=request_data)

    # Assert
    data = response.json()
    for facility in data["facilities"]:
        assert "x" in facility
        assert "y" in facility
        assert 0 <= facility["x"] <= 100
        assert 0 <= facility["y"] <= 100


def test__generate_instance__zero_customers__returns_422(client):
    # Arrange
    request_data = {"n_customers": 0, "n_facilities": 3}

    # Act
    response = client.post("/api/generate-instance", json=request_data)

    # Assert
    assert response.status_code == 422


def test__generate_instance__zero_facilities__returns_422(client):
    # Arrange
    request_data = {"n_customers": 10, "n_facilities": 0}

    # Act
    response = client.post("/api/generate-instance", json=request_data)

    # Assert
    assert response.status_code == 422


def test__generate_instance__missing_customers_field__returns_422(client):
    # Arrange
    request_data = {"n_facilities": 3}

    # Act
    response = client.post("/api/generate-instance", json=request_data)

    # Assert
    assert response.status_code == 422