"""Abstract class for drawing geometry objects.

This module provides:
- ABCDrawer : abstract drawer class

"""


from abc import ABC, abstractmethod


class ABCDrawer(ABC):
    """
    Abstaract drawer class.
    """

    @abstractmethod
    def draw(self) -> None:
        """
        Draw geometry object.
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Delete geometry object.
        """
