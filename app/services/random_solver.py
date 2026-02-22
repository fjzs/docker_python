"""
Random Solver Service
Solves a facility location instance by randomly assigning customers to facilities.
This is a baseline solver — it produces feasible but not optimal solutions.
"""
import logging
import random

from app.models import FacilityLocationInstance, FacilityLocationSolution
from app.models.facility_location_solution import Assignment

logger = logging.getLogger(__name__)


def solve(instance: FacilityLocationInstance) -> FacilityLocationSolution:
    """
    Solves a facility location instance using random assignment.

    Randomly selects at least one facility to open, then assigns each
    customer to a randomly chosen open facility.

    Args:
        instance: A complete facility location problem instance

    Returns:
        FacilityLocationSolution: A feasible solution with random assignments

    Raises:
        ValueError: If the instance has no facilities
    """
    # Randomly decide which facilities are open (guarantee at least one)
    all_indices = list(range(instance.n_facilities))
    n_open = random.randint(1, instance.n_facilities)
    open_facilities = sorted(random.sample(all_indices, n_open))

    # Assign each customer to a random open facility
    assignments = [
        Assignment(customer_id=i, facility_id=random.choice(open_facilities))
        for i in range(instance.n_customers)
    ]

    logger.info(
        f"Random solver: {len(open_facilities)}/{instance.n_facilities} facilities open, "
        f"{instance.n_customers} customers assigned"
    )

    return FacilityLocationSolution(
        open_facilities=open_facilities,
        assignments=assignments,
    )