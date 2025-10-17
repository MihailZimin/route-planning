"""
Abstract class for drawing geometry objects.

This module provides:
- ABCDrawer : abstract drawer class

"""


from abc import ABC, abstractmethod

from PyQt6.QtWidgets import QGraphicsView

from core.abstract_geometry import ABCGeo


class ABCDrawer(ABCGeo, ABC):
    """
    Abstaract drawer class.
    """

    @abstractmethod
    def draw(self, map_view: QGraphicsView) -> None:
        """
        Draw geometry object.
        """
