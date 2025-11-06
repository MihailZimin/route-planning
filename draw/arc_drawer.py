"""
Class ArcDrawer.

This module provides:
- ArcDrawer : class for drawing arc.

"""

import QCustomPlot_PyQt6 as qcp

from core.arc import Arc
from core.point import Point

from .abstract_drawer import ABCDrawer


class ArcDrawer(Arc, ABCDrawer):
    """
    Class for drawing arc.
    """

    def __init__(self, center: Point, p_start: Point, p_end: Point) -> None:
        """
        Init arc drawer.
        """
        super().__init__(center, p_start, p_end)

    def draw(self, map_view: qcp.QCustomPlot) -> None:
        """
        Draw arc.
        """
