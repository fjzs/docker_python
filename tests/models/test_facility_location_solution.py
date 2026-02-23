"""
Tests for the FacilityLocationSolution model.
"""
import pytest
from pydantic import ValidationError

from app.models.facility_location_solution import Assignment, FacilityLocationSolution


# ── Tests for Assignment ───────────────────────────────────────────────────

@pytest.mark.parametrize("customer_id, facility_id", [
    (-1, 0),   # negative customer_id
    (0, -1),   # negative facility_id
])
def test__assignment__invalid_values__raises_validation_error(customer_id, facility_id):
    # Arrange & Act & Assert
    with pytest.raises(ValidationError):
        Assignment(customer_id=customer_id, facility_id=facility_id)


def test__assignment__valid_values__creates_assignment():
    # Arrange & Act
    assignment = Assignment(customer_id=0, facility_id=2)

    # Assert
    assert assignment.customer_id == 0
    assert assignment.facility_id == 2


# ── Tests for FacilityLocationSolution ────────────────────────────────────

def test__facility_location_solution__valid_values__creates_solution():
    # Arrange & Act
    solution = FacilityLocationSolution(
        open_facilities=[0, 2],
        assignments=[Assignment(customer_id=0, facility_id=0)],
        total_transportation_cost=5.0,
        total_opening_cost=20.0,
        total_cost=25.0,
    )

    # Assert
    assert solution.open_facilities == [0, 2]
    assert len(solution.assignments) == 1
    assert solution.total_transportation_cost == 5.0
    assert solution.total_opening_cost == 20.0
    assert solution.total_cost == 25.0


@pytest.mark.parametrize("transport, opening, total", [
    (-1.0, 20.0, 19.0),   # negative transportation cost
    (5.0, -1.0, 4.0),     # negative opening cost
    (5.0, 20.0, -1.0),    # negative total cost
])
def test__facility_location_solution__negative_costs__raises_validation_error(
    transport, opening, total
):
    # Arrange & Act & Assert
    with pytest.raises(ValidationError):
        FacilityLocationSolution(
            open_facilities=[0],
            assignments=[Assignment(customer_id=0, facility_id=0)],
            total_transportation_cost=transport,
            total_opening_cost=opening,
            total_cost=total,
        )