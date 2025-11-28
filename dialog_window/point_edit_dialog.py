"""
Point edit window class.

This module provides:
- PointEditDialogWindow for editing point.

"""


from PyQt6.QtWidgets import QMessageBox, QWidget

from dialog_window.base_edit_dialog import EditDialogWindow
from draw.point_drawer import PointDrawer


class PointEditDialogWindow(EditDialogWindow):
    """
    Class for edit point window.
    """

    def __init__(self, point: PointDrawer, parent: QWidget = None) -> None:
        """
        Create point edit window.
        """
        super().__init__(point, "dialog_window/point_edit_dialog.ui", parent)

    def validateAccept(self) -> None:
        """
        Slot for accept button with validation of parameters.
        """
        name = self.nameLineEdit.text()
        try:
            x = float(self.xLineEdit.text())
            y = float(self.yLineEdit.text())
            self._geo_object.name = name
            self._geo_object.x = x
            self._geo_object.y = y
        except ValueError as error:
            QMessageBox.information(self, "Траектория БПЛА", str(error))
            return
        self.accept()

    def loadParams(self) -> None:
        """
        Load point parameters.
        """
        self.nameLineEdit.setText(self._geo_object.name)
        self.xLineEdit.setText(str(self._geo_object.x))
        self.yLineEdit.setText(str(self._geo_object.y))
