"""
Edit window class.

This module provides:
- EditDialogWindow for editing geometry object.

"""


from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from draw.abstract_drawer import ABCDrawer


class EditDialogWindow(QDialog):
    """
    Edit window class for editing geo objects.
    """

    def __init__(self, geo_object : ABCDrawer, parent: QWidget = None) -> None:
        """
        Create edit window object.
        """
        super().__init__(parent)
        self._geo_object = geo_object
        self.widgets : dict[str, QLineEdit] = {}
        self.InitializeWin()
        self.loadParams()

    def InitializeWin(self) -> None:
        """
        Initialize edit window.
        """
        self.setWindowTitle("Редактирование объекта")
        self.setWindowIcon(QIcon("./pict_trajectory/drone.png"))
        self.setMinimumWidth(400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        info = QGroupBox("Параметры объекта")
        self.info_layout = QFormLayout()
        info.setLayout(self.info_layout)

        self.addEditLines()
        layout.addWidget(info)
        layout.addStretch()

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def addEditLines(self) -> None:
        """
        Create edit lines.
        """
        if self._geo_object.type == "Point":
            self.widgets["name"] = QLineEdit()
            self.widgets["name"].setPlaceholderText("Введите название")
            self.info_layout.addRow("Название", self.widgets["name"])

            self.widgets["x"] = QLineEdit()
            self.widgets["x"].setPlaceholderText("Введите координату X")
            self.info_layout.addRow("X:", self.widgets["x"])

            self.widgets["y"] = QLineEdit()
            self.widgets["y"].setPlaceholderText("Введите координату Y")
            self.info_layout.addRow("Y:", self.widgets["y"])

        if self._geo_object.type == "Circle":
            self.widgets["name"] = QLineEdit()
            self.widgets["name"].setPlaceholderText("Введите название")
            self.info_layout.addRow("Название", self.widgets["name"])

            self.widgets["x"] = QLineEdit()
            self.widgets["x"].setPlaceholderText("Введите координату X")
            self.info_layout.addRow("X:", self.widgets["x"])

            self.widgets["y"] = QLineEdit()
            self.widgets["y"].setPlaceholderText("Введите координату Y")
            self.info_layout.addRow("Y:", self.widgets["y"])

            self.widgets["R"] = QLineEdit()
            self.widgets["R"].setPlaceholderText("Введите радиус")
            self.info_layout.addRow("R:", self.widgets["R"])
        

    def loadParams(self) -> None:
        """
        Load current parameters of geo object.
        """
        for val, cur_val in zip(self.widgets.keys(), self._geo_object.parameters.values(), strict=False):
            self.widgets[val].setText(str(cur_val))

    def getChanges(self) -> dict:
        """
        Return new parameters of geo object.
        """
        return self.widgets
