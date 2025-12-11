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

    def draw(self, map_view: qcp.QCustomPlot, color:Qt.GlobalColor=Qt.GlobalColor.red) -> None:
        """
        Draw arc.

        Args:
            map_view: widget where arc will be drawn.
            color: color of arc.

        Default arc color: Red.

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

        arc.setPen(QPen(color, 2))

        map_view.replot()

    def get_progress_points(self, progress: float) -> list[Point]:
        """
        Get points for animation drawing.

        Args:
            progress: animation progress (0 <= progress <= 1).
            point_count: amount of points in arc part.

        Returns:
            Points of arc from start to animation progress.

        """
        if progress <= 0.0:
            return [Point(self.p_start.x, self.p_start.y)]

        x0 = self.center.x
        y0 = self.center.y
        rad = self.radius

        total_angle = self.angle_end - self.angle_start
        total_length = rad * abs(total_angle)

        num_points = max(100, min(500, int(total_length/2)))

        points = []
        for i in range(num_points + 1):

            point_progress = i / num_points
            if point_progress > progress:
                break
            point_length = total_length * point_progress
            point_angle = self.angle_start + (point_length / rad) * (1 if total_angle >= 0 else -1)

            x = x0 + rad * cos(point_angle)
            y = y0 + rad * sin(point_angle)
            points.append(Point(x, y))

        return points