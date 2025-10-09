"""
Class ArcDrawer.

This module provides:
- ArcDrawer : class for drawing arc.

"""

from .abstract_drawer import ABCDrawer


class ArcDrawer(ABCDrawer):
    """
    Class for drawing arc.
    """

    def __init__(self) -> None:
        """
        Init arc drawer.
        """
        super().__init__()

    def draw(self) -> None:
        """
        Draw arc.
        """

    def delete(self) -> None:
        """
        Delete arc.
        """
