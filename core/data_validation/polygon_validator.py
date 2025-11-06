"""Validator class for Polygon."""
import itertools
from collections.abc import Callable
from typing import ClassVar

import numpy as np

from core.point import Point

from .data_validator import GeometryValidator


class PolygonExceptionError(Exception):
    """
    Custom exception for Polygon validation errors.
    """


class PolygonValidator(GeometryValidator):
    """
    Class for Polygon validation.
    """

    _CHECKONCONVEX: bool = False

    @staticmethod
    def _get_points_error_msg(points: list[Point]) -> str:
        error_msg = ""

        for index, point in enumerate(points):
            if not isinstance(point, Point):
                error_msg += f"element on index: {index} is not type of Point\n"

        if PolygonValidator._CHECKONCONVEX and not error_msg:
            is_convex = PolygonValidator._check_on_convex(points)
            if not is_convex:
                error_msg += "points is not forming convex polygon\n"

        return error_msg

    @staticmethod
    def _validate_polygon_init(points: list[Point]) -> None:
        """
        Validate polygon initialization.

        Args:
            points: list of points that form polygon

        Raises:
            PolygonErrorException: if validation fails

        """
        if not isinstance(points, list):
            error_msg = "points array is not type of list\n"
            raise PolygonExceptionError(error_msg)

        error_msg = PolygonValidator._get_points_error_msg(points)

        if error_msg:
            raise PolygonExceptionError(error_msg)

    @staticmethod
    def _validate_polygon_setter(points: list[Point]) -> None:
        """
        Validate polygon points setter.

        Args:
            points: list of points that form polygon

        Raises:
            PolygonErrorException: if validation fails

        """
        error_msg = PolygonValidator._get_points_error_msg(points)

        if error_msg:
            raise PolygonExceptionError(error_msg)

    @staticmethod
    def check_on_convex(points: list[Point]) -> bool:
        """
        Check if polygon is convex.

        Args:
            points: list of points that form polygon

        Returns:
            bool variable:
                True if points form convex polygon
                False otherwise

        """
        sides = list(itertools.pairwise(points))
        pair_sides = list(itertools.pairwise(sides))
        reference_vector = np.array([0, 0, 1])

        def get_sign(side1: Point, side2: Point) -> int:
            vec1 = np.array([side1[1].x - side1[0].x, side1[1].y - side1[0].y, 0])
            vec2 = np.array([side2[1].x - side2[0].x, side2[1].y - side2[0].y, 0])
            return np.sign(np.inner(np.cross(vec1, vec2), reference_vector))

        sign = get_sign(*pair_sides[0])
        return all(get_sign(side1, side2) == sign for side1, side2 in pair_sides)

    validators: ClassVar[dict[str, Callable]] = {
        "Polygon_init": _validate_polygon_init,
        "Polygon_setter": _validate_polygon_setter,
    }
