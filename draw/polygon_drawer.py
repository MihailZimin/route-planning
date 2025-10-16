"""
Class PolygonDrawer.

This module provides:
- PolygonDrawer : class for drawing polygon.

"""

from .abstract_drawer import ABCDrawer

from PyQt6.QtWidgets import QGraphicsView

class PolygonDrawer(ABCDrawer):
    """
    Class for drawing polygon.
    """

    def __init__(self) -> None:
        """
        Init polygon drawer.
        """
        super().__init__()

    def draw(self, map_view: QGraphicsView) -> None:
        """
        Draw Polygon.
        """

    def delete(self, map_view: QGraphicsView) -> None:
        """
        Delete polygon.
        """
