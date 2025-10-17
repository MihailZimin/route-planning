"""
Class PointDrawer.

This module provides:
- PointDrawer : class for drawing point.

"""


from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import QGraphicsView

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
        self.point_size: int = 5

    @property
    def name(self) -> str:
        """
        Return point name.
        """
        return self._name

    def draw(self, map_view: QGraphicsView) -> None:
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
        scene = map_view.scene()
        color = QColor(255, 0, 0)
        point = scene.addEllipse(
            self.x - self.point_size / 2,
            self.y - self.point_size / 2,
            self.point_size,
            self.point_size,
            QPen(color),
            QBrush(color)
        )

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        point.setPen(pen)

        if self.name:
            graphics_text = scene.addText(self.name)
            graphics_text.setPos(self.x + self.point_size, self.y - self.point_size)
            graphics_text.setDefaultTextColor(color)

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
