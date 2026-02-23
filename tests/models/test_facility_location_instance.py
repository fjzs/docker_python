"""
Tests for the FacilityLocationInstance model.
"""
import pytest
from pydantic import ValidationError

from app.models.facility_location_instance import FacilityLocationInstance
from app.models.point import Point


# ── Helpers ────────────────────────────────────────────────────────────────

def make_instance(n_customers: int, n_facilities: int, opening_cost: int):
    customers = [Point(x=i * 10, y=i * 10) for i in range(n_customers)]
    facilities = [Point(x=i * 20, y=i * 20) for i in range(n_facilities)]
    return FacilityLocationInstance(
        n_customers=n_customers,
        n_facilities=n_facilities,
        opening_cost=opening_cost,
        customers=customers,
        facilities=facilities,
    )


# ── Tests ──────────────────────────────────────────────────────────────────

def test__facility_location_instance__valid_values__creates_instance():
    # Arrange & Act
    instance = make_instance(n_customers=2, n_facilities=1, opening_cost=10)

    # Assert
    assert instance.n_customers == 2
    assert instance.n_facilities == 1
    assert instance.opening_cost == 10
    assert len(instance.customers) == 2
    assert len(instance.facilities) == 1


def test__facility_location_instance__customer_count_matches_list_length():
    # Arrange & Act
    instance = make_instance(n_customers=5, n_facilities=1, opening_cost=10)

    # Assert
    assert instance.n_customers == len(instance.customers)


def test__facility_location_instance__facility_count_matches_list_length():
    # Arrange & Act
    instance = make_instance(n_customers=1, n_facilities=3, opening_cost=10)

    # Assert
    assert instance.n_facilities == len(instance.facilities)


@pytest.mark.parametrize("n_customers, n_facilities, opening_cost", [
    (0,  1, 10),   # zero customers
    (-1, 1, 10),   # negative customers
    (1,  0, 10),   # zero facilities
    (1, -1, 10),   # negative facilities
    (1,  1,  0),   # zero opening cost
    (1,  1, -5),   # negative opening cost
])
def test__facility_location_instance__invalid_values__raises_validation_error(
    n_customers, n_facilities, opening_cost
):
    # Arrange & Act & Assert
    with pytest.raises(ValidationError):
        make_instance(
            n_customers=n_customers,
            n_facilities=n_facilities,
            opening_cost=opening_cost,
        )