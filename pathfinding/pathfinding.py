"""TODO: description of module."""

from itertools import product

import numpy as np

from core.arc import Arc
from core.circle import Circle
from core.line import Line
from core.point import Point
from core.polygon import Polygon


class Route:
    """TODO: description of class."""

    def __init__(self, route: list[Line | Arc]):
        """TODO: description of method."""
        self.route = route

    @property
    def length(self) -> float:
        return sum([x.length() for x in self.route])

def point_to_point(start: Point, end: Point, obstacles: set[Circle | Line | Polygon]) -> Route:
    """TODO: description of function."""
    path = []
    position = start

    for obstacle in obstacles:
        if isinstance(obstacle, Line):
            path.append(Line(position, obstacle.start))
            path.append(Line(obstacle.start, obstacle.end))
            position = obstacle.end
        if isinstance(obstacle, Circle):
            left = Point(obstacle.center.x - obstacle.radius, obstacle.center.y)
            right = Point(obstacle.center.x + obstacle.radius, obstacle.center.y)
            path.append(Line(position, left))
            path.append(Arc(center=obstacle.center, p_start=left, p_end=right))
            position = right
        if isinstance(obstacle, Polygon):
            for point in obstacle.points:
                path.append(Line(position, point))
                position = point
    path.append(Line(position, end))

    return Route(path)

def route_calculation(points: list[Point], obstacles: set[Circle | Line | Polygon]) -> Route:
    """TODO: description of function."""
    matrix = [[None for j in range(len(points))] for i in range(len(points))]
    for i, j in product(range(len(points)), range(len(points))):
        matrix[i][j] = point_to_point(points[i], points[j], obstacles)
    return matrix

def matrix_calculation(routes: list[list[Route]]) -> np.ndarray:
    """TODO: description of function."""
    return np.array([[routes[i][j].length for j in range(len(routes))] for i in range(len(routes))])

if __name__ == "__main__":
    a, b = Point(0,0), Point(10,10)
    obstacles = [
        Line(Point(3,0), Point(0,3)),
        Circle(Point(5,5), 1),
        Polygon([Point(7,0), Point(8,0), Point(7, 1)]),
    ]
    routes = route_calculation([a, b], obstacles)
    matrix = matrix_calculation(routes)
    [[print(routes[i][j].route) for j in range(len(routes))] for i in range(len(routes))]
    print(matrix)
