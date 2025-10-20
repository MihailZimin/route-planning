"""Class TSPSolver for easier data processing."""
from abc import ABC, abstractmethod

import numpy as np


class TSPSolver(ABC):
    """
    Abstract TSP solver class.
    """

    @abstractmethod
    def solve(self, data: np.ndarray, start: int) -> list[int]:
        """
        Solve travel salesman problem.

        Args:
            data: matrix of lengthes, where data[i][j] is length of path from i-th control point to j-th
            start: index of start control point

        Returns:
            sequence(list) of points in optimal order.

        """
