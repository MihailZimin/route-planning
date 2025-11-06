"""
Polygon edit dialog class.

This module provides:
- PolygonEditDialogWindow for editing polygon.

"""

from PyQt6.QtWidgets import QLineEdit, QMessageBox, QWidget

from dialog_window.base_edit_dialog import EditDialogWindow
from draw.polygon_drawer import PolygonDrawer


class PolygonEditDialogWindow(EditDialogWindow):
    """
    Class for edit polygon window.
    """

    def __init__(self, geo_object: PolygonDrawer, parent: QWidget = None) -> None:
        """
        Create polygon edit window.
        """
        self._rows: dict = {}
        super().__init__(geo_object, "dialog_window/polygon_edit_dialog.ui", parent)

    def InitializeWin(self, path: str) -> None:
        """
        Initialize polygon edit dialog window.

        Args:
            path: path to the ui file.

        """
        super().InitializeWin(path)
        self._rows["Название"] = QLineEdit()
        self.formLayout.addRow("Название", self._rows["Название"])
        for i in range(len(self._geo_object.points)):
            self._rows["X" + str(i + 1)] = QLineEdit()
            self._rows["Y" + str(i + 1)] = QLineEdit()
            self.formLayout.addRow("X" + str(i + 1), self._rows["X" + str(i + 1)])
            self.formLayout.addRow("Y" + str(i + 1), self._rows["Y" + str(i + 1)])

    def validateAccept(
            self,
            min_x_coord: float = 0,
            max_x_coord: float = 1000,
            min_y_coord: float = 0,
            max_y_coord: float = 1000
        ) -> None:
        """
        Slot for accept button with validation of parameters.

        Args:
            min_x_coord: minimum value of x coordinate on the map.
            max_x_coord: maximum value of x coordinate on the map.
            min_y_coord: minimum value of y coordinate on the map.
            max_y_coord: maximum value of y coordinate on the map.

        """
        for i in range(len(self._geo_object.points)):
            x_coord = self._rows["X" + str(i + 1)].text()
            y_coord = self._rows["Y" + str(i + 1)].text()

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
        Load polygon parameters.
        """
        self._rows["Название"].setText(self._geo_object.name)
        for i, point in enumerate(self._geo_object.points):
            self._rows["X" + str(i + 1)].setText(str(point.x))
            self._rows["Y" + str(i + 1)].setText(str(point.y))

    def setChanges(self) -> None:
        """
        Change polygon parameters.
        """
        self._geo_object.name = self._rows["Название"].text()
        for i, point in enumerate(self._geo_object.points):
            point.x = float(self._rows["X" + str(i + 1)].text())
            point.y = float(self._rows["Y" + str(i + 1)].text())
