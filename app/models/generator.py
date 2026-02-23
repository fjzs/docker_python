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
    opening_cost: int,
) -> FacilityLocationInstance:
    """
    Generate a random facility location problem instance.

    Creates random locations for customers and facilities on a 100x100 unit grid.
    All coordinates are generated uniformly at random within [0, 100].

    Args:
        n_customers: Number of customers to generate
        n_facilities: Number of facilities to generate
        opening_cost: Cost to open a single facility

    Returns:
        FacilityLocationInstance: A complete problem instance with random locations

    Example:
        >>> instance = generate_facility_location_instance(10, 3, 10)
        >>> len(instance.customers)
        10
        >>> len(instance.facilities)
        3
    """
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

    return FacilityLocationInstance(
        n_customers=n_customers,
        n_facilities=n_facilities,
        opening_cost=opening_cost,
        customers=customers,
        facilities=facilities,
    )