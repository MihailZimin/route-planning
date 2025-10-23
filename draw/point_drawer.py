"""
Class PointDrawer.

This module provides:
- PointDrawer : class for drawing point.

"""


import QCustomPlot_PyQt6 as qcp
from PyQt6.QtGui import QBrush, QColor, QFont, QPen

from core.point import Point

from .abstract_drawer import ABCDrawer


class PointDrawer(ABCDrawer, Point):
    """
    Class for drawing point.
    """

    def __init__(self, x: float = 0, y: float = 0, name: str = "") -> None:
        """
        Init point drawer.
        """
        super().__init__(x, y)
        self._name = name
        self.point_size: int = 8

    @property
    def name(self) -> str:
        """
        Return point name.
        """
        return self._name

    def draw(self, map_view: qcp.QCustomPlot) -> None:
        """
        Draw point.

        Args:
            map_view: widget where point will be drawn.
            x: x-coordinate of point.
            y: y-coordinate of point.
            name: point name.
            point_size: point size (default: 5)

        Default point color: Red.

        """
        color = QColor(255, 0, 0)
        point = qcp.QCPItemEllipse(map_view)

        point.topLeft.setCoords(self.x - self.point_size/2, self.y + self.point_size/2)
        point.bottomRight.setCoords(self.x + self.point_size/2, self.y - self.point_size/2)

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        point.setPen(pen)
        point.setBrush(QBrush(QColor(color)))

        if self.name:
            text_item = qcp.QCPItemText(map_view)
            text_item.position.setCoords(self.x + 2*self.point_size, self.y + 2*self.point_size)
            text_item.setText(self.name)
            text_item.setFont(QFont("Arial", 8))

        map_view.replot()

    @property
    def parameters(self) -> dict:
        """
        Return line parameters for GUI display.
        """
        return {
            "Название:": self.name,
            "X:": self.x,
            "Y:": self.y
        }
