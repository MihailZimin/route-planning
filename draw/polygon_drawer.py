"""
Class PolygonDrawer.

This module provides:
- PolygonDrawer : class for drawing polygon.

"""

import QCustomPlot_PyQt6 as qcp
from PyQt6.QtGui import QBrush, QColor, QPen

from core.point import Point
from core.polygon import Polygon

from .abstract_drawer import ABCDrawer


class PolygonDrawer(Polygon, ABCDrawer):
    """
    Class for drawing polygon.
    """

    def __init__(self, points: list[Point], name: str = "") -> None:
        """
        Init polygon drawer.
        """
        super().__init__(points)
        self._name = name
        self._type : str = "Polygon"

    @property
    def name(self) -> str:
        """
        Return polygon name.
        """
        return self._name

    @property
    def type(self) -> str:
        """
        Return geo object type.
        """
        return self._type

    def draw(self, map_view: qcp.QCustomPlot) -> None:
        """
        Draw Polygon.
        """
        x_coords = []
        y_coords = []

        for point in self.points:
            x_coords.append(point.x)
            y_coords.append(point.y)

        polygon = qcp.QCPCurve(map_view.xAxis, map_view.yAxis)
        polygon.setData(x_coords, y_coords)

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        color = QColor(0, 0, 255)
        point_style = qcp.QCPScatterStyle()
        point_style.setShape(qcp.QCPScatterStyle.ScatterShape.ssCircle)
        point_style.setPen(pen)
        point_style.setBrush(QBrush(color))
        point_style.setSize(5)

        polygon.setScatterStyle(point_style)
        polygon.setPen(QPen(color, 2))
        polygon.setBrush(QBrush(color))

        map_view.replot()

    @property
    def parameters(self) -> dict:
        """
        Return polygon parameters for GUI display.
        """
        params = {"Название:": self.name}
        for i, point in enumerate(self.points):
            point_label = "Точка " + str(i + 1)
            params[point_label] = str(point)

        return params
