"""Class TSPSolver for easier data processing."""
import itertools
from abc import ABC, abstractmethod

import numpy as np


class SolutionExceptionError(Exception):
    """
    Custom exception for TSP.
    """


class TSPSolver(ABC):
    """
    Abstract TSP solver class.
    """

    @abstractmethod
    def solve(self, matrix: np.ndarray, start: int) -> list[int]:
        """
        Solve travel salesman problem.

        Args:
            matrix: matrix of distances,
                where matrix[i][j] is length of path from i-th control point to j-th
            start: index of start control point

        Returns:
            sequence(list) of points in optimal order.

        """

    def _find_right_order(
            self,
            v: int,
            visited: list[int],
            matrix: np.ndarray,
            order: list[int]
    ) -> None:
        """
        Find topologic-like order of elements.

        This order is written in "order" array.

        Args:
            v: start vertex
            visited: array where visited[i] equal to 1 if vertex with index i is visited
                and 0 otherwise
            matrix: matrix of distances,
                where matrix[i][j] is length of path from i-th control point to j-th
            order: array, where this method writes right order of elements

        """
        visited[v] = 1
        for u in range(matrix.shape[0]):
            if (visited[u] or matrix[v][u] == np.inf):
                continue
            self._find_right_order(u, visited, matrix, order)
        order.append(v)

    def _get_component(
            self,
            v: int,
            visited: list[int],
            component: list[int],
            matrix: np.ndarray
        ) -> None:
        """
        Find strongly connected component.

        Args:
            v: start vertex
            visited: array where visited[i] equal to 1 if vertex with index i is visited
                and 0 otherwise:
            component: array, where this method writes elements of one strong connected component
            matrix: matrix of distances,
                where matrix[i][j] is length of path from i-th control point to j-th

        """
        visited[v] = 1
        component.append(v)
        for u in range(matrix.shape[0]):
            if (visited[u] or matrix.T[v][u] == np.inf):
                continue
            self._get_component(u, visited, component, matrix)

    def _find_strongly_connected_components(self, matrix: np.ndarray) -> list[list[int]]:
        """
        Find every strongly connected component.

        Args:
            matrix: matrix of distances,
                where matrix[i][j] is length of path from i-th control point to j-th

        """
        size = matrix.shape[0]
        visited = [0] * size
        component = []
        order = []
        components = []

        for i in range(size):
            if not visited[i]:
                self._find_right_order(i, visited, matrix, order)
        visited = [0] * size
        while order:
            v = order.pop()
            if not visited[v]:
                self._get_component(v, visited, component, matrix)
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

    def _check_input_data(self, matrix: np.ndarray, start: int) -> None:
        """
        Check data correctness.

        Data is incorrect if there is no solution of travel salesman problem.

        Args:
            matrix: matrix of distances,
                where matrix[i][j] is length of path from i-th control point to j-th
            start: start point of route

        Raises:
            SolutionExceptionError: if check fails

        """
        components = self._find_strongly_connected_components(matrix)
        if len(components) > 1:
            unreachable_elements = self._get_elements_not_in_main_component(components, start)
            error_msg = (f"Can't build a route thruough every vertex\n"
                         f"Those vertices are unreachable: {unreachable_elements}")
            raise SolutionExceptionError(error_msg)

    def _transform_matrix_for_multiple_salesmen(
            self,
            matrix: np.ndarray,
            start_point: int,
            salesmen_count: int
        ) -> np.ndarray:
        """
        Transform matrix of distances with one control point to matrix with multiple control points.

        Args:
            matrix: original matrix of distances
            start_point: start point
            salesmen_count: count of salesmen

        Returns:
            Expanded matrix for muptiple salesmen logic

        """
        original_size = matrix.shape[0]
        result_size = original_size + salesmen_count - 1
        result_matrix = np.full(shape=(result_size, result_size), fill_value=np.inf)
        result_matrix[:original_size, :original_size] = matrix
        for copy_start_point in range(original_size, result_size):
            result_matrix[copy_start_point, :original_size] = matrix[start_point, :]
            result_matrix[:original_size, copy_start_point] = matrix[:, start_point]

        return result_matrix

    def _unravel_multiple_salesmen_routes(
            self,
            mixed_route: list[int],
            points_count: int,
            start_point: int
        ) -> list[list[int]]:
        """
        Divide raw route to multiple routes for each salesman.

        Args:
            mixed_route: route with mixed salesmen pathes
            points_count: count of control points
            start_point: start point

        Returns:
            list of lists of routes for each salesman

        """
        single_route = []
        result_routes = []
        for current_point, next_point in itertools.pairwise(mixed_route):
            point_to_add = current_point
            if point_to_add >= points_count:
                point_to_add = start_point
            single_route.append(point_to_add)
            if next_point >= points_count or next_point == start_point:
                single_route.append(single_route[0])
                result_routes.append(single_route.copy())
                single_route = []

        return result_routes

