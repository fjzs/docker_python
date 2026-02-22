from app.models.facility_location_instance import FacilityLocationInstance
from app.models.point import Point
from app.services.simple_solver import solve_random


def test_solve_random_returns_valid_structure():
    # Arrange
    instance = FacilityLocationInstance(
        n_customers=2,
        n_facilities=2,
        customers=[Point(x=10, y=10), Point(x=20, y=20)],
        facilities=[Point(x=0, y=0), Point(x=100, y=100)],
    )

    # Act
    solution = solve_random(instance)

    # Assert
    assert "status" in solution
    assert "open_facilities" in solution
    assert "assignments" in solution
    assert "solve_time" in solution

    assert len(solution["assignments"]) == 2