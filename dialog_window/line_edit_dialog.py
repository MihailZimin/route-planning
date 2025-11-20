"""
Line edit window class.

This module provides:
- LineEditDialogWindow for editing line.

"""

from PyQt6.QtWidgets import QMessageBox, QWidget

from dialog_window.base_edit_dialog import EditDialogWindow
from draw.line_drawer import LineDrawer


class LineEditDialogWindow(EditDialogWindow):
    """
    Class for edit line window.
    """

    def __init__(self, geo_object: LineDrawer, parent: QWidget = None) -> None:
        """
        Create line edit window.
        """
        super().__init__(geo_object, "dialog_window/line_edit_dialog.ui", parent)

    def validateAccept(self) -> None:
        """
        Slot for accept button with validation of parameters.
        """
        name = self.nameLineEdit.text()
        try:
            x1 = float(self.xBegCoordLineEdit.text())
            y1 = float(self.yBegCoordLineEdit.text())
            x2 = float(self.xEndCoordLineEdit.text())
            y2 = float(self.yEndCoordLineEdit.text())
            self._geo_object.name = name
            self._geo_object.start.x = x1
            self._geo_object.start.y = y1
            self._geo_object.end.x = x2
            self._geo_object.end.y = y2
        except ValueError as error:
            QMessageBox.information(self, "Траектория БПЛА", str(error))
            return
        self.accept()

    def loadParams(self) -> None:
        """
        Load line parameters.
        """
        self.nameLineEdit.setText(self._geo_object.name)
        self.xBegCoordLineEdit.setText(str(self._geo_object.start.x))
        self.yBegCoordLineEdit.setText(str(self._geo_object.start.y))
        self.xEndCoordLineEdit.setText(str(self._geo_object.end.x))
        self.yEndCoordLineEdit.setText(str(self._geo_object.end.y))
