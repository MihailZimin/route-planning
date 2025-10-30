"""Brute force algorithm class."""
import itertools

import numpy as np

from .tsp_abstract_solver import TSPSolver


class BruteForceSolver(TSPSolver):
    """
    Class that represents brute force solution to TSP.
    """

    def solve(self, matrix: np.ndarray, start: int) -> list[int]:
        """
        Solve travel salesman problem.

        Args:
            matrix: matrix of lengthes,
                where matrix[i][j] is length of path from i-th control point to j-th
            start: index of start control point

        Returns:
            sequence(list) of points in optimal order.

        """
        size = matrix.shape[0]
        matrix = np.where(matrix == -1, np.inf, matrix)

        permutated_vertices = [i for i in range(size) if i != start]

        optimal_length = np.inf
        optimal_path = []

        for permutation in itertools.permutations(permutated_vertices):
            cur_length = 0
            prev_vertex = start
            for vertex in permutation:
                cur_length += matrix[prev_vertex, vertex]
                prev_vertex = vertex
            cur_length += matrix[permutation[-1], start]
            if cur_length < optimal_length:
                optimal_length = cur_length
                optimal_path = [start, *permutation, start]

        self._optimal_length = optimal_length
        return optimal_path, optimal_length
