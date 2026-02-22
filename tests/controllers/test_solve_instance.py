"""
Tests for the solve instance controller.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Fixture to provide a FastAPI test client."""
    return TestClient(app)


def test__solve_instance__valid_instance__returns_200(client):
    # Arrange
    instance_data = {
        "n_customers": 10,
        "n_facilities": 3,
        "customers": [{"x": i, "y": i} for i in range(10)],
        "facilities": [{"x": i * 10, "y": i * 10} for i in range(3)],
    }

    # Act
    response = client.post("/api/solve-instance", json=instance_data)

    # Assert
    assert response.status_code == 200


def test__solve_instance__valid_instance__returns_solution_fields(client):
    # Arrange
    instance_data = {
        "n_customers": 10,
        "n_facilities": 3,
        "customers": [{"x": i, "y": i} for i in range(10)],
        "facilities": [{"x": i * 10, "y": i * 10} for i in range(3)],
    }

    # Act
    response = client.post("/api/solve-instance", json=instance_data)

    # Assert
    data = response.json()
    assert "open_facilities" in data
    assert "assignments" in data


def test__solve_instance__valid_instance__all_customers_are_assigned(client):
    # Arrange
    instance_data = {
        "n_customers": 10,
        "n_facilities": 3,
        "customers": [{"x": i, "y": i} for i in range(10)],
        "facilities": [{"x": i * 10, "y": i * 10} for i in range(3)],
    }

    # Act
    response = client.post("/api/solve-instance", json=instance_data)

    # Assert
    data = response.json()
    assert len(data["assignments"]) == 10


def test__solve_instance__missing_customers_field__returns_422(client):
    # Arrange
    instance_data = {
        "n_customers": 10,
        "n_facilities": 3,
        "facilities": [{"x": i * 10, "y": i * 10} for i in range(3)],
    }

    # Act
    response = client.post("/api/solve-instance", json=instance_data)

    # Assert
    assert response.status_code == 422


def test__solve_instance__negative_n_customers__returns_422(client):
    # Arrange
    instance_data = {
        "n_customers": -1,
        "n_facilities": 3,
        "customers": [{"x": 0, "y": 0}],
        "facilities": [{"x": i * 10, "y": i * 10} for i in range(3)],
    }

    # Act
    response = client.post("/api/solve-instance", json=instance_data)

    # Assert
    assert response.status_code == 422