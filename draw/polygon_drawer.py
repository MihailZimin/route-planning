"""
Class PolygonDrawer.

This module provides:
- PolygonDrawer : class for drawing polygon.

"""

from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QBrush, QColor, QPolygonF
from PyQt6.QtWidgets import QGraphicsPolygonItem, QGraphicsView

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

    @property
    def name(self) -> str:
        """
        Return polygon name.
        """
        return self._name

    def draw(self, map_view: QGraphicsView) -> None:
        """
        Draw Polygon.
        """
        points_to_draw = []
        for point in self.points:
            p = QPointF(point.x, point.y)
            points_to_draw.append(p)

        polygon = QPolygonF(points_to_draw)
        brush = QBrush(QColor(0, 0, 255, 100))
        polygon_to_draw = QGraphicsPolygonItem(polygon)
        polygon_to_draw.setBrush(brush)
        scene = map_view.scene()
        scene.addItem(polygon_to_draw)

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
