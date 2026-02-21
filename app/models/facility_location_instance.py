"""
Facility Location Instance Model

Represents a complete facility location problem instance with customers and facilities.
"""

from typing import List

from pydantic import BaseModel, Field

from app.models.point import Point


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

