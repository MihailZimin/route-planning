"""
Class CircleDrawer.

This module provides:
- CircleDrawer : class for drawing circle.

"""


from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsView

from .abstract_drawer import ABCDrawer


class CircleDrawer(ABCDrawer):
    """
    Class for drawing circle.
    """

    def __init__(self) -> None:
        """
        Init circle drawer.
        """
        super().__init__()
        self.graphicsItem: QGraphicsEllipseItem = QGraphicsEllipseItem()

    def draw(
        self,
        map_view: QGraphicsView,
        x: float,
        y: float,
        rad: float
    ) -> None:
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
            x - rad / 2,
            y - rad / 2,
            rad,
            rad,
            QPen(color),
            QBrush(color)
        )

    def delete(self, map_view: QGraphicsView) -> None:
        """
        Delete Circle.

        Args:
            map_view: widget where circle is located.

        """
        scene = map_view.scene()
        scene.removeItem(self.graphicsItem)
