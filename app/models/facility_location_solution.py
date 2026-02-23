"""
Facility Location Solution Model
Represents a solution to a facility location problem instance.
"""
from typing import List

from pydantic import BaseModel, Field


class Assignment(BaseModel):
    """
    Represents the assignment of a single customer to a facility.

    Attributes:
        customer_id: Index of the customer in the instance customers list
        facility_id: Index of the facility in the instance facilities list
    """
    customer_id: int = Field(ge=0, description="Index of the customer")
    facility_id: int = Field(ge=0, description="Index of the assigned facility")


class FacilityLocationSolution(BaseModel):
    """
    Represents a complete solution to a facility location problem instance.

    Attributes:
        open_facilities: List of indices of open facilities
        assignments: List of customer-to-facility assignments
        total_transportation_cost: Sum of Euclidean distances from each customer to its facility
        total_opening_cost: Sum of opening costs for all open facilities
        total_cost: Sum of transportation and opening costs
    """
    open_facilities: List[int] = Field(description="Indices of open facilities")
    assignments: List[Assignment] = Field(description="Customer-facility assignments")
    total_transportation_cost: float = Field(ge=0, description="Sum of Euclidean distances")
    total_opening_cost: float = Field(ge=0, description="Sum of opening costs for open facilities")
    total_cost: float = Field(ge=0, description="Total transportation and opening cost")