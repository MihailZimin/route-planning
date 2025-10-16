"""Class TSPSolver for easier data processing."""
from enum import Enum

import numpy as np


class TSPAlgorithm(Enum):
    """
    Enum class for TSP algorithms names.
    """

    BRUTE_FORCE = "brute_force"

class TSPSolver:
    """
    Class that represent algorithms for TSP problem.
    """

    def __init__(
            self,
            data: np.ndarray,
            start: int,
            algorithm: TSPAlgorithm = TSPAlgorithm.BRUTE_FORCE
        ) -> None:
        """
        Initialize necessary data.

        Args:
            data: matrix of weights, where data[i][j] is weight of path from i-th control point to j-th
            start: index of start control point
            algorithm: name of the algorithm (TSPAlgorithm class member)

        """
        self._data = data
        self._size = data.shape[0]
        self._start = start
        self._algorithm = algorithm

    def solve(self) -> list[int]:
        """
        Solve the TSP problem.

        Return optimal path

        """
        if self._algorithm == TSPAlgorithm.BRUTE_FORCE:
            return self._brute_force()
        return []

    def _brute_force(self) -> list[int]:
        self.__initialize_necessary_data()

        def recursive_iteration(ind: int, frm: int) -> None:
            if ind == self._size - 1:
                path_length = self._current_length + self._data[frm][self._start]
                if path_length < self._optimal_length:
                    self._optimal_length = path_length
                    self._optimal_path = [self._current_path, self._start]
                return

            for i in range(self._size):
                if self._visited[i]:
                    continue
                self._visited[i] = 1
                self._current_path.append(i)
                self._current_length += self._data[frm][i]

                recursive_iteration(ind + 1, i)

                self._visited[i] = 0
                self._current_path.pop()
                self._current_length -= self._data[frm][i]

        recursive_iteration(0, self._start)
        return self._optimal_path

    def __initialize_necessary_data(self) -> None:
        self._visited = [0 for _ in range(self._size)]
        self._visited[self._start] = 1
        self._current_path = [self._start]
        self._optimal_path = []
        self._current_length = 0
        self._optimal_length = 1e18
