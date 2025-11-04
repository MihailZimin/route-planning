"""Validator class for core geometry objects."""
from collections.abc import Callable
from functools import wraps
from typing import ClassVar


class PointExceptionError(Exception):
    """
    Custom exception for Point validation errors.
    """


class GeometryValidator:
    """
    Class for data validation.
    """

    _XMAXCOORDS: float =  1000
    _XMINCOORDS: float = -1000
    _YMAXCOORDS: float =  1000
    _YMINCOORDS: float = -1000

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
            if x < GeometryValidator._XMINCOORDS:
                error_msg += (f"x coordinate is lower than lower bound: "
                              f"{x} < {GeometryValidator._XMINCOORDS}\n")
            if x > GeometryValidator._XMAXCOORDS:
                error_msg += (f"x coordinate is upper than upper bound: "
                              f"{x} > {GeometryValidator._XMAXCOORDS}\n")

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
            if y < GeometryValidator._YMINCOORDS:
                error_msg += (f"y coordinate is lower than lower bound: "
                              f"{y} < {GeometryValidator._YMINCOORDS}\n")
            if y > GeometryValidator._YMAXCOORDS:
                error_msg += (f"y coordinate is upper than upper bound: "
                              f"{y} > {GeometryValidator._YMAXCOORDS}\n")

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
            GeometryValidator._get_x_coord_error_msg(x) +
            GeometryValidator._get_y_coord_error_msg(y)
        )

        if error_msg:
            raise PointExceptionError(error_msg)

    @staticmethod
    def _validate_point_x_setter(x: float | object) -> None:
        """
        Validate x coordinate point setter.
        """
        error_msg = GeometryValidator._get_x_coord_error_msg(x)

        if error_msg:
            raise PointExceptionError(error_msg)

    @staticmethod
    def _validate_point_y_setter(y: float | object) -> None:
        """
        Validate y coordinate point setter.
        """
        error_msg = GeometryValidator._get_x_coord_error_msg(y)

        if error_msg:
            raise PointExceptionError(error_msg)

    validators: ClassVar[dict[str, Callable]] = {
        "Point_init": _validate_point_init,
        "Point_x_setter": _validate_point_x_setter,
        "Point_y_setter": _validate_point_y_setter,
    }

    @staticmethod
    def validate(validation_type: str) -> None:
        """
        Generate decorator for validation.

        Args:
            validation_type: validation type name

        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: float | object, **kwargs: float | object) -> Callable:
                validator = GeometryValidator.validators.get(validation_type)
                if validator:
                    validator(*args[1:], **kwargs)
                return func(*args, **kwargs)
            return wrapper
        return decorator
