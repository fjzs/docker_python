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

    # Act
    instance = generate_facility_location_instance(n_customers, n_facilities)

    # Assert
    assert instance.n_customers == n_customers
    assert instance.n_facilities == n_facilities
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

    # Act
    instance = generate_facility_location_instance(n_customers, n_facilities)

    # Assert
    for customer in instance.customers:
        assert 0 <= customer.x <= 100, f"Customer x={customer.x} out of bounds"
        assert 0 <= customer.y <= 100, f"Customer y={customer.y} out of bounds"

    for facility in instance.facilities:
        assert 0 <= facility.x <= 100, f"Facility x={facility.x} out of bounds"
        assert 0 <= facility.y <= 100, f"Facility y={facility.y} out of bounds"


def test_generate_facility_location_instance__uniqueness__no_duplicate_coordinates():
    """
    Test that coordinates are reasonably unique (no duplicates for small instances).

    Arrange: Request small instance (5 customers, 2 facilities)
    Act: Generate instance
    Assert: No duplicate coordinates
    """
    # Arrange
    n_customers = 5
    n_facilities = 2

    # Act
    instance = generate_facility_location_instance(n_customers, n_facilities)

    # Assert
    all_points = [(c.x, c.y) for c in instance.customers] + [(f.x, f.y) for f in instance.facilities]
    # For small samples, duplicates should be extremely rare
    assert len(all_points) == len(set(all_points)), "Duplicate coordinates found"


def test_generate_facility_location_instance__multiple_calls__different_instances():
    """
    Test that multiple generated instances are different.

    Arrange: Same request parameters
    Act: Generate two instances
    Assert: Instances have different coordinates
    """
    # Arrange
    n_customers = 10
    n_facilities = 3

    # Act
    instance1 = generate_facility_location_instance(n_customers, n_facilities)
    instance2 = generate_facility_location_instance(n_customers, n_facilities)

    # Assert
    # Compare customer coordinates
    coords1 = [(c.x, c.y) for c in instance1.customers]
    coords2 = [(c.x, c.y) for c in instance2.customers]
    assert coords1 != coords2, "Two generated instances should be different"


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

    # Act
    instance = generate_facility_location_instance(n_customers, n_facilities)

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

    # Act
    instance = generate_facility_location_instance(n_customers, n_facilities)

    # Assert
    assert instance.n_customers == 1
    assert instance.n_facilities == 1
    assert len(instance.customers) == 1
    assert len(instance.facilities) == 1



