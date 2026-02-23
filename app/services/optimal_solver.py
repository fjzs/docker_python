"""
Optimal Solver Service
Solves a facility location instance to optimality using Mixed Integer Linear
Programming (MILP) via PuLP.

Formulation:
    Variables:
        y[j] in {0, 1}  -- 1 if facility j is open
        x[i][j] in {0, 1}  -- 1 if customer i is assigned to facility j

    Objective:
        minimize sum_{i,j} d(i,j) * x[i][j] + opening_cost * sum_j y[j]

    Constraints:
        sum_j x[i][j] = 1        for all i  (each customer assigned to exactly one)
        x[i][j] <= y[j]          for all i, j  (only assign to open facilities)
"""
import logging

import pulp

from app.models import FacilityLocationInstance, FacilityLocationSolution
from app.models.facility_location_solution import Assignment

logger = logging.getLogger(__name__)


def solve(instance: FacilityLocationInstance) -> FacilityLocationSolution:
    """
    Solves a facility location instance to optimality using MILP.

    Uses PuLP with the default CBC solver to find the assignment of customers
    to facilities that minimizes total transportation and opening costs.

    Args:
        instance: A complete facility location problem instance.

    Returns:
        FacilityLocationSolution: The optimal solution.

    Raises:
        ValueError: If the solver fails to find an optimal solution.
    """
    customers = range(instance.n_customers)
    facilities = range(instance.n_facilities)

    # Precompute distances between all customer-facility pairs
    distances = {
        (i, j): instance.customers[i].distance_to(instance.facilities[j])
        for i in customers
        for j in facilities
    }

    # Define the problem
    prob = pulp.LpProblem("facility_location", pulp.LpMinimize)

    # Decision variables
    x = pulp.LpVariable.dicts("x", [(i, j) for i in customers for j in facilities], cat="Binary")
    y = pulp.LpVariable.dicts("y", facilities, cat="Binary")

    # Objective: minimize transportation + opening costs
    prob += (
        pulp.lpSum(distances[i, j] * x[i, j] for i in customers for j in facilities)
        + instance.opening_cost * pulp.lpSum(y[j] for j in facilities)
    )

    # Constraint: each customer must be assigned to exactly one facility
    for i in customers:
        prob += pulp.lpSum(x[i, j] for j in facilities) == 1

    # Constraint: customers can only be assigned to open facilities
    for i in customers:
        for j in facilities:
            prob += x[i, j] <= y[j]

    # Solve — change msg=1 to msg=0 to suppress solver output
    prob.solve(pulp.PULP_CBC_CMD(msg=1))

    if pulp.LpStatus[prob.status] != "Optimal":
        raise ValueError(
            f"Solver did not find an optimal solution: {pulp.LpStatus[prob.status]}"
        )

    # Extract open facilities
    open_facilities = [j for j in facilities if pulp.value(y[j]) > 0.5]

    # Extract assignments
    assignments = [
        Assignment(
            customer_id=i,
            facility_id=next(j for j in facilities if pulp.value(x[i, j]) > 0.5),
        )
        for i in customers
    ]

    # Compute costs from the solution
    total_transportation_cost = sum(
        distances[a.customer_id, a.facility_id] for a in assignments
    )
    total_opening_cost = len(open_facilities) * instance.opening_cost
    total_cost = total_transportation_cost + total_opening_cost

    logger.info(
        f"Optimal solver: {len(open_facilities)}/{instance.n_facilities} facilities open, "
        f"{instance.n_customers} customers assigned, total cost: {total_cost:.2f}"
    )

    return FacilityLocationSolution(
        open_facilities=open_facilities,
        assignments=assignments,
        total_transportation_cost=total_transportation_cost,
        total_opening_cost=float(total_opening_cost),
        total_cost=total_cost,
    )