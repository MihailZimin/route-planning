"""Module for route calculation logic."""

from itertools import product

import numpy as np

from core.arc import Arc
from core.circle import Circle
from core.line import Line
from core.point import Point
from core.polygon import Polygon

try:
    from pathfinding.dijkstra import algorithm_dijkstra
    from pathfinding.visibility_graph import (
        build_visibility_matrix,
        collect_nodes,
    )
except (ImportError, AttributeError):
    from dijkstra import algorithm_dijkstra
    from visibility_graph import (
        build_visibility_matrix,
        collect_nodes,
    )


class Route:
    """Class representing a calculated route."""

    def __init__(self, route: list[Line | Arc]) -> None:
        """Initialize route."""
        self.route = route

    @property
    def length(self) -> float:
        """Calculate total length of the route."""
        return sum([x.length() for x in self.route])


def point_to_point(start: Point, end: Point, obstacles: list[Circle | Line | Polygon]) -> Route:
    """
    Find the shortest path using Tangent Graph (supporting Arcs).
    """
    # 1. Collecting all points that can theoretically form an optimal route
    nodes, node_to_circle = collect_nodes(start, end, obstacles)

    # 2. Converting to matrix
    matrix = build_visibility_matrix(nodes, obstacles, node_to_circle)

    # 3. Getting start and finish node's indexes
    start_idx = 0
    end_idx = 1

    # 4. Getting optimal path between start and end
    path_indices, _ = algorithm_dijkstra(matrix, start_idx, end_idx)

    # Fallback for no path (should not be triggered)
    if not path_indices:
        return Route([Line(start, end)])

    # 5. Converting to Route object with Line/Arc segments
    path_segments = []

    for k in range(len(path_indices) - 1):
        idx_curr = path_indices[k]
        idx_next = path_indices[k + 1]

        p_curr = nodes[idx_curr]
        p_next = nodes[idx_next]

        # Check if points are on the same circle
        circ_curr = node_to_circle.get(idx_curr)
        circ_next = node_to_circle.get(idx_next)

        if circ_curr and circ_next and circ_curr == circ_next:
            # 2 points form an Arc
            try:
                arc = Arc(circ_curr.center, p_curr, p_next)
                path_segments.append(arc)
            except ValueError:
                # Fallback to a Line
                path_segments.append(Line(p_curr, p_next))
        else:
            # 2 points form a Line
            path_segments.append(Line(p_curr, p_next))

    return Route(path_segments)


def route_calculation(
    points: list[Point], obstacles: list[Circle | Line | Polygon]
) -> list[list[Route]]:
    """Calculate routes between all pairs of control points."""
    n = len(points)
    matrix = [[None for _ in range(n)] for _ in range(n)]

    for i, j in product(range(n), range(n)):
        if i == j:
            matrix[i][j] = Route([])
        else:
            matrix[i][j] = point_to_point(points[i], points[j], obstacles)

    return matrix


def matrix_calculation(routes: list[list[Route]]) -> np.ndarray:
    """Convert Route objects to distance matrix for TSP solver."""
    n = len(routes)
    dist_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = routes[i][j].length

    return dist_matrix
