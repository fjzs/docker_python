import random
import time


def solve_random(instance):
    start_time = time.time()

    n_facilities = instance.n_facilities

    # Random open facilities
    open_facilities = [
        i for i in range(n_facilities)
        if random.random() < 0.5
    ]

    if not open_facilities:
        open_facilities = [random.randint(0, n_facilities - 1)]

    assignments = []

    for customer_id in range(instance.n_customers):
        facility_id = random.choice(open_facilities)
        assignments.append({
            "customer_id": customer_id,
            "facility_id": facility_id
        })

    return {
        "status": "random_solution",
        "open_facilities": open_facilities,
        "assignments": assignments,
        "solve_time": time.time() - start_time,
    }