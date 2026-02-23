"""
Tests for the GenerateInstanceRequest model.
"""
import pytest
from pydantic import ValidationError

from app.models.generate_instance_request import GenerateInstanceRequest


@pytest.mark.parametrize("n_customers, n_facilities, opening_cost", [
    (-1, 3,  10),   # negative customers
    (0,  3,  10),   # zero customers
    (10, -1, 10),   # negative facilities
    (10, 0,  10),   # zero facilities
    (10, 3,  0),    # zero opening cost
    (10, 3,  -5),   # negative opening cost
])
def test__generate_instance_request__invalid_values__raises_validation_error(
    n_customers, n_facilities, opening_cost
):
    # Arrange & Act & Assert
    with pytest.raises(ValidationError):
        GenerateInstanceRequest(
            n_customers=n_customers,
            n_facilities=n_facilities,
            opening_cost=opening_cost,
        )


def test__generate_instance_request__valid_values__creates_request():
    # Arrange & Act
    request = GenerateInstanceRequest(n_customers=10, n_facilities=3, opening_cost=10)

    # Assert
    assert request.n_customers == 10
    assert request.n_facilities == 3
    assert request.opening_cost == 10