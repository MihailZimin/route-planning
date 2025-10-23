"""Tests for Little's algorithm."""
import math

import numpy as np
import pytest

from tsp_algorithms.little_algorithm import LittleAlgorithm
from tsp_algorithms.tsp_brute_force import BruteForceSolver

solver_little = LittleAlgorithm()
solver_brute = BruteForceSolver()

@pytest.mark.fast
@pytest.mark.parametrize(
    ("matrix_size", "tests_count", "start_vertex"),
    [
        (3, 3, 0),
        (4, 5, 0),
        (5, 6, 0),
        (6, 8, 0),
    ]
)
def test_compare_to_brute_force(matrix_size: int, tests_count: int, start_vertex: int) -> None:
    """
    Test which checks if Little's algorithm realisation works.

    Considered that brute force algorithm is correct.
    """
    rng = np.random.default_rng(seed=42)

    for _ in range(tests_count):
        matrix = rng.uniform(1, 100, size=(matrix_size, matrix_size))
        np.fill_diagonal(matrix, np.inf)
        result_little = solver_little.solve(matrix, start_vertex)
        result_brute = solver_brute.solve(matrix, start_vertex)
        assert math.isclose(result_little[1], result_brute[1], abs_tol=1e-5)

@pytest.mark.slow
@pytest.mark.parametrize(
    ("matrix_size", "tests_count", "start_vertex"),
    [
        (8, 5, 0),
        (9, 5, 0),
        (10, 10, 0),
    ]
)
def test_compare_to_brute_force_slow(matrix_size: int, tests_count: int, start_vertex: int) -> None:
    """
    Test which checks if Little's algorithm realisation works.

    Considered that brute force algorithm is correct.
    """
    rng = np.random.default_rng(seed=42)

    for _ in range(tests_count):
        matrix = rng.uniform(1, 100, size=(matrix_size, matrix_size))
        np.fill_diagonal(matrix, np.inf)
        result_little = solver_little.solve(matrix, start_vertex)
        result_brute = solver_brute.solve(matrix, start_vertex)
        assert math.isclose(result_little[1], result_brute[1], abs_tol=1e-5)

@pytest.mark.fast
@pytest.mark.parametrize(
    ("matrix_size", "tests_count", "start_vertex"),
    [
        (3, 3, 0),
        (4, 5, 0),
        (5, 6, 0),
        (6, 8, 0),
    ]
)
def test_route_length_to_optimal(matrix_size: int, tests_count: int, start_vertex: int) -> None:
    """
    Test that the route finded in Little's algorithm realisation is correct.
    """
    rng = np.random.default_rng(seed=42)

    for _ in range(tests_count):
        matrix = rng.uniform(1, 100, size=(matrix_size, matrix_size))
        np.fill_diagonal(matrix, np.inf)
        result_little = solver_little.solve(matrix, start_vertex)
        route_length = 0
        for i in range(1, len(result_little[0])):
            route_length += matrix[result_little[0][i - 1], result_little[0][i]]
        assert math.isclose(result_little[1], route_length, abs_tol=1e-5)
