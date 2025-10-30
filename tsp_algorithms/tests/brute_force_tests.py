"""Tests for brute force algorithm of TSP."""
import json
from pathlib import Path

import numpy as np
import pytest

from tsp_algorithms.tsp_brute_force import BruteForceSolver


@pytest.fixture
def sample_solver() -> BruteForceSolver:
    """
    Fixture for brute force solver.
    """
    return BruteForceSolver()

@pytest.mark.fast
def test_on_data_from_file(sample_solver: BruteForceSolver) -> None:
    """
    Tests for brute force algorithm taken from file.
    """
    test_data = {}
    with Path("tsp_algorithms/cases.json").open() as f:
        test_data = json.load(f)

    for data in test_data.values():

        matrix = np.array(data["matrix"], dtype=float)
        matrix = np.where(matrix == -1, np.inf, matrix)
        start = data["start"]
        expected_length = data["expected_length"]

        _, length = sample_solver.solve(matrix, start)
        assert length == expected_length
