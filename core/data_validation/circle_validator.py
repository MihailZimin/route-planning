"""Validator class for Circle."""
from collections.abc import Callable
from typing import ClassVar

from core.point import Point

from .data_validator import GeometryValidator


class CircleExceptionError(Exception):
    """
    Custom exception for Circle validation errors.
    """


class CircleValidator(GeometryValidator):
    """
    Class for Circle validation.
    """

    @staticmethod
    def _validate_circle_init(center: Point, radius: float | object) -> None:
        """
        Validate circle.

        Args:
            center: center coordinates
            radius: radius value

        Raises:
            CircleErrorException: if validation fails

        """
        error_msg = (
            GeometryValidator.get_radius_error_msg(radius)
        )
        if not isinstance(center, Point):
            error_msg += "center is not Point type\n"

        if error_msg:
            raise CircleExceptionError(error_msg)

    @staticmethod
    def _validate_circle_radius_setter(radius: float | object) -> None:
        """
        Validate circle radius setter.
        """
        error_msg = GeometryValidator.get_radius_error_msg(radius)

        if error_msg:
            raise CircleExceptionError(error_msg)

    @staticmethod
    def _validate_circle_center_setter(center: Point) -> None:
        """
        Validate circle center setter.
        """
        error_msg = ""

        if not isinstance(center, Point):
            error_msg += "center is not Point type\n"

        if error_msg:
            raise CircleExceptionError(error_msg)

    validators: ClassVar[dict[str, Callable]] = {
        "Circle_init": _validate_circle_init,
        "Circle_radius_setter": _validate_circle_radius_setter,
        "Circle_center_setter": _validate_circle_center_setter,
    }
