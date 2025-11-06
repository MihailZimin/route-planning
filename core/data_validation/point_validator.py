"""Validator class for Point."""
from collections.abc import Callable
from typing import ClassVar

from .data_validator import GeometryValidator


class PointExceptionError(Exception):
    """
    Custom exception for Point validation errors.
    """


class PointValidator(GeometryValidator):
    """
    Class for Point validation.
    """

    @staticmethod
    def _get_x_coord_error_msg(x: float | object) -> str:
        """
        Get x point coordinate's error message.

        Args:
            x: x-coordinate

        Returns:
            error message

        """
        error_msg = ""
        if not isinstance(x, (int, float)):
            error_msg += f"x coordinate: '{x}' is not a number\n"
        else:
            if x < GeometryValidator.XMINCOORDS:
                error_msg += (f"x coordinate is lower than lower bound: "
                              f"{x} < {GeometryValidator.XMINCOORDS}\n")
            if x > GeometryValidator.XMAXCOORDS:
                error_msg += (f"x coordinate is upper than upper bound: "
                              f"{x} > {GeometryValidator.XMAXCOORDS}\n")

        return error_msg

    @staticmethod
    def _get_y_coord_error_msg(y: float | object) -> str:
        """
        Get y point coordinate's error message.

        Args:
            y: y-coordinate

        Returns:
            error message

        """
        error_msg = ""
        if not isinstance(y, (int, float)):
            error_msg += f"y coordinate: '{y}' is not a number\n"
        else:
            if y < GeometryValidator.YMINCOORDS:
                error_msg += (f"y coordinate is lower than lower bound: "
                              f"{y} < {GeometryValidator.YMINCOORDS}\n")
            if y > GeometryValidator.YMAXCOORDS:
                error_msg += (f"y coordinate is upper than upper bound: "
                              f"{y} > {GeometryValidator.YMAXCOORDS}\n")

        return error_msg

    @staticmethod
    def _validate_point_init(x: float | object, y: float | object) -> None:
        """
        Validate point coordinates.

        Args:
            x: x-coordinate
            y: y-coordinate

        Raises:
            PointErrorException: if validation fails

        """
        error_msg = (
            PointValidator._get_x_coord_error_msg(x) +
            PointValidator._get_y_coord_error_msg(y)
        )

        if error_msg:
            raise PointExceptionError(error_msg)

    @staticmethod
    def _validate_point_x_setter(x: float | object) -> None:
        """
        Validate x coordinate point setter.
        """
        error_msg = PointValidator._get_x_coord_error_msg(x)

        if error_msg:
            raise PointExceptionError(error_msg)

    @staticmethod
    def _validate_point_y_setter(y: float | object) -> None:
        """
        Validate y coordinate point setter.
        """
        error_msg = PointValidator._get_y_coord_error_msg(y)

        if error_msg:
            raise PointExceptionError(error_msg)

    validators: ClassVar[dict[str, Callable]] = {
        "Point_init": _validate_point_init,
        "Point_x_setter": _validate_point_x_setter,
        "Point_y_setter": _validate_point_y_setter,
    }
