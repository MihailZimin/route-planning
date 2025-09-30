"""Point geometry class for core."""
import json

from .abstract_geometry import ABCGeo


class Point(ABCGeo):
    """
    Point core class.
    """

    def __init__(self, x: float, y: float) -> None:
        """
        Initialize 2D point.

        Args:
            x: X-coordinate of the point
            y: Y-coordinate of the point

        """
        self._x = x
        self._y = y

    def save(self) -> str:
        """
        Return JSON string representation of the object.
        """
        return json.dumps((self._x, self._y))

    @property
    def x(self) -> float:
        """
        Return x coordinate of point.
        """
        return self._x

    @x.setter
    def x(self, x_coord: float) -> None:
        """
        Set x coordinate of point.

        Args:
            x_coord: new X-coordinate of the point

        """
        self._x = x_coord

    @property
    def y(self) -> float:
        """
        Returns y coordinate of point.
        """
        return self._y

    @y.setter
    def y(self, y_coord: float) -> None:
        """
        Set y coordinate of point.

        Args:
            y_coord: new Y-coordinate of the point

        """
        self._y = y_coord

    def __str__(self) -> str:
        """
        Return string representation of point.
        """
        return f"({self._x}, {self._y})"
