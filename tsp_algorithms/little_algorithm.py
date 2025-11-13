"""Little algorithm class."""
import heapq

import numpy as np

from .abstract_solver import TSPSolver


class Node:
        """
        Auxiliary class for Little's algorithm.
        """

        def __init__(
                self,
                matrix: np.ndarray,
                lower_bound: float,
                route: list[tuple[int, int]],
            ) -> None:
            """
            Initialize node.

            Args:
                matrix: 2D numpy array of distances
                lower_bound: lower bound of possible route length
                route: list of edges between points

            """
            self.matrix = matrix
            self.lower_bound = lower_bound
            self.route = route

        def __lt__(self, other: "Node") -> bool:
            """
            Auxiliary method for possibility to add elements to queue.
            """
            return self.lower_bound < other.lower_bound


class LittleAlgorithm(TSPSolver):
    """
    Class that represents Little algorithm solution to TSP.
    """

    def __add_node(self, nodes: list[Node],  node: Node) -> None:
        """
        Auxiliary method for clearer usage of heap.

        Args:
            nodes: list(heap) of elements of class Node
            node: element of class Node which we want to push in our list

        """
        heapq.heappush(nodes, node)

    def __get_best_node(self, nodes: list[Node]) -> Node:
        """
        Auxiliary method for clearer usage of heap.

        Args:
            nodes: list(heap) of elements of class Node

        Returns:
            node: element of class Node with the lowest lower_bound field.

        """
        return heapq.heappop(nodes)

    def __reduce_matrix_by_rows(self, matrix: np.ndarray) -> float:
        """
        Auxiliary method for reducing process of matrix.

        This method finds valid rows - rows where exists not np.inf value
        and by those rows make reduction process.

        Args:
            matrix: 2D numpy array of distances

        Returns:
            Summary reduction value of each row

        """
        valid_rows = ~np.all(np.isinf(matrix), axis=1)

        mins = np.zeros(matrix.shape[0])
        mins[valid_rows] = np.min(matrix[valid_rows], axis=1)
        matrix[valid_rows] -= mins[valid_rows, np.newaxis]
        return np.sum(mins)

    def __reduce_matrix_by_cols(self, matrix: np.ndarray) -> float:
        """
        Auxiliary method for reducing process of matrix.

        This method finds valid cols - cols where exists not np.inf value
        and by those cols make reduction process.

        Args:
            matrix: 2D numpy array of distances

        Returns:
            Summary reduction value of each col

        """
        valid_cols = ~np.all(np.isinf(matrix), axis=0)

        mins = np.zeros(matrix.shape[1])
        mins[valid_cols] = np.min(matrix[:, valid_cols], axis=0)
        matrix[:, valid_cols] -= mins[np.newaxis, valid_cols]
        return np.sum(mins)

    def __reduce_matrix_by_rows_and_cols(self, matrix: np.ndarray) -> float:
        """
        Auxiliary method for reducing process of matrix.

        This method provides reduction by rows and cols simultaniously.

        Args:
            matrix: 2D numpy array of distances

        Returns:
            Summary reduction value of rows and cols

        """
        return self.__reduce_matrix_by_rows(matrix) + self.__reduce_matrix_by_cols(matrix)

    def __reduce_row_and_col(self, matrix: np.ndarray, row: int, col: int) -> float:
        """
        Auxiliary method for reducing process of matrix.

        This method provides reduction by specific row and col.

        Args:
            matrix: 2D numpy array of distances
            row: row index of point in consideration
            col: col index of point in consideration

        Returns:
            Summary reduction value of row and col

        """
        summary = 0
        if not np.all(np.isinf(matrix[row, :])):
            min_elem = np.min(matrix[row])
            matrix[row] -= min_elem
            summary += min_elem
        if not np.all(np.isinf(matrix[:, col])):
            min_elem = np.min(matrix[:, col])
            matrix[:, col] -= min_elem
            summary += min_elem
        return summary

    def __get_index_with_max_penalty(self, matrix: np.ndarray) -> tuple[int, int]:
        """
        Auxiliary method for reducing process of matrix.

        This method finds zero element in matrix with maximum reduction value.

        Args:
            matrix: 2D numpy array of distances

        Returns:
            Tuple of row and col - index in matrix of element

        """
        row_mins = np.min(np.where(matrix == 0, np.inf, matrix), axis=1)
        col_mins = np.min(np.where(matrix == 0, np.inf, matrix), axis=0)

        penalties = np.where(matrix == 0, row_mins[:, np.newaxis] + col_mins[np.newaxis, :], -np.inf)

        return np.unravel_index(np.argmax(penalties), penalties.shape)

    def __find_next_start_point_edge(self, edges: list[tuple[int, int]], start_point: int) -> int:
        """
        Auxiliary method of finding early closive edges.

        This method finds for argument point edge,
        from which we entered this point.

        Args:
            edges: list of edges between points
            start_point: point for which we want to find entering edge

        Returns:
            index of edge in edges if such edge exists, otherwise -1

        """
        for i in range(len(edges)):
            if edges[i][1] == start_point:
                return i

        return -1

    def __find_next_end_point_edge(self, edges: list[tuple[int, int]], end_point: int) -> int:
        """
        Auxiliary method of finding early closive edges.

        This method finds for argument point edge,
        which we entering from this point.

        Args:
            edges: list of edges between points
            end_point: point for which we want to find outer edge

        Returns:
            index of edge in edges if such edge exists, otherwise -1

        """
        for i in range(len(edges)):
            if edges[i][0] == end_point:
                return i

        return -1

    def __unravel_edges(self, start: int, edges: list[tuple[int, int]]) -> list[int]:
        """
        Auxiliary method to find the final route.

        For edges which form correct route finds this route.

        Args:
            start: start point of the route
            edges: list of edges in the route in arbitrary order

        Returns:
            list of indices of points in correct cycle order,
            where i-th point goes after (i - 1)-th point

        """
        path = [start]
        index = self.__find_next_start_point_edge(edges, start)
        cur = int(edges[index][0])
        path.append(cur)
        while cur != start:
            index = self.__find_next_start_point_edge(edges, cur)
            cur = int(edges[index][0])
            path.append(cur)
        return path[::-1]

    def __get_close_edges(self, route: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Auxiliary method of finding early closive edges.

        Args:
            route: list of edges

        Returns:
            list of edges which forms early closive circles.

        """
        result = []
        edges = route.copy()
        min_elements_form_circle = 2

        while len(edges):
            length = 1
            edge = edges.pop()
            start = edge[0]
            end = edge[1]

            index = self.__find_next_start_point_edge(edges, start)
            while index != -1:
                length += 1
                start = edges[index][0]
                edges.pop(index)
                index = self.__find_next_start_point_edge(edges, start)

            index = self.__find_next_end_point_edge(edges, end)
            while index != -1:
                length += 1
                end = edges[index][1]
                edges.pop(index)
                index = self.__find_next_end_point_edge(edges, end)

            if length >= min_elements_form_circle:
                result.append((end, start))

        return result

    def __make_children(self, cur_node: Node) -> tuple[Node, Node]:
        """
        Auxiliary method to form new correct nodes in Little algorithm.

        Args:
            cur_node: current node from which we want to form descendant nodes

        Returns:
            left and right descendant nodes

        """
        frm, to = self.__get_index_with_max_penalty(cur_node.matrix)
        left_matrix = cur_node.matrix.copy()
        left_matrix[frm, to] = np.inf
        left_penalty = self.__reduce_row_and_col(left_matrix, frm, to)
        left_bound = cur_node.lower_bound + left_penalty
        left_child = Node(left_matrix, left_bound, cur_node.route.copy())

        right_matrix = cur_node.matrix.copy()
        right_matrix[to, frm] = np.inf
        right_matrix[frm, :] = np.inf
        right_matrix[:, to] = np.inf
        right_route = [*cur_node.route, (frm, to)]
        close_edges = self.__get_close_edges(right_route)
        for i, j in close_edges:
            right_matrix[i][j] = np.inf
        right_penalty = self.__reduce_matrix_by_rows_and_cols(right_matrix)
        right_bound = cur_node.lower_bound + right_penalty
        right_child = Node(right_matrix, right_bound, right_route)

        return left_child, right_child

    def solve(self, matrix: np.ndarray, start: int) -> list[int]:
        """
        Representation method of Little's algorithm.

        Args:
            matrix: matrix of lengthes,
                where matrix[i][j] is length of path from i-th control point to j-th
            start: index of start control point

        Returns:
            list of indices of points which form circle for the most optimal TSP solution

        """
        matrix = np.where(matrix == -1, np.inf, matrix)
        sz = matrix.shape[0]
        nodes = []

        self._check_input_data(matrix, start)

        root_matrix = matrix.copy()
        lower_bound = (self.__reduce_matrix_by_rows(root_matrix) +
                        self.__reduce_matrix_by_cols(root_matrix))
        root = Node(root_matrix, lower_bound, route=[])
        self.__add_node(nodes, root)

        optimal_length = np.inf
        optimal_route = []

        while nodes:
            cur_node = self.__get_best_node(nodes)

            if optimal_length <= cur_node.lower_bound:
                continue

            if len(cur_node.route) == sz - 1:
                final_edge = self.__get_close_edges(cur_node.route)
                cur_node.route.append(*final_edge)

            if optimal_length > cur_node.lower_bound and len(cur_node.route) == sz:
                optimal_length = cur_node.lower_bound
                optimal_route = cur_node.route
                continue

            left_child, right_child = self.__make_children(cur_node)
            self.__add_node(nodes, left_child)
            self.__add_node(nodes, right_child)

        self._optimal_length = optimal_length
        return self.__unravel_edges(start, optimal_route), optimal_length
