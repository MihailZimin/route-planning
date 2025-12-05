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
    from pathfinding.visibility_graph import build_visibility_matrix, collect_nodes
except (ImportError, AttributeError):
    # Fallback for local testing
    from dijkstra import algorithm_dijkstra
    from visibility_graph import build_visibility_matrix, collect_nodes


class Route:
    """Class representing a calculated route."""

    def __init__(self, route: list[Line | Arc]) -> None:
        """Initialize route."""
        self.route = route

    @property
    def length(self) -> float:
        """Calculate total length of the route."""
        return sum([x.length() for x in self.route])


def point_to_point(
    start: Point, end: Point, obstacles: list[Circle | Line | Polygon]
) -> Route:
    """
    Find shortest path between two points avoiding obstacles using Dijkstra.
    """
    # 1. Собираем граф (узлы: старт, финиш, углы препятствий)
    nodes = collect_nodes(start, end, obstacles)

    # 2. Строим матрицу видимости (кто кого видит напрямую)
    matrix = build_visibility_matrix(nodes, obstacles)

    # 3. Находим индексы узлов Старта и Финиша в списке nodes
    start_idx = nodes.index(start)
    end_idx = nodes.index(end)

    # 4. Запускаем Дейкстру
    path_indices, _ = algorithm_dijkstra(matrix, start_idx, end_idx)

    # 5. Если пути нет (или он пустой), возвращаем прямую линию (fallback)
    if not path_indices:
        return Route([Line(start, end)])

    # 6. Превращаем список точек в список линий (маршрут)
    path_segments = []
    for i in range(len(path_indices) - 1):
        p1 = nodes[path_indices[i]]
        p2 = nodes[path_indices[i + 1]]
        path_segments.append(Line(p1, p2))

    return Route(path_segments)


def route_calculation(
    points: list[Point], obstacles: list[Circle | Line | Polygon]
) -> list[list[Route]]:
    """Calculate routes between all pairs of control points."""
    # Создаем матрицу маршрутов размером NxN
    n = len(points)
    matrix = [[None for _ in range(n)] for _ in range(n)]

    for i, j in product(range(n), range(n)):
        if i == j:
            # Путь из точки в саму себя - пустой
            matrix[i][j] = Route([])
        else:
            # Считаем сложный путь с препятствиями
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