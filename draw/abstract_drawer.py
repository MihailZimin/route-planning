"""Abstract class for drawing geometry objects.

This module provides:
- ABCDrawer : abstract drawer class

"""


from abc import ABC, abstractmethod

from core.abstract_geometry import ABCGeo

from PyQt6.QtWidgets import QGraphicsView

class ABCDrawer(ABCGeo, ABC):
    """
    Abstaract drawer class.
    """

    @abstractmethod
    def draw(self, map_view: QGraphicsView) -> None:
        """
        Draw geometry object.
        """

    @abstractmethod
    def delete(self, map_view: QGraphicsView) -> None:
        """
        Delete geometry object.
        """
