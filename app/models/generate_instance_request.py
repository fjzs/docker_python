"""
Generate Instance Request Model

Request model for API endpoints that generate facility location problem instances.
"""

from pydantic import BaseModel, Field


class GenerateInstanceRequest(BaseModel):
    """
    Request model for generating a new facility location problem instance.

    Attributes:
        n_customers: Number of customers to generate (must be between 1 and MAX_CUSTOMERS)
        n_facilities: Number of facilities to generate (must be between 1 and MAX_FACILITIES)
    """

    MAX_CUSTOMERS: int = 100
    MAX_FACILITIES: int = 100

    n_customers: int = Field(gt=0, le=100, description="Number of customers (1-100)")
    n_facilities: int = Field(gt=0, le=100, description="Number of facilities (1-100)")