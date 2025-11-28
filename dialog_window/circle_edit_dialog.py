"""
Circle edit window class.

This module provides:
- CircleEditDialogWindow for editing circle.

"""

from PyQt6.QtWidgets import QMessageBox, QWidget

from dialog_window.base_edit_dialog import EditDialogWindow
from draw.circle_drawer import CircleDrawer


class CircleEditDialogWindow(EditDialogWindow):
    """
    Class for edit circle window.
    """

    def __init__(self, point: CircleDrawer, parent: QWidget = None) -> None:
        """
        Create circle edit window.
        """
        super().__init__(point, "dialog_window/circle_edit_dialog.ui", parent)

    def validateAccept(self) -> None:
        """
        Slot for accept button with validation of parameters.
        """
        name = self.nameLineEdit.text()
        try:
            x = float(self.xLineEdit.text())
            y = float(self.yLineEdit.text())
            r = float(self.radiusLineEdit.text())
            self._geo_object.name = name
            self._geo_object.center.x = x
            self._geo_object.center.y = y
            self._geo_object.radius = r
        except ValueError as error:
            QMessageBox.information(self, "Траектория БПЛА", str(error))
            return
        self.accept()

    def loadParams(self) -> None:
        """
        Load circle parameters.
        """
        self.nameLineEdit.setText(self._geo_object.name)
        self.xLineEdit.setText(str(self._geo_object.center.x))
        self.yLineEdit.setText(str(self._geo_object.center.y))
        self.radiusLineEdit.setText(str(self._geo_object.radius))
