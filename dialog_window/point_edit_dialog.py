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
        min_x_coord = 0
        max_x_coord = 1000
        min_y_coord = 0
        max_y_coord = 1000

        x_coord = self.xLineEdit.text()
        y_coord = self.yLineEdit.text()
        if not x_coord or not y_coord:
            QMessageBox.information(self, "Траектория БПЛА", "Заполните все поля")
            return
        try:
            x_coord = float(x_coord)
            y_coord = float(y_coord)
        except ValueError:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        if x_coord < min_x_coord or x_coord > max_x_coord:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        if y_coord < min_y_coord or y_coord > max_y_coord:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        self.accept()

    def loadParams(self) -> None:
        """
        Load point parameters.
        """
        self.nameLineEdit.setText(self._geo_object.parameters["Название"])
        self.xLineEdit.setText(str(self._geo_object.parameters["X"]))
        self.yLineEdit.setText(str(self._geo_object.parameters["Y"]))

    def setChanges(self) -> None:
        """
        Change point parameters.
        """
        name = self.nameLineEdit.text()
        x = float(self.xLineEdit.text())
        y = float(self.yLineEdit.text())
        self._geo_object.name = name
        self._geo_object.x = x
        self._geo_object.y = y
