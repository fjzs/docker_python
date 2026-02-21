"""
Generate Facility Location Instance Function

Business logic for generating random facility location problem instances.
"""

import random

from app.models.facility_location_instance import FacilityLocationInstance
from app.models.point import Point


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

