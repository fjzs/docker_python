import numpy as np

def knapsack_greedy(
    weights: np.ndarray, values: np.ndarray, capacity: float
) -> tuple[list[int], float]:
    """
    Greedy heuristic: pick items based on highest value-to-weight ratio.
    Returns selected item indices and total value.
    """
    index = list(range(len(weights)))
    ratio = [v / w for v, w in zip(values, weights)]
    # Sort items by descending value-to-weight ratio
    index.sort(key=lambda i: ratio[i], reverse=True)

    total_value = 0
    total_weight = 0
    selected_items = []

    for i in index:
        if total_weight + weights[i] <= capacity:
            selected_items.append(i)
            total_weight += weights[i]
            total_value += values[i]

    return selected_items, total_value