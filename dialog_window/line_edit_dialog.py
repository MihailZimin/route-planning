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
        x1_coord = self.x1LineEdit.text()
        y1_coord = self.y1LineEdit.text()
        x2_coord = self.x2LineEdit.text()
        y2_coord = self.y2LineEdit.text()
        if not x1_coord or not y1_coord or not x2_coord or not y2_coord:
            QMessageBox.information(self, "Траектория БПЛА", "Заполните все поля")
            return
        try:
            x1_coord = float(x1_coord)
            y1_coord = float(y1_coord)
            x2_coord = float(x2_coord)
            y2_coord = float(y2_coord)
        except ValueError:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        if x1_coord < 0 or x1_coord > 1000:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        if y1_coord < 0 or y1_coord > 1000:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        if x2_coord < 0 or x2_coord > 1000:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        if y2_coord < 0 or y2_coord > 1000:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        self.accept()

    def loadParams(self) -> None:
        """
        Load line parameters.
        """
        self.nameLineEdit.setText(self._geo_object.parameters["Название"])
        self.x1LineEdit.setText(str(self._geo_object.parameters["X1"]))
        self.y1LineEdit.setText(str(self._geo_object.parameters["Y1"]))
        self.x2LineEdit.setText(str(self._geo_object.parameters["X2"]))
        self.y2LineEdit.setText(str(self._geo_object.parameters["Y2"]))

    def setChanges(self) -> None:
        """
        Change line parameters.
        """
        name = self.nameLineEdit.text()
        x1 = float(self.x1LineEdit.text())
        y1 = float(self.y1LineEdit.text())
        x2 = float(self.x2LineEdit.text())
        y2 = float(self.y2LineEdit.text())
        self._geo_object.name = name
        self._geo_object.start.x = x1
        self._geo_object.start.y = y1
        self._geo_object.end.x = x2
        self._geo_object.end.y = y2
