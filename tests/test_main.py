import numpy as np

from app.main import knapsack_greedy


def test_basic_case():
    weights = np.array([2, 3, 4, 5])
    values = np.array([3, 4, 5, 6])
    capacity = 5
    selected, total_value = knapsack_greedy(weights, values, capacity)
    assert total_value == 7
    assert sorted(selected) == [0, 1]


def test_empty_case():
    weights = np.array([])
    values = np.array([])
    capacity = 10
    selected, total_value = knapsack_greedy(weights, values, capacity)
    assert total_value == 0
    assert selected == []


def test_no_fit():
    weights = np.array([10, 20, 30])
    values = np.array([1, 2, 3])
    capacity = 5
    selected, total_value = knapsack_greedy(weights, values, capacity)
    assert total_value == 0
    assert selected == []
