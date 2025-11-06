"""Validator class for Line."""
from collections.abc import Callable
from typing import ClassVar

from core.point import Point

from .data_validator import GeometryValidator


class LineExceptionError(Exception):
    """
    Custom exception for Line validation errors.
    """


class LineValidator(GeometryValidator):
    """
    Class for Line validation.
    """

    @staticmethod
    def _validate_line_init(start: Point, end: Point) -> None:
        """
        Validate line.

        Args:
            start: start point of line
            end: end point of line

        """
        error_msg = ""
        if not isinstance(start, Point):
            error_msg += "start is not point type\n"
        if not isinstance(end, Point):
            error_msg += "end is not point type\n"

        if error_msg:
            raise LineExceptionError(error_msg)


    @staticmethod
    def _validate_start_setter(start: Point) -> None:
        """
        Validate start point of line.
        """
        error_msg = ""
        if not isinstance(start, Point):
            error_msg += "start is not point type\n"

        if error_msg:
            raise LineExceptionError(error_msg)

    @staticmethod
    def _validate_end_setter(end: Point) -> None:
        """
        Validate end point of line.
        """
        error_msg = ""
        if not isinstance(end, Point):
            error_msg += "start is not point type\n"

        if error_msg:
            raise LineExceptionError(error_msg)


    validators: ClassVar[dict[str, Callable]] = {
        "Line_init": _validate_line_init,
        "Line_start_setter": _validate_start_setter,
        "Line_end_setter": _validate_end_setter,
    }
