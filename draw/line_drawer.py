"""
Class LineDrawer.

This module provides:
- LineDrawer : class for drawing line.

"""


import QCustomPlot_PyQt6 as qcp
from PyQt6.QtGui import QBrush, QColor, QPen

from core.line import Line
from core.point import Point

from .abstract_drawer import ABCDrawer


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

    def draw(self, map_view: qcp.QCustomPlot) -> None:
        """
        Draw line.

        Args:
            map_view: widget where line will be drawn.
            begin: tuple of coordinates of line begin.
            end: tuple of coordinates of line end.

        Default line color: Red.

        """
        color = QColor(255, 0, 0)
        line = map_view.addGraph()
        line.setData([self.start.x, self.end.x], [self.start.y, self.end.y])

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        point_style = qcp.QCPScatterStyle()
        point_style.setShape(qcp.QCPScatterStyle.ScatterShape.ssCircle)
        point_style.setPen(pen)
        point_style.setBrush(QBrush(color))
        point_style.setSize(self.start.point_size)

        line.setScatterStyle(point_style)
        line.setPen(QPen(color, 2))

        map_view.replot()

    @property
    def parameters(self) -> dict:
        """
        Return line parameters for GUI display.
        """
        return {
            "Название:": self.name,
            "X1:": self.start.x,
            "Y1:": self.start.y,
            "X2:": self.end.x,
            "Y2:": self.end.y
        }
