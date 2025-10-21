"""
Class for GUI.

This module provides:
- MainWindow: class for main window of app.

"""


import json
import sys
from typing import TYPE_CHECKING

from PyQt6 import uic
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsScene,
    QMainWindow,
    QMessageBox,
    QTreeWidgetItem,
)

from core.point import Point
from draw.circle_drawer import CircleDrawer
from draw.line_drawer import LineDrawer
from draw.point_drawer import PointDrawer
from draw.polygon_drawer import PolygonDrawer

if TYPE_CHECKING:
    from draw.abstract_drawer import ABCDrawer


class MainWindow(QMainWindow):
    """
    Main window class.
    """

    def __init__(self) -> None:
        """
        Initialize MainWindow object.
        """
        super().__init__()
        self.geo_objects: list[ABCDrawer] = []
        self.initializeUI()

    def initializeUI(self) -> None:
        """
        Initionalization of MainWindow.
        """
        uic.loadUi("main_window/trajectory.ui", self)
        self.setGeometry(300, 100, 900, 550)
        self.setMaximumSize(QSize(1000, 1000))
        self.setMinimumSize(QSize(400, 300))

        self.showStatAction.triggered.connect(self.showStatistic)
        self.showParamsAction.triggered.connect(self.showParams)
        self.chooseMapAction.triggered.connect(self.chooseMap)
        self.changeMapAction.triggered.connect(self.changeMap)
        self.startAction.triggered.connect(self.startTrajectory)
        self.saveMapAction.triggered.connect(self.SaveMap)

        self.addPointButton.clicked.connect(self.addPoint)
        self.addCircleButton.clicked.connect(self.addCircle)
        self.addLineButton.clicked.connect(self.addLine)
        self.addPointPolygonButton.clicked.connect(self.addPolygonPoint)
        self.addPolygonButton.clicked.connect(self.addPolygon)

        self.deleteButton.clicked.connect(self.deleteObject)
        self.objectList.itemSelectionChanged.connect(self.showObjectsParams)

        self.scene = QGraphicsScene()
        self.mapView.setScene(self.scene)
        self.scene.setSceneRect(1, 1, 600, 450)

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
        Slot for showing parameters of flight.
        """
        self.stackedWidget.setCurrentIndex(1)

    def changeMap(self) -> None:
        """
        Slot for changing map.
        """
        self.stackedWidget.setCurrentIndex(2)

    def chooseMap(self) -> None:
        """
        Slot for chosing map.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "")
        if file_path:
            self.statusBar.showMessage(f"Выбран файл: {file_path}")

    def SaveMap(self) -> None:
        """
        Slot for saving map
        """
        if self.geo_objects:
            file_name, _ = QFileDialog.getSaveFileName(
                self, 
                "Сохранить карту", 
                "", 
                "JSON Files (*.json);;All Files (*)"
            )
            if file_name:
                with open(file_name, "w", encoding='utf-8') as file:
                    map_data = [obj.save() for obj in self.geo_objects]
                    json.dump(map_data, file, indent=4)
        else:
            QMessageBox.information(self, "Траектория БПЛА",
                "Ha карте нет объектов для сохранения")

    def startTrajectory(self) -> None:
        """
        Slot for starting animation of flight.
        """
        self.statusBar.showMessage("Процесс построения траектории запущен")

    def updateObjectList(self) -> None:
        """
        Update list of geometry objects.
        """
        self.objectList.clear()
        for obj in self.geo_objects:
            self.objectList.addItem(obj.name)

    def deleteObject(self) -> None:
        """
        Delete selected geo object.
        """
        selected_objects = self.objectList.selectedItems()

        if not selected_objects:
            QMessageBox.information(self, "Траектория БПЛА",
                "Выберите элемент")
            return

        items_index = []

        for item in selected_objects:
            index = self.objectList.row(item)
            items_index.append(index)

        items_index.sort(reverse=True)
        for i in items_index:
            self.geo_objects.pop(i)

        self.updateObjectList()
        self.redraw()

    def showObjectsParams(self) -> None:
        """
        Show parameters of selected objects.
        """
        selected_objects = self.objectList.selectedItems()

        if not selected_objects:
            self.infoLabel.setText("Характеристики объекта")
            return

        info = ""

        for item in selected_objects:
            index = self.objectList.row(item)
            for param, value in self.geo_objects[index].parameters.items():
                info += param + f"  {value}<br>"

        self.infoLabel.setText(info)

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

        point = PointDrawer(float(x_coord), float(y_coord), name)
        self.geo_objects.append(point)
        point.draw(self.mapView)
        self.updateObjectList()

        self.objectList.setCurrentRow(len(self.geo_objects) - 1)

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

        center = Point(float(x_coord), float(y_coord))

        circle = CircleDrawer(center, float(radius), name)
        self.geo_objects.append(circle)
        circle.draw(self.mapView)
        self.updateObjectList()

        self.objectList.setCurrentRow(len(self.geo_objects) - 1)

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

        point_begin = Point(float(x_coord_beg), float(y_coord_beg))
        point_end = Point(float(x_coord_end), float(y_coord_end))

        line = LineDrawer(point_begin, point_end, name)
        self.geo_objects.append(line)
        line.draw(self.mapView)
        self.updateObjectList()

        self.objectList.setCurrentRow(len(self.geo_objects) - 1)

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
        point = QTreeWidgetItem(["Точка " + str(point_num + 1)])
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

        polygon_points = []

        for i in range(points_count):
            coords = []
            point = self.pointsPolygon.topLevelItem(i)
            for k in range(point.childCount()):
                coord = point.child(k)
                coords.append(float(coord.text(1)))
            p = Point(coords[0], coords[1])
            polygon_points.append(p)

        polygon = PolygonDrawer(polygon_points, name)
        self.geo_objects.append(polygon)
        polygon.draw(self.mapView)
        self.updateObjectList()

        self.objectList.setCurrentRow(len(self.geo_objects) - 1)

        QMessageBox.information(self, "Траектория БПЛА",
                "Многоугольник добавлен")
        self.pointsPolygon.clear()

    def redraw(self) -> None:
        """
        Redraw current map.
        """
        self.scene.clear()
        for obj in self.geo_objects:
            obj.draw(self.mapView)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
