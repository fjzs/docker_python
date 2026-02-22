"""
Solve Instance Controller
Handles the API endpoint for solving a facility location problem instance.
"""
import logging

from fastapi import APIRouter, HTTPException

from app.models import FacilityLocationInstance, FacilityLocationSolution
from app.services.random_solver import solve

logger = logging.getLogger(__name__)

# APIRouter groups related endpoints and attaches them to the main app via
# app.include_router() in main.py. The prefix applies to all routes in this
# file, so @router.post("/solve-instance") becomes POST /api/solve-instance.
# tags controls how endpoints are grouped in the Swagger UI at /docs.
router = APIRouter(prefix="/api", tags=["facility-location"])


@router.post("/solve-instance", response_model=FacilityLocationSolution)
def solve_instance(instance: FacilityLocationInstance) -> FacilityLocationSolution:
    """
    Solve a facility location problem instance.

    Args:
        instance: A complete facility location problem instance

    Returns:
        FacilityLocationSolution: A feasible solution

    Raises:
        HTTPException: If input validation fails (handled by Pydantic)

    Example:
        POST /api/solve-instance
        {
            "n_customers": 10,
            "n_facilities": 3,
            "customers": [...],
            "facilities": [...]
        }
        Returns:
        {
            "open_facilities": [0, 2],
            "assignments": [...]
        }
    """
    try:
        solution = solve(instance)
        logger.info(
            f"Solved instance: {instance.n_customers} customers, "
            f"{instance.n_facilities} facilities"
        )
        return solution
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error solving instance: {str(e)}")
        raise HTTPException(status_code=500, detail="Error solving instance")