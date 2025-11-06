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

    def validateAccept(
            self,
            min_x_coord: float = 0,
            max_x_coord: float = 1000,
            min_y_coord: float = 0,
            max_y_coord: float = 1000,
            max_rad: float = 500
        ) -> None:
        """
        Slot for accept button with validation of parameters.

        Args:
            min_x_coord: minimum value of x coordinate on the map.
            max_x_coord: maximum value of x coordinate on the map.
            min_y_coord: minimum value of y coordinate on the map.
            max_y_coord: maximum value of y coordinate on the map.
            max_rad: maximum value of radius.

        """
        x_coord = self.xLineEdit.text()
        y_coord = self.yLineEdit.text()
        radius = self.radiusLineEdit.text()
        if not x_coord or not y_coord:
            QMessageBox.information(self, "Траектория БПЛА", "Заполните все поля")
            return
        try:
            x_coord = float(x_coord)
            y_coord = float(y_coord)
            rad = float(radius)
        except ValueError:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные параметры")
            return
        if x_coord < min_x_coord or x_coord > max_x_coord:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        if y_coord < min_y_coord or y_coord > max_y_coord:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректные координаты")
            return
        if rad < 0 or rad > max_rad:
            QMessageBox.information(self, "Траектория БПЛА", "Введите корректный радиус")
            return
        self.accept()

    def loadParams(self) -> None:
        """
        Load circle parameters.
        """
        self.nameLineEdit.setText(self._geo_object.parameters["Название"])
        self.xLineEdit.setText(str(self._geo_object.parameters["X"]))
        self.yLineEdit.setText(str(self._geo_object.parameters["Y"]))
        self.radiusLineEdit.setText(str(self._geo_object.parameters["Радиус"]))

    def setChanges(self) -> None:
        """
        Change circle parameters.
        """
        name = self.nameLineEdit.text()
        x = float(self.xLineEdit.text())
        y = float(self.yLineEdit.text())
        r = float(self.radiusLineEdit.text())
        self._geo_object.name = name
        self._geo_object.center.x = x
        self._geo_object.center.y = y
        self._geo_object.radius = r
