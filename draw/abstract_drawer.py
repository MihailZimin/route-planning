"""
Abstract class for drawing geometry objects.

This module provides:
- ABCDrawer : abstract drawer class

"""

from abc import ABC, abstractmethod

import QCustomPlot_PyQt6 as qcp

from core.abstract_geometry import ABCGeo


class ABCDrawer(ABCGeo, ABC):
    """
    Abstaract drawer class.
    """

    @abstractmethod
    def draw(self, map_view: qcp.QCustomPlot) -> None:
        """
        Draw geometry object.
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return geo object name.
        """

    @property
    @abstractmethod
    def type(self) -> str:
        """
        Return geo object type.
        """

    @property
    @abstractmethod
    def parameters(self) -> dict:
        """
        Return object parameters for GUI display.
        """
