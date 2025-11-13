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

    def _find_right_order(
            self,
            v: int,
            visited: list[int],
            data: np.ndarray,
            order: list[int]
    ) -> None:
        """
        Find topologic-like order of elements.

        This order is written in "order" array.

        Args:
            v: start vertex
            visited: array where visited[i] equal to 1 if vertex with index i is visited
                and 0 otherwise
            data: matrix of distances
            order: array, where this method writes right order of elements

        """
        visited[v] = 1
        for u in range(data.shape[0]):
            if (visited[u] or data[v][u] == np.inf):
                continue
            self._find_right_order(u, visited, data, order)
        order.append(v)

    def _get_component(self, v: int, visited: list[int], component: list[int], data: np.ndarray) -> None:
        """
        Find strongly connected component.

        Args:
            v: start vertex
            visited: array where visited[i] equal to 1 if vertex with index i is visited
                and 0 otherwise:
            component: array, where this metthod writes elements of one strong connected component
            data: matrix of distances

        """
        visited[v] = 1
        component.append(v)
        for u in range(data.shape[0]):
            if (visited[u] or data.T[v][u] == np.inf):
                continue
            self._get_component(u, visited, component, data)

    def _find_strongly_connected_components(self, data: np.ndarray) -> list[list[int]]:
        """
        Find every strongly connected component.

        Args:
            data: matrix of distances

        """
        size = data.shape[0]
        visited = [0] * size
        component = []
        order = []
        components = []

        for i in range(size):
            if not visited[i]:
                self._find_right_order(i, visited, data, order)
        visited = [0] * size
        while order:
            v = order.pop()
            if not visited[v]:
                self._get_component(v, visited, component, data)
                components.append(component.copy())
                component = []

        return components

    def _get_elements_not_in_main_component(
            self,
            components: list[list[int]],
            main_element: int
    ) -> list[int]:
        """
        Find every element which is not in the component with main element.

        Args:
            components: list of strongly connected components
            main_element: major element which indicates main component

        """
        elements = []
        for component in components:
            if main_element in component:
                continue
            elements += component

        return elements
