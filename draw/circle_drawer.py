"""
Class CircleDrawer.

This module provides:
- CircleDrawer : class for drawing circle.

"""


from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsView

from .abstract_drawer import ABCDrawer

from core.point import Point
from core.circle import Circle

class CircleDrawer(ABCDrawer, Circle):
    """
    Class for drawing circle.
    """

    def __init__(self, center: Point, radius: float, name: str) -> None:
        """
        Init circle drawer.
        """
        super().__init__(center, radius)
        self.graphicsItem: QGraphicsEllipseItem = QGraphicsEllipseItem()
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
        self.graphicsItem = scene.addEllipse(
            self.center.x - self.radius / 2,
            self.center.y - self.radius / 2,
            self.radius,
            self.radius,
            QPen(color),
            QBrush(color)
    )

    @property
    def parameters(self) -> tuple:
        """
        Return line parameters for GUI display. 
        """
        params = {
            "Название:": self.name,
            "X:": self.center.x,
            "Y:": self.center.y,
            "Радиус:": self.radius
        }

        return params

    def delete(self, map_view: QGraphicsView) -> None:
        """
        Delete Circle.

        Args:
            map_view: widget where circle is located.

        """
        scene = map_view.scene()
        scene.removeItem(self.graphicsItem)
