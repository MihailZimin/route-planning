"""Validator class for core geometry objects."""
from collections.abc import Callable
from functools import wraps
from typing import ClassVar


class GeometryValidator:
    """
    Class for data validation.
    """

    XMAXCOORDS: float =  1000.0
    XMINCOORDS: float = -1000.0
    YMAXCOORDS: float =  1000.0
    YMINCOORDS: float = -1000.0
    MINRADIUS:  float =     0.0
    MAXRADIUS:  float =  1000.0

    @staticmethod
    def _get_radius_error_msg(radius: float | object) -> str:
        """
        Get radius error message.

        Args:
            radius: radius of geometry object (circle or arc)

        Returns:
            error message

        """
        error_msg = ""
        if not isinstance(radius, (int, float)):
            error_msg += f"radius: {radius} is not a number\n"
        else:
            if radius < GeometryValidator.MINRADIUS:
                error_msg += (f"radius is lower than lower bound: "
                              f"{radius} < {GeometryValidator.MINRADIUS}")
            if radius > GeometryValidator.MAXRADIUS:
                error_msg += (f"radius is upper than upper bound: "
                              f"{radius} > {GeometryValidator.MAXRADIUS}")

        return error_msg

    validators: ClassVar[dict[str, Callable]] = {}

    @classmethod
    def validate(cls, validation_type: str) -> None:
        """
        Generate decorator for validation.

        Args:
            validation_type: validation type name

        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: float | object, **kwargs: float | object) -> Callable:
                validator = cls.validators.get(validation_type)
                if validator:
                    validator(*args[1:], **kwargs)
                return func(*args, **kwargs)
            return wrapper
        return decorator
