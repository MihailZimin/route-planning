"""
Edit window class.

This module provides:
- EditDialogWindow for editing geometry object.

"""


from PyQt6 import uic
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QDialog, QMessageBox, QWidget

from draw.point_drawer import PointDrawer


class PointEditDialogWindow(QDialog):
    """
    Class for edit point window.
    """

    def __init__(self, point: PointDrawer, parent: QWidget = None) -> None:
        """
        Create point edit window.
        """
        super().__init__(parent)
        self._point = point
        self.InitializeUI()

    def InitializeUI(self) -> None:
        """
        Initialize point edit dialog win.
        """
        uic.loadUi("main_window/point_edit_dialog.ui", self)
        self.setMinimumSize(QSize(400, 210))
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.validateAccept)
        self.buttonBox.rejected.connect(self.reject)
        self.loadParams()

    def validateAccept(self) -> None:
        """
        Slot for accept button with validation of parameters.
        """
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
        if x_coord < 0 or x_coord > 1000:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        if y_coord < 0 or y_coord > 1000:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        self.accept()

    def loadParams(self) -> None:
        """
        Load point parameters.
        """
        self.nameLineEdit.setText(self._point.parameters["Название"])
        self.xLineEdit.setText(str(self._point.parameters["X"]))
        self.yLineEdit.setText(str(self._point.parameters["Y"]))

    def setChanges(self) -> None:
        """
        Change point parameters.
        """
        name = self.nameLineEdit.text()
        x = float(self.xLineEdit.text())
        y = float(self.yLineEdit.text())
        self._point.name = name
        self._point.x = x
        self._point.y = y
