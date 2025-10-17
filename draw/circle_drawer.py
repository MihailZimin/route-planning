"""
Class CircleDrawer.

This module provides:
- CircleDrawer : class for drawing circle.

"""


from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import QGraphicsView

from core.circle import Circle
from core.point import Point

from .abstract_drawer import ABCDrawer


class CircleDrawer(ABCDrawer, Circle):
    """
    Class for drawing circle.
    """

    def __init__(self, center: Point, radius: float, name: str) -> None:
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

    def draw(self, map_view: QGraphicsView) -> None:
        """
        Draw circle.

        Args:
            map_view: widget where circle will be drawn.
            x: x-coordinate of circle.
            y: y-coordinate of circle.
            rad: circle radius.

        Default circle color: Red.

        """
        scene = map_view.scene()
        color = QColor(255, 0, 0)
        circle = scene.addEllipse(
            self.center.x - self.radius / 2,
            self.center.y - self.radius / 2,
            self.radius,
            self.radius,
            QPen(color),
            QBrush(color)
        )

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        circle.setPen(pen)

    @property
    def parameters(self) -> dict:
        """
        Return line parameters for GUI display.
        """
        return {
            "Название:": self.name,
            "X:": self.center.x,
            "Y:": self.center.y,
            "Радиус:": self.radius
        }
