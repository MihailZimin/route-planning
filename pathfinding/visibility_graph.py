"""Module for building tangent visibility graph for precise circular pathfinding."""

import math
from itertools import combinations, product

import numpy as np

from core.circle import Circle
from core.line import Line
from core.point import Point
from core.polygon import Polygon


def get_distance(p1: Point, p2: Point) -> float:
    """Euclidean distance."""
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def get_tangent_points(point: Point, circle: Circle) -> list[Point]:
    """
    Calculate two tangent points on a circle from an external point.
    """
    dx = point.x - circle.center.x
    dy = point.y - circle.center.y
    dist = (dx**2 + dy**2) ** 0.5

    # Если точка внутри круга, касательных нет
    if dist < circle.radius:
        return []

    angle_to_center = math.atan2(dy, dx)

    # Смещение угла для касательной: cos(alpha) = R / D
    # Ограничиваем аргумент acos, чтобы избежать ошибок из-за float precision
    val = circle.radius / dist
    val = max(-1.0, min(1.0, val))
    angle_offset = math.acos(val)

    t1_angle = angle_to_center + angle_offset
    t2_angle = angle_to_center - angle_offset

    p1 = Point(
        circle.center.x + circle.radius * math.cos(t1_angle),
        circle.center.y + circle.radius * math.sin(t1_angle),
    )
    p2 = Point(
        circle.center.x + circle.radius * math.cos(t2_angle),
        circle.center.y + circle.radius * math.sin(t2_angle),
    )
    return [p1, p2]


def circle_line_intersection(p1: Point, p2: Point, circle: Circle) -> bool:
    """
    Check if line segment [p1, p2] intersects the circle.

    Calculates the distance from the Center to the Segment.
    """
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    if dx == 0 and dy == 0:
        return False

    # Projection of circle's center onto the line
    t = ((circle.center.x - p1.x) * dx + (circle.center.y - p1.y) * dy) / (dx * dx + dy * dy)

    # Limit t to [0, 1]
    t = max(0, min(1, t))

    closest_x = p1.x + t * dx
    closest_y = p1.y + t * dy
    closest_point = Point(closest_x, closest_y)

    dist_to_center = get_distance(closest_point, circle.center)

    return dist_to_center < (circle.radius - 1e-4)


def get_arc_length(p1: Point, p2: Point, circle: Circle) -> float:
    """Calculate the shorter arc length between two points on a circle."""
    ang1 = math.atan2(p1.y - circle.center.y, p1.x - circle.center.x)
    ang2 = math.atan2(p2.y - circle.center.y, p2.x - circle.center.x)

    diff = abs(ang1 - ang2)
    if diff > math.pi:
        diff = 2 * math.pi - diff

    return diff * circle.radius


# --- Old logic for Line and Polygon ---
def ccw(a: Point, b: Point, c: Point) -> float:
    """
    Sign of this function depends on the orientation of the ABC angle.
    """
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def segments_intersect(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    """
    Check if two segments intersect.
    """
    d1 = ccw(p3, p4, p1)
    d2 = ccw(p3, p4, p2)
    d3 = ccw(p1, p2, p3)
    d4 = ccw(p1, p2, p4)
    return ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0))


# -----------------------------------------------------


def is_path_blocked(p1: Point, p2: Point, obstacles: list) -> bool:
    """Check if straight line p1-p2 intersects ANY obstacle."""
    for obs in obstacles:
        if isinstance(obs, Line):
            if segments_intersect(p1, p2, obs.start, obs.end):
                return True
        elif isinstance(obs, Polygon):
            for i, j in combinations(range(len(obs.points) - 1)):
                if segments_intersect(p1, p2, obs.points[i], obs.points[j]):
                    return True
        elif isinstance(obs, Circle):
            # If points are NOT on the circle, path can be blocked by obstacles
            on_circle1 = math.isclose(get_distance(p1, obs.center), obs.radius, abs_tol=1e-3)
            on_circle2 = math.isclose(get_distance(p2, obs.center), obs.radius, abs_tol=1e-3)
            if not (on_circle1 and on_circle2) and circle_line_intersection(p1, p2, obs):
                return True
    return False


def collect_nodes(start: Point, end: Point, obstacles: list) -> tuple[list[Point], dict]:  # noqa: C901
    """
    Collect Start, End, and Tangent Points.

    Returns:
        nodes: list of Point objects
        node_to_circle: dict mapping index of a node -> Circle object (if it lies on one)

    """
    nodes = [start, end]
    node_to_circle = {}  # Map: index -> Circle

    # Case w/o circles
    for obs in obstacles:
        if isinstance(obs, Line):
            nodes.append(obs.start)
            nodes.append(obs.end)
        elif isinstance(obs, Polygon):
            nodes.extend(obs.points[:-1])

    # Case w circles
    def add_circle_tangent(point: Point, circle: Circle) -> None:
        tangents = get_tangent_points(point, circle)
        current_idx = len(nodes)
        for i, p in enumerate(tangents):
            nodes.append(p)
            node_to_circle[current_idx + i] = circle

    noncircle_points = nodes.copy()
    circles = [c for c in obstacles if isinstance(c, Circle)]

    for circle in circles:
        # Tangents from all non-circles to circle
        for point in noncircle_points:
            add_circle_tangent(point, circle)

    return nodes, node_to_circle


def build_visibility_matrix(nodes: list[Point], obstacles: list, node_to_circle: dict) -> np.ndarray:
    """
    Build adjacency matrix.

    Logic:
    - If points on SAME circle -> Weight is Arc Length
    - Else -> Weight is Line Length (if visible)
    """
    n = len(nodes)
    matrix = np.full((n, n), np.inf)

    for i, j in product(range(n), range(n)):
        if i == j:
            matrix[i][j] = 0
            continue

        p1 = nodes[i]
        p2 = nodes[j]

        # Check if both points are on the same circle
        circle_i = node_to_circle.get(i)
        circle_j = node_to_circle.get(j)

        if circle_i and circle_j and circle_i == circle_j:
            # Movement on the Arc, always unobstructed
            dist = get_arc_length(p1, p2, circle_i)
            matrix[i][j] = dist

        # Movement through space, may be obstructed
        elif not is_path_blocked(p1, p2, obstacles):
            matrix[i][j] = get_distance(p1, p2)

    return matrix
