"""
Class CircleDrawer.

This module provides:
- CircleDrawer : class for drawing circle.

"""


import QCustomPlot_PyQt6 as qcp
from PyQt6.QtGui import QBrush, QColor, QPen

from core.circle import Circle
from core.point import Point

from .abstract_drawer import ABCDrawer


class CircleDrawer(ABCDrawer, Circle):
    """
    Class for drawing circle.
    """

    _type : str = "Circle"
    def __init__(self, center: Point, radius: float, name: str = "") -> None:
        """
        Init circle drawer.
        """
        super().__init__(center, radius)
        self._name = name

    @property
    def name(self) -> str:
        """
        Return circle name.
        """
        return self._name

    @name.setter
    def name(self, name : str) -> None:
        """
        Set circle name.
        """
        self._name = name

    @property
    def type(self) -> str:
        """
        Return geo object type.
        """
        return CircleDrawer._type

    def draw(self, map_view: qcp.QCustomPlot) -> None:
        """
        Draw circle.

        Args:
            map_view: widget where circle will be drawn.
            x: x-coordinate of circle.
            y: y-coordinate of circle.
            rad: circle radius.

        Default circle color: Red.

        """
        color = QColor(255, 0, 0)
        circle = qcp.QCPItemEllipse(map_view)

        circle.topLeft.setCoords(self.center.x - self.radius, self.center.y + self.radius)
        circle.bottomRight.setCoords(self.center.x + self.radius, self.center.y - self.radius)

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        circle.setPen(pen)
        circle.setBrush(QBrush(QColor(color)))

        map_view.replot()

    @property
    def parameters(self) -> dict:
        """
        Return line parameters for GUI display.
        """
        return {
            "Название": self.name,
            "X": self.center.x,
            "Y": self.center.y,
            "Радиус": self.radius
        }
