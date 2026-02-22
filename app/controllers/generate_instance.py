"""
Generate Instance Controller
Handles the API endpoint for generating a facility location problem instance.
"""
import logging

from fastapi import APIRouter, HTTPException

from app.models import FacilityLocationInstance, GenerateInstanceRequest
from app.models import generate_facility_location_instance

logger = logging.getLogger(__name__)

# APIRouter groups related endpoints and attaches them to the main app via
# app.include_router() in main.py. The prefix applies to all routes in this
# file, so @router.post("/generate-instance") becomes POST /api/generate-instance.
# tags controls how endpoints are grouped in the Swagger UI at /docs.
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
        instance = generate_facility_location_instance(
            n_customers=request.n_customers,
            n_facilities=request.n_facilities,
        )
        logger.info(
            f"Generated instance: {request.n_customers} customers, "
            f"{request.n_facilities} facilities"
        )
        return instance
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating instance: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating instance")