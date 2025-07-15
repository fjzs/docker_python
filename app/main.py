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


def main():
    weights = np.array([10, 20, 30])
    values = np.array([60, 100, 120])
    capacity = 50
    selected_items, total_value = knapsack_greedy(weights, values, capacity)

    print("\nKnapsack Problem using Greedy Heuristic:")
    print("Weights:", weights)
    print("Capacity:", capacity)
    print("Values:", values)
    print("Selected item indices:", selected_items)
    print("Total value:", total_value)


if __name__ == "__main__":
    main()
