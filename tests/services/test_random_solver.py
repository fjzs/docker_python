"""
Tests for the random solver service.
"""
from app.models import FacilityLocationInstance, FacilityLocationSolution
from app.models.point import Point
from app.services.random_solver import solve


# ── Helpers ────────────────────────────────────────────────────────────────

def make_instance(n_customers: int, n_facilities: int) -> FacilityLocationInstance:
    customers = [Point(x=i, y=i) for i in range(n_customers)]
    facilities = [Point(x=i * 10, y=i * 10) for i in range(n_facilities)]
    return FacilityLocationInstance(
        n_customers=n_customers,
        n_facilities=n_facilities,
        customers=customers,
        facilities=facilities,
    )


# ── Tests ──────────────────────────────────────────────────────────────────

def test__solve__normal_instance__returns_facility_location_solution():
    # Arrange
    instance = make_instance(n_customers=10, n_facilities=3)

    # Act
    solution = solve(instance)

    # Assert
    assert isinstance(solution, FacilityLocationSolution)


def test__solve__normal_instance__all_customers_are_assigned():
    # Arrange
    instance = make_instance(n_customers=10, n_facilities=3)

    # Act
    solution = solve(instance)

    # Assert
    assert len(solution.assignments) == instance.n_customers


def test__solve__normal_instance__all_customer_ids_are_present():
    # Arrange
    instance = make_instance(n_customers=10, n_facilities=3)

    # Act
    solution = solve(instance)

    # Assert
    assigned_ids = {a.customer_id for a in solution.assignments}
    assert assigned_ids == set(range(instance.n_customers))


def test__solve__normal_instance__assigned_facilities_are_open():
    # Arrange
    instance = make_instance(n_customers=10, n_facilities=3)

    # Act
    solution = solve(instance)

    # Assert
    open_set = set(solution.open_facilities)
    for assignment in solution.assignments:
        assert assignment.facility_id in open_set


def test__solve__normal_instance__at_least_one_facility_is_open():
    # Arrange
    instance = make_instance(n_customers=10, n_facilities=3)

    # Act
    solution = solve(instance)

    # Assert
    assert len(solution.open_facilities) >= 1


def test__solve__single_facility__all_customers_assigned_to_it():
    # Arrange
    instance = make_instance(n_customers=5, n_facilities=1)

    # Act
    solution = solve(instance)

    # Assert
    assert solution.open_facilities == [0]
    assert all(a.facility_id == 0 for a in solution.assignments)


def test__solve__single_customer__exactly_one_assignment():
    # Arrange
    instance = make_instance(n_customers=1, n_facilities=3)

    # Act
    solution = solve(instance)

    # Assert
    assert len(solution.assignments) == 1