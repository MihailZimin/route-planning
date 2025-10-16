"""
Class LineDrawer.

This module provides:
- LineDrawer : class for drawing line.

"""


from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsView

from .abstract_drawer import ABCDrawer

from core.point import Point
from core.line import Line

class LineDrawer(ABCDrawer, Line):
    """
    Class for drawing line.
    """

    def __init__(self, start: Point, end: Point, name: str) -> None:
        """
        Init line drawer.
        """
        super().__init__(start, end)
        self._name = name

    @property
    def name(self) -> str:
        """
        Return line name.
        """
        return self._name

    def draw(self, map_view: QGraphicsView) -> None:
        """
        Draw line.

        Args:
            map_view: widget where line will be drawn.
            begin: tuple of coordinates of line begin.
            end: tuple of coordinates of line end.

        Default line color: Red.

        """
        color = QColor(255, 0, 0)
        scene = map_view.scene()
        scene.addLine(
            self.start.x,
            self.start.y,
            self.end.x,
            self.end.y,
            QPen(color)
        )

    @property
    def parameters(self) -> dict:
        """
        Return line parameters for GUI display. 
        """
        params = {
            "Название:": self.name,
            "X1:": self.start.x,
            "Y1:": self.start.y,
            "X2:": self.end.x,
            "Y2:": self.end.y
        }

        return params
