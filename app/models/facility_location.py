"""
Facility Location Problem Models

This module contains Pydantic models and business logic for the facility location
optimization problem. The problem involves:
- Customers at various locations on a 100x100 unit grid
- Facilities that can be placed on the same grid
- Goal: optimize facility placement to serve customers efficiently
"""

from pydantic import BaseModel, Field
from typing import List
import random


class Point(BaseModel):
    """
    Represents a 2D point on the grid.

    Attributes:
        x: X-coordinate (0 to 100)
        y: Y-coordinate (0 to 100)
    """
    x: float = Field(ge=0, le=100, description="X-coordinate on 100x100 grid")
    y: float = Field(ge=0, le=100, description="Y-coordinate on 100x100 grid")


class GenerateInstanceRequest(BaseModel):
    """
    Request model for generating a new facility location problem instance.

    Attributes:
        n_customers: Number of customers to generate (must be > 0)
        n_facilities: Number of facilities to generate (must be > 0)
    """
    n_customers: int = Field(gt=0, description="Number of customers")
    n_facilities: int = Field(gt=0, description="Number of facilities")


class FacilityLocationInstance(BaseModel):
    """
    Represents a complete facility location problem instance.

    Attributes:
        n_customers: Total number of customers in the instance
        n_facilities: Total number of facilities in the instance
        customers: List of customer locations as Points
        facilities: List of facility locations as Points
    """
    n_customers: int = Field(gt=0, description="Total customers in instance")
    n_facilities: int = Field(gt=0, description="Total facilities in instance")
    customers: List[Point] = Field(description="Customer locations")
    facilities: List[Point] = Field(description="Facility locations")


def generate_facility_location_instance(
    n_customers: int,
    n_facilities: int,
) -> FacilityLocationInstance:
    """
    Generate a random facility location problem instance.

    Creates random locations for customers and facilities on a 100x100 unit grid.
    All coordinates are generated uniformly at random within [0, 100].

    Args:
        n_customers: Number of customers to generate
        n_facilities: Number of facilities to generate

    Returns:
        FacilityLocationInstance: A complete problem instance with random locations

    Raises:
        ValueError: If n_customers or n_facilities <= 0

    Example:
        >>> instance = generate_facility_location_instance(10, 3)
        >>> len(instance.customers)
        10
        >>> len(instance.facilities)
        3
    """
    # Validate inputs
    if n_customers <= 0:
        raise ValueError("n_customers must be greater than 0")
    if n_facilities <= 0:
        raise ValueError("n_facilities must be greater than 0")

    # Generate random customer locations
    customers = [
        Point(x=random.uniform(0, 100), y=random.uniform(0, 100))
        for _ in range(n_customers)
    ]

    # Generate random facility locations
    facilities = [
        Point(x=random.uniform(0, 100), y=random.uniform(0, 100))
        for _ in range(n_facilities)
    ]

    # Create and return the instance
    return FacilityLocationInstance(
        n_customers=n_customers,
        n_facilities=n_facilities,
        customers=customers,
        facilities=facilities,
    )

