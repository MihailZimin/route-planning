"""
Polygon point edit dialog class.

This module provides:
- PolygonPointEditDialogWindow for editing polygon point.

"""

from PyQt6.QtWidgets import QWidget

from core.point import Point
from dialog_window.base_edit_dialog import EditDialogWindow


class PolygonPointEditDialogWindow(EditDialogWindow):
    """
    Class for editing polygon point.
    """

    def __init__(self, geo_object: Point, title: str, parent: QWidget = None) -> None:
        """
        Create polygon point edit window.
        """
        super().__init__(geo_object, "dialog_window/polygon_point_edit_dialog.ui", parent)
        self.pointParams.setTitle(title)

    def validateAccept(self) -> None:
        """
        Slot for accept button with parameters validation.
        """
        self.accept()

    def loadParams(self) -> None:
        """
        Load current point parameters.
        """
        self.xCoordLineEdit.setText(str(self._geo_object.x))
        self.yCoordLineEdit.setText(str(self._geo_object.y))

    def setChanges(self) -> None:
        """
        Change point parameters.
        """
        x_coord = float(self.xCoordLineEdit.text())
        y_coord = float(self.yCoordLineEdit.text())
        self._geo_object.x = x_coord
        self._geo_object.y = y_coord
