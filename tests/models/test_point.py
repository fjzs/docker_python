"""
Test suite for Point model.
"""

import pytest
from pydantic import ValidationError

from app.models.point import Point


class TestPoint:
    """Test the Point data model."""

    def test_point__valid_coordinates__creates_point(self):
        """
        Test that a point can be created within the 100x100 grid.

        Arrange: Coordinates within valid range (0-100)
        Act: Create a Point instance
        Assert: Point is created with correct coordinates
        """
        # Arrange & Act
        point = Point(x=50.0, y=75.5)

        # Assert
        assert point.x == 50.0
        assert point.y == 75.5

    def test_point__at_boundaries__creates_point(self):
        """
        Test that points at grid boundaries are valid.

        Arrange: Boundary coordinates (0 and 100)
        Act: Create Point instances at boundaries
        Assert: Points are created successfully
        """
        # Arrange & Act
        p1 = Point(x=0.0, y=0.0)
        p2 = Point(x=100.0, y=100.0)

        # Assert
        assert p1.x == 0.0 and p1.y == 0.0
        assert p2.x == 100.0 and p2.y == 100.0

    def test_point__negative_x__rejected(self):
        """Test that negative x-coordinate is rejected."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            Point(x=-1.0, y=50.0)

    def test_point__negative_y__rejected(self):
        """Test that negative y-coordinate is rejected."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            Point(x=50.0, y=-1.0)

    def test_point__x_exceeds_max__rejected(self):
        """Test that x-coordinate exceeding 100 is rejected."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            Point(x=100.1, y=50.0)

    def test_point__y_exceeds_max__rejected(self):
        """Test that y-coordinate exceeding 100 is rejected."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            Point(x=50.0, y=100.1)


    def test__distance_to__same_point__returns_zero(self):
        # Arrange
        point = Point(x=10.0, y=20.0)

        # Act
        distance = point.distance_to(point)

        # Assert
        assert distance == pytest.approx(0.0)

    def test__distance_to__horizontal_points__returns_correct_distance(self):
        # Arrange
        p1 = Point(x=0.0, y=0.0)
        p2 = Point(x=3.0, y=0.0)

        # Act
        distance = p1.distance_to(p2)

        # Assert
        assert distance == pytest.approx(3.0)

    def test__distance_to__vertical_points__returns_correct_distance(self):
        # Arrange
        p1 = Point(x=0.0, y=0.0)
        p2 = Point(x=0.0, y=4.0)

        # Act
        distance = p1.distance_to(p2)

        # Assert
        assert distance == pytest.approx(4.0)

    def test__distance_to__diagonal_points__returns_correct_distance(self):
        # Arrange
        p1 = Point(x=0.0, y=0.0)
        p2 = Point(x=3.0, y=4.0)

        # Act
        distance = p1.distance_to(p2)

        # Assert
        assert distance == pytest.approx(5.0)

    def test__distance_to__is_symmetric(self):
        # Arrange
        p1 = Point(x=10.0, y=20.0)
        p2 = Point(x=40.0, y=60.0)

        # Act & Assert
        assert p1.distance_to(p2) == pytest.approx(p2.distance_to(p1))