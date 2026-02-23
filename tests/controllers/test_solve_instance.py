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


@pytest.fixture
def valid_instance_data():
    """Fixture providing a valid facility location instance payload."""
    return {
        "n_customers": 10,
        "n_facilities": 3,
        "opening_cost": 10,
        "customers": [{"x": i, "y": i} for i in range(10)],
        "facilities": [{"x": i * 10, "y": i * 10} for i in range(3)],
    }


# ── /api/solve-instance-randomly ──────────────────────────────────────────

def test__solve_instance_randomly__valid_instance__returns_200(client, valid_instance_data):
    # Arrange & Act
    response = client.post("/api/solve-instance-randomly", json=valid_instance_data)

    # Assert
    assert response.status_code == 200


def test__solve_instance_randomly__valid_instance__returns_solution_fields(client, valid_instance_data):
    # Arrange & Act
    response = client.post("/api/solve-instance-randomly", json=valid_instance_data)

    # Assert
    data = response.json()
    assert "open_facilities" in data
    assert "assignments" in data


def test__solve_instance_randomly__valid_instance__all_customers_are_assigned(client, valid_instance_data):
    # Arrange & Act
    response = client.post("/api/solve-instance-randomly", json=valid_instance_data)

    # Assert
    data = response.json()
    assert len(data["assignments"]) == 10


def test__solve_instance_randomly__missing_customers_field__returns_422(client):
    # Arrange
    instance_data = {
        "n_customers": 10,
        "n_facilities": 3,
        "opening_cost": 10,
        "facilities": [{"x": i * 10, "y": i * 10} for i in range(3)],
    }

    # Act
    response = client.post("/api/solve-instance-randomly", json=instance_data)

    # Assert
    assert response.status_code == 422


def test__solve_instance_randomly__negative_n_customers__returns_422(client):
    # Arrange
    instance_data = {
        "n_customers": -1,
        "n_facilities": 3,
        "opening_cost": 10,
        "customers": [{"x": 0, "y": 0}],
        "facilities": [{"x": i * 10, "y": i * 10} for i in range(3)],
    }

    # Act
    response = client.post("/api/solve-instance-randomly", json=instance_data)

    # Assert
    assert response.status_code == 422


# ── /api/solve-instance-optimally ─────────────────────────────────────────

def test__solve_instance_optimally__valid_instance__returns_200(client, valid_instance_data):
    # Arrange & Act
    response = client.post("/api/solve-instance-optimally", json=valid_instance_data)

    # Assert
    assert response.status_code == 200


def test__solve_instance_optimally__valid_instance__returns_solution_fields(client, valid_instance_data):
    # Arrange & Act
    response = client.post("/api/solve-instance-optimally", json=valid_instance_data)

    # Assert
    data = response.json()
    assert "open_facilities" in data
    assert "assignments" in data


def test__solve_instance_optimally__valid_instance__all_customers_are_assigned(client, valid_instance_data):
    # Arrange & Act
    response = client.post("/api/solve-instance-optimally", json=valid_instance_data)

    # Assert
    data = response.json()
    assert len(data["assignments"]) == 10


def test__solve_instance_optimally__missing_customers_field__returns_422(client):
    # Arrange
    instance_data = {
        "n_customers": 10,
        "n_facilities": 3,
        "opening_cost": 10,
        "facilities": [{"x": i * 10, "y": i * 10} for i in range(3)],
    }

    # Act
    response = client.post("/api/solve-instance-optimally", json=instance_data)

    # Assert
    assert response.status_code == 422


def test__solve_instance_optimally__negative_n_customers__returns_422(client):
    # Arrange
    instance_data = {
        "n_customers": -1,
        "n_facilities": 3,
        "opening_cost": 10,
        "customers": [{"x": 0, "y": 0}],
        "facilities": [{"x": i * 10, "y": i * 10} for i in range(3)],
    }

    # Act
    response = client.post("/api/solve-instance-optimally", json=instance_data)

    # Assert
    assert response.status_code == 422