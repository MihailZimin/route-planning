"""
Class ArcDrawer.

This module provides:
- ArcDrawer : class for drawing arc.

"""

from math import cos, pi, sin

import QCustomPlot_PyQt6 as qcp
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from core.arc import Arc
from core.point import Point


class ArcDrawer(Arc):
    """
    Class for drawing arc.
    """

    def __init__(self, center: Point, p_start: Point, p_end: Point) -> None:
        """
        Init arc drawer.
        """
        super().__init__(center, p_start, p_end)

    def convert_angle_to_horizontal(self, angle: float) -> float:
        """
        Convert angle to count it from the horizontal.

        Args:
            angle: angle which needs to be converted.

        """
        return pi / 2 - angle if angle >= 0 and angle <= pi / 2 else 2 * pi - (angle - pi / 2)

    def draw(self, map_view: qcp.QCustomPlot) -> None:
        """
        Draw arc.
        """
        arc = qcp.QCPCurve(map_view.xAxis, map_view.yAxis)
        point_count = 500
        x0 = self.center.x
        y0 = self.center.y
        rad = self.radius
        x_coord = []
        y_coord = []
        for i in range(point_count):
            delta_t = (self.angle_end - self.angle_start) / (point_count - 1)
            t = self.angle_start + i * delta_t
            x = x0 + rad * cos(t)
            y = y0 + rad * sin(t)
            x_coord.append(x)
            y_coord.append(y)

        arc.setData(x_coord, y_coord)

        arc.setPen(QPen(Qt.GlobalColor.red, 2))

        map_view.replot()
