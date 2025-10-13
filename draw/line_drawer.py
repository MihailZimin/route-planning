"""
Class LineDrawer.

This module provides:
- LineDrawer : class for drawing line.

"""


from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsView

from .abstract_drawer import ABCDrawer


class LineDrawer(ABCDrawer):
    """
    Class for drawing line.
    """

    def __init__(self) -> None:
        """
        Init line drawer.
        """
        super().__init__()
        self.graphicsItem: QGraphicsLineItem = QGraphicsLineItem()

    def draw(
        self,
        map_view: QGraphicsView,
        begin: tuple[float, float],
        end: tuple[float, float]
    ) -> None:
        """
        Draw line.

        Args:
            map_view: widget where line will be drawn.
            begin: tuple of coordinates of line begin.
            end: tuple of coordinates of line end.

        Default line color: Red.
        """
        color = QColor(255, 0, 0)
        scene = map_view.scene()
        self.graphicsItem = scene.addLine(
            begin[0],
            begin[1],
            end[0],
            end[1],
            QPen(color)
        )

    def delete(self, map_view: QGraphicsView) -> None:
        """
        Delete line.

        Args:
            map_view: widget where line is located.
        """
        scene = map_view.scene()
        scene.removeItem(self.graphicsItem)
