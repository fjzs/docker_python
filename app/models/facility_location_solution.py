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
    """
    open_facilities: List[int] = Field(description="Indices of open facilities")
    assignments: List[Assignment] = Field(description="Customer-facility assignments")