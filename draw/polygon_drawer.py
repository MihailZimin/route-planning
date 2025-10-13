"""
Class PolygonDrawer.

This module provides:
- PolygonDrawer : class for drawing polygon.

"""

from .abstract_drawer import ABCDrawer


class PolygonDrawer(ABCDrawer):
    """
    Class for drawing polygon.
    """

    def __init__(self) -> None:
        """
        Init polygon drawer.
        """
        super().__init__()

    def draw(self) -> None:
        """
        Draw Polygon.
        """

    def delete(self) -> None:
        """
        Delete polygon.
        """
