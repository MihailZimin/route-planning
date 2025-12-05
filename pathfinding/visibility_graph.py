"""Module for building visibility graph."""

import math
from itertools import product

import numpy as np
from core.circle import Circle
from core.line import Line
from core.point import Point
from core.polygon import Polygon

try:
    from pathfinding.dijkstra import algorithm_dijkstra
except (ImportError, AttributeError):
    from dijkstra import algorithm_dijkstra


def approximate_circle(circle: Circle, segments: int = 360) -> Polygon:
    """Approximates a circle with a polygon."""
    points = []
    angle_step = 2 * math.pi / segments
    for i in range(segments):
        angle = i * angle_step
        x = circle.center.x + circle.radius * math.cos(angle)
        y = circle.center.y + circle.radius * math.sin(angle)
        points.append(Point(x, y))
    return Polygon(points)


def ccw(a: Point, b: Point, c: Point) -> float:
    """
    Counter-Clockwise test.

    Returns positive value if a->b->c is counter-clockwise,
    negative if clockwise, 0 if collinear.
    """
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def segments_intersect(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    """
    Check if segment [p1, p2] strictly intersects segment [p3, p4].

    Strict intersection: touching at endpoints returns False.
    """
    d1 = ccw(p3, p4, p1)
    d2 = ccw(p3, p4, p2)
    d3 = ccw(p1, p2, p3)
    d4 = ccw(p1, p2, p4)

    return ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and (
        (d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)
    )


def obstacle_is_in_the_way(
    p_start: Point, p_end: Point, obstacle: Line | Polygon | Circle
) -> bool:
    """Check if obstacle intersects the segment [p_start, p_end]."""
    # 1. Line
    if isinstance(obstacle, Line):
        return segments_intersect(p_start, p_end, obstacle.start, obstacle.end)

    # 2. Polygon
    if isinstance(obstacle, Polygon):
        poly_points = obstacle.points
        # Check all edges
        for i in range(len(poly_points) - 1):
            p1_poly = poly_points[i]
            p2_poly = poly_points[i + 1]

            if segments_intersect(p_start, p_end, p1_poly, p2_poly):
                return True
        return False

    # 3. Circle (approximated as Polygon)
    if isinstance(obstacle, Circle):
        poly = approximate_circle(obstacle)
        return obstacle_is_in_the_way(p_start, p_end, poly)

    return False


def check_all_obstacles(
    p_start: Point, p_end: Point, obstacles: list[Line | Polygon | Circle]
) -> bool:
    """Check if ANY obstacle blocks the path."""
    return any(obstacle_is_in_the_way(p_start, p_end, obs) for obs in obstacles)


def collect_nodes(
    start: Point, end: Point, obstacles: list[Line | Polygon | Circle]
) -> list[Point]:
    """Collect all important nodes: Start, End + all vertices of obstacles."""
    nodes = [start, end]

    for obs in obstacles:
        if isinstance(obs, Line):
            nodes.append(obs.start)
            nodes.append(obs.end)
        elif isinstance(obs, Polygon):
            # Polygon.points returns closed loop, take slice to avoid duplicate
            nodes.extend(obs.points[:-1])
        elif isinstance(obs, Circle):
            poly = approximate_circle(obs)
            nodes.extend(poly.points[:-1])

    return nodes


def build_visibility_matrix(
    nodes: list[Point], obstacles: list[Line | Polygon | Circle]
) -> np.ndarray:
    """Build adjacency matrix for visibility graph."""
    n = len(nodes)
    matrix = np.full((n, n), np.inf)

    for i, j in product(range(n), range(n)):
        if i == j:
            matrix[i][j] = 0
            continue

        p1 = nodes[i]
        p2 = nodes[j]

        if not check_all_obstacles(p1, p2, obstacles):
            dist = p1.distance_to(p2)
            matrix[i][j] = dist
            matrix[j][i] = dist

    return matrix


if __name__ == "__main__":
    # Test Part 6
    print("Test Part 6: Auto-pathfinding through obstacle vertices")  # noqa: T201

    p_start = Point(10, 50)
    p_end = Point(90, 50)

    # Obstacle: Wall
    wall = Line(Point(50, 10), Point(50, 90))
    obstacles = [wall]

    nodes_list = collect_nodes(p_start, p_end, obstacles)
    print(f"Total nodes: {len(nodes_list)}")  # noqa: T201
    for i, p in enumerate(nodes_list):
        print(f"  {i}: {p}")  # noqa: T201

    matrix_res = build_visibility_matrix(nodes_list, obstacles)

    path_indices, length = algorithm_dijkstra(matrix_res, 0, 1)

    print(f"Found path (indices): {path_indices}")  # noqa: T201

    path_points = [str(nodes_list[idx]) for idx in path_indices]
    print(f"Route: {' -> '.join(path_points)}")  # noqa: T201

    # Indices [0, 2, 1] or [0, 3, 1] are valid
    is_path_valid = path_indices in ([0, 2, 1], [0, 3, 1])
    assert is_path_valid, f"Invalid path: {path_indices}"  # noqa: S101

    print("Success! Drone found the edge of the wall.")  # noqa: T201