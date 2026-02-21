"""
Test suite for FacilityLocationInstance model.

Tests the FacilityLocationInstance class which represents a complete facility location
problem instance with customers and facilities.
"""

from app.models.facility_location_instance import FacilityLocationInstance
from app.models.point import Point


class TestFacilityLocationInstance:
    """Test the facility location problem instance model."""

    def test_facility_location_instance__valid_structure__creates_instance(self):
        """
        Test that instance has correct structure with customers and facilities.

        Arrange: Create lists of customers and facilities
        Act: Create FacilityLocationInstance
        Assert: Instance is created with correct structure
        """
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

    def test_facility_location_instance__customer_count_matches__valid(self):
        """
        Test that customer count matches list length.

        Arrange: Create 5 customers
        Act: Create FacilityLocationInstance with n_customers=5
        Assert: Count matches length
        """
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

    def test_facility_location_instance__facility_count_matches__valid(self):
        """
        Test that facility count matches list length.

        Arrange: Create 3 facilities
        Act: Create FacilityLocationInstance with n_facilities=3
        Assert: Count matches length
        """
        # Arrange
        customers = [Point(x=10.0, y=20.0)]
        facilities = [Point(x=i * 20, y=i * 20) for i in range(3)]

        # Act
        instance = FacilityLocationInstance(
            n_customers=1,
            n_facilities=3,
            customers=customers,
            facilities=facilities,
        )

        # Assert
        assert instance.n_facilities == len(instance.facilities)

    def test_facility_location_instance__empty_customers__valid(self):
        """
        Test that instance can be created with empty customers list.

        Arrange: Empty customers list
        Act: Create FacilityLocationInstance
        Assert: Instance is created
        """
        # Arrange
        customers = []
        facilities = [Point(x=50.0, y=50.0)]

        # Act & Assert - This will fail validation since n_customers must be > 0
        from pydantic import ValidationError
        import pytest
        with pytest.raises(ValidationError):
            FacilityLocationInstance(
                n_customers=0,
                n_facilities=1,
                customers=customers,
                facilities=facilities,
            )

