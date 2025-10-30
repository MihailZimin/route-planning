"""Tests for Little's algorithm."""
import json
import math
from pathlib import Path

import numpy as np
import pytest

from tsp_algorithms.brute_force import BruteForceSolver
from tsp_algorithms.little_algorithm import LittleAlgorithm


@pytest.fixture
def sample_solver_bruteforce() -> BruteForceSolver:
    """
    Fixture for brute force solver.
    """
    return BruteForceSolver()

@pytest.fixture
def sample_solver_little() -> LittleAlgorithm:
    """
    Fixture for Little's algorithm solver.
    """
    return LittleAlgorithm()

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
def test_compare_to_brute_force(
        matrix_size: int,
        tests_count: int,
        start_vertex: int,
        sample_solver_bruteforce: BruteForceSolver,
        sample_solver_little: LittleAlgorithm
    ) -> None:
    """
    Test which checks if Little's algorithm realisation works.

    Considered that brute force algorithm is correct.
    """
    rng = np.random.default_rng(seed=42)

    for _ in range(tests_count):
        matrix = rng.uniform(1, 100, size=(matrix_size, matrix_size))
        np.fill_diagonal(matrix, np.inf)
        _, length_little = sample_solver_little.solve(matrix, start_vertex)
        _, length_brute = sample_solver_bruteforce.solve(matrix, start_vertex)
        assert math.isclose(length_little, length_brute, abs_tol=1e-5)

@pytest.mark.slow
@pytest.mark.parametrize(
    ("matrix_size", "tests_count", "start_vertex"),
    [
        (8, 5, 0),
        (9, 5, 0),
        (10, 10, 0),
    ]
)
def test_compare_to_brute_force_slow(
        matrix_size: int,
        tests_count: int,
        start_vertex: int,
        sample_solver_bruteforce: BruteForceSolver,
        sample_solver_little: LittleAlgorithm
    ) -> None:
    """
    Test which checks if Little's algorithm realisation works.

    Considered that brute force algorithm is correct.
    """
    rng = np.random.default_rng(seed=42)

    for _ in range(tests_count):
        matrix = rng.uniform(1, 100, size=(matrix_size, matrix_size))
        np.fill_diagonal(matrix, np.inf)
        _, length_little = sample_solver_little.solve(matrix, start_vertex)
        _, length_brute = sample_solver_bruteforce.solve(matrix, start_vertex)
        assert math.isclose(length_little, length_brute, abs_tol=1e-5)

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
def test_route_length_to_optimal(
        matrix_size: int,
        tests_count: int,
        start_vertex: int,
        sample_solver_little: LittleAlgorithm
    ) -> None:
    """
    Test that the route finded in Little's algorithm realisation is correct.

    Considered that Little algorithm correctly finds optimal length.
    If there is no valid route - test is skipped.
    """
    rng = np.random.default_rng(seed=42)

    for _ in range(tests_count):
        matrix = rng.uniform(1, 100, size=(matrix_size, matrix_size))
        np.fill_diagonal(matrix, np.inf)
        route_little, length_little = sample_solver_little.solve(matrix, start_vertex)
        if length_little == -1:
            continue

        route_length = 0
        for i in range(1, len(route_little)):
            route_length += matrix[route_little[i - 1], route_little[i]]
        assert math.isclose(length_little, route_length, abs_tol=1e-5)

@pytest.mark.fast
def test_on_data_from_file(sample_solver_little: LittleAlgorithm) -> None:
    """
    Tests for Little's algorithm taken from file.
    """
    test_data = {}
    with Path("tsp_algorithms/cases.json").open() as f:
        test_data = json.load(f)

    for data in test_data.values():

        matrix = np.array(data["matrix"], dtype=float)
        matrix = np.where(matrix == -1, np.inf, matrix)
        start = data["start"]
        expected_length = data["expected_length"]

        _, length = sample_solver_little.solve(matrix, start)
        assert length == expected_length
