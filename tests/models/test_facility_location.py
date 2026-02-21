"""
Test suite for facility location problem data models and generation logic.
Tests are in tests/ folder mirroring the source code structure.
"""

import pytest
from pydantic import ValidationError

from app.models.facility_location import (
    FacilityLocationInstance,
    GenerateInstanceRequest,
    generate_facility_location_instance,
    Point,
)


class TestGenerateInstanceRequest:
    """Test the API request validation model."""

    def test_valid_request(self):
        """Test that valid request data is accepted."""
        # Arrange & Act
        request = GenerateInstanceRequest(n_customers=10, n_facilities=3)

        # Assert
        assert request.n_customers == 10
        assert request.n_facilities == 3

    def test_invalid_negative_customers(self):
        """Test that negative customer count is rejected."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            GenerateInstanceRequest(n_customers=-1, n_facilities=3)

    def test_invalid_zero_customers(self):
        """Test that zero customer count is rejected."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            GenerateInstanceRequest(n_customers=0, n_facilities=3)

    def test_invalid_zero_facilities(self):
        """Test that zero facility count is rejected."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            GenerateInstanceRequest(n_customers=10, n_facilities=0)

    def test_invalid_negative_facilities(self):
        """Test that negative facility count is rejected."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            GenerateInstanceRequest(n_customers=10, n_facilities=-1)


class TestPoint:
    """Test the Point data model."""

    def test_point_within_grid(self):
        """Test that a point can be created within the 100x100 grid."""
        # Arrange & Act
        point = Point(x=50.0, y=75.5)

        # Assert
        assert point.x == 50.0
        assert point.y == 75.5

    def test_point_at_boundaries(self):
        """Test that points at grid boundaries are valid."""
        # Arrange & Act
        p1 = Point(x=0.0, y=0.0)
        p2 = Point(x=100.0, y=100.0)

        # Assert
        assert p1.x == 0.0 and p1.y == 0.0
        assert p2.x == 100.0 and p2.y == 100.0


class TestFacilityLocationInstance:
    """Test the facility location problem instance model."""

    def test_instance_structure(self):
        """Test that instance has correct structure with customers and facilities."""
        # Arrange
        customers = [Point(x=10.0, y=20.0), Point(x=30.0, y=40.0)]
        facilities = [Point(x=50.0, y=50.0)]

        # Act
        instance = FacilityLocationInstance(
            n_customers=2,
            n_facilities=1,
            customers=customers,
            facilities=facilities,
        )

        # Assert
        assert instance.n_customers == 2
        assert instance.n_facilities == 1
        assert len(instance.customers) == 2
        assert len(instance.facilities) == 1

    def test_instance_customers_count_matches(self):
        """Test that customer count matches list length."""
        # Arrange
        customers = [Point(x=i * 10, y=i * 10) for i in range(5)]
        facilities = [Point(x=50.0, y=50.0)]

        # Act
        instance = FacilityLocationInstance(
            n_customers=5,
            n_facilities=1,
            customers=customers,
            facilities=facilities,
        )

        # Assert
        assert instance.n_customers == len(instance.customers)


class TestGenerateFacilityLocationInstance:
    """Test the instance generation function."""

    def test_generate_instance_correct_counts(self):
        """Test that generated instance has correct number of customers and facilities."""
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

    def test_generate_instance_coordinates_in_grid(self):
        """Test that all generated coordinates are within the 100x100 grid."""
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

    def test_generate_instance_uniqueness(self):
        """Test that coordinates are reasonably unique (no duplicates for small instances)."""
        # Arrange
        n_customers = 5
        n_facilities = 2

        # Act
        instance = generate_facility_location_instance(n_customers, n_facilities)

        # Assert
        all_points = [(c.x, c.y) for c in instance.customers] + [(f.x, f.y) for f in instance.facilities]
        # For small samples, duplicates should be extremely rare
        assert len(all_points) == len(set(all_points)), "Duplicate coordinates found"

    def test_generate_multiple_instances_are_different(self):
        """Test that multiple generated instances are different."""
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

    def test_generate_instance_large_scale(self):
        """Test instance generation with larger numbers."""
        # Arrange
        n_customers = 100
        n_facilities = 20

        # Act
        instance = generate_facility_location_instance(n_customers, n_facilities)

        # Assert
        assert len(instance.customers) == n_customers
        assert len(instance.facilities) == n_facilities

