"""
Test suite for generate_facility_location_instance function.

Tests the generator function which creates random facility location problem instances.
"""

from app.models.generator import generate_facility_location_instance


def test_generate_facility_location_instance__valid_input__correct_counts():
    """
    Test that generated instance has correct number of customers and facilities.

    Arrange: Request 15 customers and 4 facilities
    Act: Generate instance
    Assert: Counts match requested amounts
    """
    # Arrange
    n_customers = 15
    n_facilities = 4
    opening_cost = 10

    # Act
    instance = generate_facility_location_instance(n_customers, n_facilities, opening_cost)

    # Assert
    assert instance.n_customers == n_customers
    assert instance.n_facilities == n_facilities
    assert instance.opening_cost == opening_cost
    assert len(instance.customers) == n_customers
    assert len(instance.facilities) == n_facilities


def test_generate_facility_location_instance__coordinates_in_grid__all_coordinates_valid():
    """
    Test that all generated coordinates are within the 100x100 grid.

    Arrange: Request instance generation
    Act: Generate 10 customers and 3 facilities
    Assert: All coordinates within [0, 100] range
    """
    # Arrange
    n_customers = 10
    n_facilities = 3
    opening_cost = 10

    # Act
    instance = generate_facility_location_instance(n_customers, n_facilities, opening_cost)

    # Assert
    for customer in instance.customers:
        assert 0 <= customer.x <= 100, f"Customer x={customer.x} out of bounds"
        assert 0 <= customer.y <= 100, f"Customer y={customer.y} out of bounds"

    for facility in instance.facilities:
        assert 0 <= facility.x <= 100, f"Facility x={facility.x} out of bounds"
        assert 0 <= facility.y <= 100, f"Facility y={facility.y} out of bounds"


def test_generate_facility_location_instance__large_scale__generates_correct_counts():
    """
    Test instance generation with larger numbers.

    Arrange: Request 100 customers and 20 facilities
    Act: Generate instance
    Assert: Correct counts are generated
    """
    # Arrange
    n_customers = 100
    n_facilities = 20
    opening_cost = 10

    # Act
    instance = generate_facility_location_instance(n_customers, n_facilities, opening_cost)

    # Assert
    assert len(instance.customers) == n_customers
    assert len(instance.facilities) == n_facilities


def test_generate_facility_location_instance__minimum_size__creates_instance():
    """
    Test instance generation with minimum valid size.

    Arrange: Request 1 customer and 1 facility
    Act: Generate instance
    Assert: Instance is created successfully
    """
    # Arrange
    n_customers = 1
    n_facilities = 1
    opening_cost = 10

    # Act
    instance = generate_facility_location_instance(n_customers, n_facilities, opening_cost)

    # Assert
    assert instance.n_customers == 1
    assert instance.n_facilities == 1
    assert len(instance.customers) == 1
    assert len(instance.facilities) == 1



