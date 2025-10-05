"""Class for GUI.

This module provides:
- MainWindow: class for main window of app.

"""


import sys

from PyQt6 import uic
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow


class MainWindow(QMainWindow):
    """
    Main window class.
    """

    def __init__(self) -> None:
        """
        Initialize MainWindow object.
        """
        super().__init__()
        self.initializeUI()

    def initializeUI(self) -> None:
        """
        Initionalization of MainWindow.
        """
        uic.loadUi("trajectory.ui", self)
        self.setGeometry(300, 100, 900, 550)
        self.setMaximumSize(QSize(1000, 1000))
        self.setMinimumSize(QSize(400, 300))

        self.showStatAction.triggered.connect(self.showStatistic)
        self.showParamsAction.triggered.connect(self.showParams)
        self.choseMapAction.triggered.connect(self.processFile)
        self.changeMapAction.triggered.connect(self.changeMap)
        self.startAction.triggered.connect(self.startTrajectory)

    def closeWindow(self) -> None:
        """
        Slot for closing app.
        """
        self.close()

    def showStatistic(self) -> None:
        """
        Slot for showing statistic of flight.
        """
        self.stackedWidget.setCurrentIndex(0)

    def showParams(self) -> None:
        """
        Slot for showing parametrs of flight.
        """
        self.stackedWidget.setCurrentIndex(1)

    def changeMap(self) -> None:
        """
        Slot for changing map.
        """
        self.stackedWidget.setCurrentIndex(2)

    def processFile(self) -> None:
        """
        Slot for chosing map.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "")
        if file_path:
            self.statusBar.showMessage(f"Выбран файл: {file_path}")

    def startTrajectory(self) -> None:
        """
        Slot for starting animation of flight.
        """
        self.statusBar.showMessage("Процесс построения траектории запущен")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
