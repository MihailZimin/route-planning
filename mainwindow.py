import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from styles import BUTTON_STYLE1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """
        Инициализация окна
        """
        uic.loadUi("trajectory.ui", self)
        self.setFixedSize(self.size())
        self.addMenubar()

    def addMenubar(self):
        """
        Создание собственного меню
        """
        menu = self.menuBar
        button_box = QWidget()
        button_layout = QHBoxLayout(button_box)
        button_layout.setContentsMargins(10, 0, 10, 0)
        button_layout.setSpacing(5)

        self.start_btn = QPushButton("Старт")
        self.chose_map_btn = QPushButton("Выбрать карту")
        self.save_map_btn = QPushButton("Сохранить карту")
        self.change_map_btn = QPushButton("Изменить карту")
        self.exit_btn = QPushButton("Выход")

        self.exit_btn.clicked.connect(self.closeWindow)
        self.chose_map_btn.clicked.connect(self.selectFile)
        self.start_btn.clicked.connect(self.startTrajectory)

        buttons = [
            (self.start_btn, "PictTrajectory/start.png"),
            (self.chose_map_btn, "PictTrajectory/map.png"),
            (self.save_map_btn, "PictTrajectory/save.png"),
            (self.change_map_btn, "PictTrajectory/change.png"),
            (self.exit_btn, "PictTrajectory/exit.png")
        ]

        for btn, pict in buttons:
            btn.setStyleSheet(BUTTON_STYLE1)
            btn.setIcon(QIcon(pict))
            btn.setIconSize(QSize(30, 30))
            btn.setFixedHeight(35)
            btn.setFixedWidth(185)
            button_layout.addWidget(btn)

        menu.setCornerWidget(button_box, Qt.Corner.TopRightCorner)

    def closeWindow(self):
        """
        Слот для выхода из приложения
        """
        self.close()

    def selectFile(self):
        """
        Слот для выбора карты
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "")
        if file_path:
            self.statusBar.showMessage(f"Выбран файл: {file_path}")
            self.proccessSelectedFile()

    def proccessSelectedFile(self):
        """
        Метод для обработки выбранной карты
        """
        pass

    def startTrajectory(self):
        """
        Слот для запуска построения траектории
        """
        self.statusBar.showMessage("Процесс построения траектории запущен")
        self.showAnimation()

    def showAnimation(self):
        """
        Метод для построения траектории
        """
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()