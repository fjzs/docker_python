"""
Facility Location Problem Controller

This module contains API endpoints for the facility location optimization problem.
Routes handle instance generation and other API operations.
"""

import logging

from fastapi import APIRouter, HTTPException

from app.models.facility_location import (
    GenerateInstanceRequest,
    FacilityLocationInstance,
    generate_facility_location_instance,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["facility-location"])


@router.post("/generate-instance", response_model=FacilityLocationInstance)
def generate_instance(request: GenerateInstanceRequest) -> FacilityLocationInstance:
    """
    Generate a new facility location problem instance.

    This endpoint creates a random instance of the facility location problem
    with the specified number of customers and facilities. All locations are
    randomly placed on a 100x100 unit grid.

    Args:
        request: GenerateInstanceRequest containing n_customers and n_facilities

    Returns:
        FacilityLocationInstance: A complete problem instance with random locations

    Raises:
        HTTPException: If input validation fails (handled by Pydantic)

    Example:
        POST /api/generate-instance
        {
            "n_customers": 10,
            "n_facilities": 3
        }

        Returns:
        {
            "n_customers": 10,
            "n_facilities": 3,
            "customers": [...],
            "facilities": [...]
        }
    """
    try:
        # Call the model generator function
        instance = generate_facility_location_instance(
            n_customers=request.n_customers,
            n_facilities=request.n_facilities,
        )
        logger.info(
            f"Generated instance: {request.n_customers} customers, {request.n_facilities} facilities"
        )
        return instance
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating instance: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating instance")

