"""
Solve Instance Controller
Handles the API endpoints for solving a facility location problem instance.
"""
import logging

from fastapi import APIRouter, HTTPException

from app.models import FacilityLocationInstance, FacilityLocationSolution
from app.services import optimal_solver, random_solver

logger = logging.getLogger(__name__)

# APIRouter groups related endpoints and attaches them to the main app via
# app.include_router() in main.py. The prefix applies to all routes in this
# file, so @router.post("/solve-instance") becomes POST /api/solve-instance.
# tags controls how endpoints are grouped in the Swagger UI at /docs.
router = APIRouter(prefix="/api", tags=["facility-location"])


def _solve(instance: FacilityLocationInstance, solver) -> FacilityLocationSolution:
    """
    Runs the given solver on the instance and wraps errors as HTTPExceptions.

    Args:
        instance: A complete facility location problem instance.
        solver: A module with a solve(instance) function.

    Returns:
        FacilityLocationSolution: The computed solution.

    Raises:
        HTTPException: 400 if input is invalid, 500 for unexpected errors.
    """
    try:
        solution = solver.solve(instance)
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


@router.post("/solve-instance-randomly", response_model=FacilityLocationSolution)
def solve_instance_randomly(instance: FacilityLocationInstance) -> FacilityLocationSolution:
    """
    Solve a facility location problem instance using random assignment.

    Args:
        instance: A complete facility location problem instance.

    Returns:
        FacilityLocationSolution: A feasible but not necessarily optimal solution.

    Example:
        POST /api/solve-instance-randomly
        {
            "n_customers": 10,
            "n_facilities": 3,
            "opening_cost": 10,
            "customers": [...],
            "facilities": [...]
        }
    """
    return _solve(instance, random_solver)


@router.post("/solve-instance-optimally", response_model=FacilityLocationSolution)
def solve_instance_optimally(instance: FacilityLocationInstance) -> FacilityLocationSolution:
    """
    Solve a facility location problem instance to optimality using MILP.

    Args:
        instance: A complete facility location problem instance.

    Returns:
        FacilityLocationSolution: The optimal solution.

    Example:
        POST /api/solve-instance-optimally
        {
            "n_customers": 10,
            "n_facilities": 3,
            "opening_cost": 10,
            "customers": [...],
            "facilities": [...]
        }
    """
    return _solve(instance, optimal_solver)