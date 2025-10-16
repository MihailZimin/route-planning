"""
Class PointDrawer.

This module provides:
- PointDrawer : class for drawing point.

"""


from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsView

from .abstract_drawer import ABCDrawer

from core.point import Point

class PointDrawer(ABCDrawer, Point):
    """
    Class for drawing point.
    """

    def __init__(self, x: float = 0, y: float = 0, name: str = "") -> None:
        """
        Init point drawer.
        """
        super().__init__(x, y)
        self.graphicsItem: QGraphicsEllipseItem = QGraphicsEllipseItem()
        self.graphicsText: QGraphicsTextItem = QGraphicsTextItem()
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
        self.graphicsItem = scene.addEllipse(
            self.x - self.point_size / 2,
            self.y - self.point_size / 2,
            self.point_size,
            self.point_size,
            QPen(color),
            QBrush(color)
        )

        if self.name:
            self.graphicsText = scene.addText(self.name)
            self.graphicsText.setPos(self.x + self.point_size, self.y - self.point_size)
            self.graphicsText.setDefaultTextColor(color)

    @property
    def parameters(self) -> tuple:
        """
        Return line parameters for GUI display. 
        """
        params = {
            "Название:": self.name,
            "X:": self.x,
            "Y:": self.y
        }

        return params

    def delete(self, map_view: QGraphicsView) -> None:
        """
        Delete point from map.

        Args:
            map_view: widget where point is located.

        """
        scene = map_view.scene()
        scene.removeItem(self.graphicsItem)
        scene.removeItem(self.graphicsText)
