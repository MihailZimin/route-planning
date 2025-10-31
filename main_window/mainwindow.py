"""
Class for GUI.

This module provides:
- MainWindow: class for main window of app.

"""


import sys
from pathlib import Path
from typing import TYPE_CHECKING

import QCustomPlot_PyQt6 as qcp
from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QTreeWidgetItem,
    QVBoxLayout,
)

from core.circle import Circle
from core.line import Line
from core.point import Point
from core.polygon import Polygon
from draw.circle_drawer import CircleDrawer
from draw.line_drawer import LineDrawer
from draw.point_drawer import PointDrawer
from draw.polygon_drawer import PolygonDrawer
from main_window.dialogwindow import EditDialogWindow

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
        self.setGeometry(300, 100, 900, 650)
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
        self.objectList.itemDoubleClicked.connect(self.editObject)

        self.initializeCustomPlot()

    def initializeCustomPlot(self) -> None:
        """
        Initionalization of QCustomPlot for map drawing.
        """
        self.custom_plot = qcp.QCustomPlot()
        layout = QVBoxLayout(self.mapView)
        layout.addWidget(self.custom_plot)

        self.custom_plot.setBackground(QColor(173, 255, 138))

        grid_pen = QPen(QColor(0, 0, 0), 0.25, Qt.PenStyle.SolidLine)
        self.custom_plot.xAxis.grid().setPen(grid_pen)
        self.custom_plot.yAxis.grid().setPen(grid_pen)

        self.custom_plot.xAxis.setRange(0, 1000)
        self.custom_plot.yAxis.setRange(0, 1000)

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
            self.geo_objects = []
            with Path(file_path).open("r", encoding="utf-8") as file:
                obj_list = file.readlines()
                for obj in obj_list:
                    params = obj.split("|")
                    obj_type = params[0]
                    obj_params = params[1]
                    obj_name = params[2].replace("\n", "")

                    if obj_type == "Point":
                        point = Point.load(obj_params)
                        point_draw = PointDrawer(point.x, point.y, obj_name)
                        self.geo_objects.append(point_draw)
                    elif obj_type == "Line":
                        line = Line.load(obj_params)
                        line_draw = LineDrawer(line.start, line.end, obj_name)
                        self.geo_objects.append(line_draw)
                    elif obj_type == "Circle":
                        circle = Circle.load(obj_params)
                        circle_draw = CircleDrawer(circle.center, circle.radius, obj_name)
                        self.geo_objects.append(circle_draw)
                    elif obj_type == "Polygon":
                        polygon = Polygon.load(obj_params)
                        polygon_draw = PolygonDrawer(polygon.points, obj_name)
                        self.geo_objects.append(polygon_draw)

            self.updateObjectList()
            self.redraw()
            self.statusBar.showMessage(f"Выбран файл: {file_path}")

    def SaveMap(self) -> None:
        """
        Slot for saving map.
        """
        if self.geo_objects:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить карту",
                "",
                "Text files (*.txt);;All Files (*)"
            )
            if file_name:
                with Path(file_name).open("w", encoding="utf-8") as file:
                    for obj in self.geo_objects:
                        obj_params = obj.save()
                        obj_type = ""
                        if isinstance(obj, PointDrawer):
                            obj_type = "Point"
                        elif isinstance(obj, CircleDrawer):
                            obj_type = "Circle"
                        elif isinstance(obj, LineDrawer):
                            obj_type = "Line"
                        elif isinstance(obj, PolygonDrawer):
                            obj_type = "Polygon"
                        obj_string = obj_type + "|" + obj_params + "|" + obj.name
                        file.write(obj_string + "\n")
                self.statusBar.showMessage("Карта сохранена")
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
            self.infoLabel.setText("")
            return

        info = ""

        for item in selected_objects:
            index = self.objectList.row(item)
            for param, value in self.geo_objects[index].parameters.items():
                info += param + f"  {value}" + "\n"

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
        point.draw(self.custom_plot)
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
        circle.draw(self.custom_plot)
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

        point_begin = PointDrawer(float(x_coord_beg), float(y_coord_beg))
        point_end = PointDrawer(float(x_coord_end), float(y_coord_end))

        line = LineDrawer(point_begin, point_end, name)
        self.geo_objects.append(line)
        line.draw(self.custom_plot)
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
        polygon.draw(self.custom_plot)
        self.updateObjectList()

        self.objectList.setCurrentRow(len(self.geo_objects) - 1)

        QMessageBox.information(self, "Траектория БПЛА",
                "Многоугольник добавлен")
        self.pointsPolygon.clear()

    def redraw(self) -> None:
        """
        Redraw current map.
        """
        self.custom_plot.clearItems()
        self.custom_plot.clearGraphs()
        self.custom_plot.clearPlottables()
        for obj in self.geo_objects:
            obj.draw(self.custom_plot)
        self.custom_plot.replot()

    def editObject(self) -> None:
        """
        Edit selected object.
        """
        selected_objects = self.objectList.selectedItems()
        index = self.objectList.row(selected_objects[0])
        geo_object = self.geo_objects[index]
        edit_win = EditDialogWindow(geo_object, self)
        new_params = edit_win.getChanges()
        if edit_win.exec() == QDialog.DialogCode.Accepted:
            if geo_object.type == "Point":
                geo_object.name = new_params["name"].text()
                geo_object.x = float(new_params["x"].text())
                geo_object.y = float(new_params["y"].text())
            if geo_object.type == "Circle":
                geo_object.name = new_params["name"].text()
                geo_object.center.x = float(new_params["x"].text())
                geo_object.center.y = float(new_params["y"].text())
                geo_object.radius = float(new_params["R"].text())
            if geo_object.type == "Line":
                geo_object.name = new_params["name"].text()
                geo_object.start.x = float(new_params["x1"].text())
                geo_object.start.y = float(new_params["y1"].text())
                geo_object.end.x = float(new_params["x2"].text())
                geo_object.end.y = float(new_params["y2"].text())

            self.redraw()
            QMessageBox.information(self, "Траектория БПЛА",
                    "Объект обновлён")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
