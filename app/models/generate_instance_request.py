"""
Generate Instance Request Model
Request model for API endpoints that generate facility location problem instances.
"""
from pydantic import BaseModel, Field


class GenerateInstanceRequest(BaseModel):
    """
    Request model for generating a new facility location problem instance.

    Attributes:
        n_customers: Number of customers to generate (must be positive)
        n_facilities: Number of facilities to generate (must be positive)
        opening_cost: Cost to open a single facility (must be positive)
    """
    n_customers: int = Field(gt=0, description="Number of customers")
    n_facilities: int = Field(gt=0, description="Number of facilities")
    opening_cost: int = Field(gt=0, description="Cost to open a single facility")