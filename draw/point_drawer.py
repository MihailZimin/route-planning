"""
Class PointDrawer.

This module provides:
- PointDrawer : class for drawing point.

"""


from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsView

from .abstract_drawer import ABCDrawer


class PointDrawer(ABCDrawer):
    """
    Class for drawing point.
    """

    def __init__(self) -> None:
        """
        Init point drawer.
        """
        super().__init__()
        self.graphicsItem: QGraphicsEllipseItem = QGraphicsEllipseItem()
        self.graphicsText: QGraphicsTextItem = QGraphicsTextItem()

    def draw(
        self,
        map_view: QGraphicsView,
        x: float,
        y: float,
        name: str,
        point_size: int = 5,
    ) -> None:
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
            x - point_size / 2,
            y - point_size / 2,
            point_size,
            point_size,
            QPen(color),
            QBrush(color)
        )

        if name:
            self.graphicsText = scene.addText(name)
            self.graphicsText.setPos(x + point_size, y - point_size)
            self.graphicsText.setDefaultTextColor(color)

    def delete(self, map_view: QGraphicsView) -> None:
        """
        Delete point from map.

        Args:
            map_view: widget where point is located.

        """
        scene = map_view.scene()
        scene.removeItem(self.graphicsItem)
        scene.removeItem(self.graphicsText)
