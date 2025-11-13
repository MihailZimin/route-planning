"""
Polygon edit dialog class.

This module provides:
- PolygonEditDialogWindow for editing polygon.

"""

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMessageBox, QWidget

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

    def initializeWin(self, path: str) -> None:
        """
        Initialize polygon edit dialog window.

        Args:
            path: path to the ui file.

        """
        super().initializeWin(path)
        self._rows["Название"] = QLineEdit()
        self.formLayout.addRow("Название", self._rows["Название"])

        for i in range(len(self._geo_object.points)):
            point_widget = QWidget()
            point_layout = QHBoxLayout(point_widget)
            point_layout.setContentsMargins(0, 0, 0, 0)

            point_label = QLabel("Точка " + str(i + 1) + ":")
            point_layout.addWidget(point_label)

            x_coord_label = QLabel("X: ")
            point_layout.addWidget(x_coord_label)
            self._rows["X" + str(i + 1)] = QLineEdit()
            point_layout.addWidget(self._rows["X" + str(i + 1)])

            y_coord_label = QLabel("Y: ")
            point_layout.addWidget(y_coord_label)
            self._rows["Y" + str(i + 1)] = QLineEdit()
            point_layout.addWidget(self._rows["Y" + str(i + 1)])

            point_layout.addStretch()

            self.formLayout.addRow(point_widget)

    def validateAccept(self) -> None:
        """
        Slot for accept button with validation of parameters.
        """
        min_x_coord = 0
        max_x_coord = 1000
        min_y_coord = 0
        max_y_coord = 1000

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
