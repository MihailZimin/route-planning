"""Class for GUI.

This module provides:
- MainWindow: class for main window of app.

"""


import sys

from PyQt6 import uic
from PyQt6.QtCore import QPoint, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
    QTreeWidgetItem,
)


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

        self.addPointButton.clicked.connect(self.addPoint)
        self.addCircleButton.clicked.connect(self.addCircle)
        self.addLineButton.clicked.connect(self.addLine)
        self.addPointPolygonButton.clicked.connect(self.addPolygonPoint)
        self.addPolygonButton.clicked.connect(self.addPolygon)

        self.addCurrentObjectsContexMenu()

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

    def addCurrentObjectsContexMenu(self) -> None:
        """
        Add contex menu to delete geo Objects.
        """
        self.currentObjects.customContextMenuRequested.connect(
            self.showContextMenu
        )
        self.actionDeleteObj.triggered.connect(self.deleteObject)

    def showContextMenu(self, position: QPoint) -> None:
        """
        Show context menu for currentObjects.

        Args:
            position: position of cursor at the click moment.

        """
        context_menu = QMenu(self.currentObjects)
        context_menu.addAction(self.actionDeleteObj)

        context_menu.exec(self.currentObjects.viewport().mapToGlobal(position))

    def deleteObject(self) -> None:
        """
        Delete selected geo object.
        """
        selected_objects = self.currentObjects.selectedItems()
        if not selected_objects:
            QMessageBox.information(self, "Траектория БПЛА",
                "He выбран объект для удаления")
            return

        object_param = [obj for obj in selected_objects if obj.parent() is None]
        if not object_param:
            return

        root = self.currentObjects.invisibleRootItem()
        for obj in selected_objects:
            root.removeChild(obj)

    def validateParamets(self, params: list[str]) -> bool:
        """
        Validate given paramets of object.

        Args:
            params: list of object paramets in string representation

        """
        for param in params:
            if not param:
                QMessageBox.information(self, "Траектория БПЛА",
                    "Заполните все поля")
                return False
            try:
                float(param)
            except ValueError:
                QMessageBox.information(self, "Траектория БПЛА",
                    "Введите корректные данные")
                return False

        return True


    def addPoint(self) -> None:
        """
        Add point to the list of current objects.
        """
        name = self.pointNameLineEdit.text()
        x_coord = self.XCoordLineEditPoint.text()
        y_coord = self.YCoordLineEditPoint.text()

        params = [x_coord, y_coord]
        if not self.validateParamets(params):
            return

        if not name:
            name = "Точка"

        point = QTreeWidgetItem([name])
        QTreeWidgetItem(point, ["X:", x_coord])
        QTreeWidgetItem(point, ["Y:", y_coord])
        self.currentObjects.addTopLevelItem(point)
        QMessageBox.information(self, "Траектория БПЛА",
                "Точка добавлена")

    def addCircle(self) -> None:
        """
        Add circle to the list of current objects.
        """
        name = self.circleNameLineEdit.text()
        x_coord = self.XCoordLineEditCircle.text()
        y_coord = self.YCoordLineEditCircle.text()
        radius = self.radiusLineEditCircle.text()

        params = [x_coord, y_coord, radius]
        if not self.validateParamets(params):
            return

        if not name:
            name = "Окружность"

        circle = QTreeWidgetItem([name])
        QTreeWidgetItem(circle, ["X:", x_coord])
        QTreeWidgetItem(circle, ["Y:", y_coord])
        QTreeWidgetItem(circle, ["R:", radius])
        self.currentObjects.addTopLevelItem(circle)
        QMessageBox.information(self, "Траектория БПЛА",
                "Окружность добавлена")

    def addLine(self) -> None:
        """
        Add line to the list of current objects.
        """
        name = self.lineNameLineEdit.text()
        x_coord_beg = self.XCoordLineEditBegin.text()
        y_coord_beg = self.YCoordLineEditBegin.text()
        x_coord_end = self.XCoordLineEditEnd.text()
        y_coord_end = self.YCoordLineEditEnd.text()

        params = [x_coord_beg, y_coord_beg, x_coord_end, y_coord_end]
        if not self.validateParamets(params):
            return

        if not name:
            name = "Отрезок"

        line = QTreeWidgetItem([name])
        QTreeWidgetItem(line, ["X1:", x_coord_beg])
        QTreeWidgetItem(line, ["Y1:", y_coord_beg])
        QTreeWidgetItem(line, ["X2:", x_coord_end])
        QTreeWidgetItem(line, ["Y2:", y_coord_end])
        self.currentObjects.addTopLevelItem(line)
        QMessageBox.information(self, "Траектория БПЛА",
                "Отрезок добавлен")

    def addPolygonPoint(self) -> None:
        """
        Add point to the current polygon.
        """
        x_coord = self.XCoordLineEditPolygon.text()
        y_coord = self.YCoordLineEditPolygon.text()

        params = [x_coord, y_coord]
        if not self.validateParamets(params):
            return

        point_num = self.pointsPolygon.topLevelItemCount()
        point = QTreeWidgetItem(["Точка " + str(point_num)])
        QTreeWidgetItem(point, ["X:", x_coord])
        QTreeWidgetItem(point, ["Y:", y_coord])
        self.pointsPolygon.addTopLevelItem(point)
        QMessageBox.information(self, "Траектория БПЛА",
                "Точка многоугольника добавлена")

    def addPolygon(self) -> None:
        """
        Add polygon to the list of current objects.
        """
        min_points = 2
        points_count = self.pointsPolygon.topLevelItemCount()
        if points_count <= min_points:
            QMessageBox.information(self, "Траектория БПЛА",
                "Недостаточно точек для добавления многоугольника")
            return

        name = self.polygonNameLineEdit.text()
        if not name:
            name = "Многоугольник"

        polygon = QTreeWidgetItem([name])
        for i in range(points_count):
            point = self.pointsPolygon.topLevelItem(i)
            new_point = QTreeWidgetItem(polygon)
            for j in range(point.columnCount()):
                new_point.setText(j, point.text(j))
            for k in range(point.childCount()):
                coord = point.child(k)
                new_coord = QTreeWidgetItem(new_point)
                for j in range(coord.columnCount()):
                    new_coord.setText(j, coord.text(j))
                new_point.addChild(new_coord)


        self.currentObjects.addTopLevelItem(polygon)
        QMessageBox.information(self, "Траектория БПЛА",
                "Многоугольник добавлен")
        self.pointsPolygon.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
