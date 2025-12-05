"""
Class for GUI.

This module provides:
- MainWindow: class for main window of app.

"""


import sys
from enum import Enum
from pathlib import Path
from typing import ClassVar

import QCustomPlot_PyQt6 as qcp
from PyQt6 import uic
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QAction, QActionGroup, QColor, QIcon, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
)

from core.circle import Circle
from core.line import Line
from core.point import Point
from core.polygon import Polygon
from dialog_window.circle_edit_dialog import CircleEditDialogWindow
from dialog_window.line_edit_dialog import LineEditDialogWindow
from dialog_window.point_edit_dialog import PointEditDialogWindow
from dialog_window.polygon_edit_dialog import PolygonEditDialogWindow
from dialog_window.polygon_point_edit_dialog import PolygonPointEditDialogWindow
from draw.abstract_drawer import ABCDrawer
from draw.circle_drawer import CircleDrawer
from draw.line_drawer import LineDrawer
from draw.point_drawer import PointDrawer
from draw.polygon_drawer import PolygonDrawer
from draw.trajectory_drawer import TrajectoryDrawer
from pathfinding.pathfinding import Route, matrix_calculation, route_calculation
from tsp_algorithms.brute_force import BruteForceSolver
from tsp_algorithms.little_algorithm import LittleAlgorithm


class Algorithm(Enum):
    """
    Enum for algorithm choice.
    """

    LITTLE = 0
    BRUTE_FORCE = 1


class MainWindow(QMainWindow):
    """
    Main window class.
    """

    dialogs: ClassVar[dict[str, ABCDrawer]] = {
        "Point": PointEditDialogWindow,
        "Circle": CircleEditDialogWindow,
        "Line": LineEditDialogWindow,
        "Polygon": PolygonEditDialogWindow
    }

    def __init__(self) -> None:
        """
        Initialize MainWindow object.
        """
        super().__init__()
        self.geo_objects: list[ABCDrawer] = []
        self.points_polygon: list[Point] = []
        self.algorithm: Algorithm = Algorithm.LITTLE
        self.trajectory_drawer: TrajectoryDrawer = None
        self.ui_timer: QTimer = None
        self.start_point: PointDrawer = None
        self.bpla_count = 1
        self.speed = 60
        self.initializeUI()

    def initializeUI(self) -> None:
        """
        Initionalization of MainWindow.
        """
        uic.loadUi("main_window/trajectory.ui", self)
        self.setGeometry(300, 100, 900, 650)
        self.setMinimumSize(QSize(400, 300))

        self.chooseMapAction.triggered.connect(self.chooseMap)
        self.changeMapAction.triggered.connect(self.changeMap)
        self.trajectoryAction.triggered.connect(self.controlTrajectory)
        self.saveMapAction.triggered.connect(self.saveMap)

        self.calculate.clicked.connect(self.calculateTrajectory)

        self.addPointButton.clicked.connect(self.addPoint)
        self.addCircleButton.clicked.connect(self.addCircle)
        self.addLineButton.clicked.connect(self.addLine)
        self.addPointPolygonButton.clicked.connect(self.addPolygonPoint)
        self.addPolygonButton.clicked.connect(self.addPolygon)

        self.deleteButton.clicked.connect(self.deleteObject)
        self.objectList.itemSelectionChanged.connect(self.showObjectsParams)
        self.objectList.itemDoubleClicked.connect(self.editObject)

        self.polygonPoints.itemDoubleClicked.connect(self.editPolygonPoint)
        self.deletePointButton.clicked.connect(self.deletePolygonPoint)

        self.algo_group = QActionGroup(self)
        self.algo_group.setExclusive(True)
        self.algo_group.addAction(self.algoLittle)
        self.algo_group.addAction(self.algoBruteForce)
        self.algo_group.triggered.connect(self.chooseAlgorithm)

        self.setupAnimation()
        self.initializeCustomPlot()

    def setupAnimation(self) -> None:
        """
        Initialize animation.
        """
        self.startButton.clicked.connect(self.start_animation)
        self.resetButton.clicked.connect(self.reset_animation)
        self.finishButton.clicked.connect(self.finish_animation)
        self.slider.valueChanged.connect(self.on_progress_slider_changed)

        self.ui_update_timer = QTimer()
        self.ui_update_timer.timeout.connect(self.update_animation_ui)
        self.ui_update_timer.start(50)

        self.set_animation_buttons_state(enabled=False)

    def set_animation_buttons_state(self, *, enabled: bool) -> None:
        """
        Set default animation buttons state.
        """
        self.startButton.setEnabled(enabled)
        self.resetButton.setEnabled(enabled)
        self.finishButton.setEnabled(enabled)
        self.slider.setEnabled(enabled)

    def get_trajectory_params(self) -> None:
        """
        Get parameters of trajectrory.
        """
        new_speed = self.speedLineEdit.text()
        new_bpla_count = self.droneAmountLineEdit.text()
        try:
            new_speed = float(new_speed)
            new_bpla_count = int(new_bpla_count)
        except TypeError:
            QMessageBox.information(self, "Траектория БПЛА",
                "He валидные параметры")
            self.speedLineEdit.setText("60")
            self.droneAmountLineEdit.text("1")
            return
        
        self.speed = new_speed
        self.bpla_count = new_bpla_count

        self.speedLineEdit.setText(str(self.speed))
        self.droneAmountLineEdit.text(str(self.bpla_count))

    def start_animation(self) -> None:
        """
        Start or continue animation.
        """
        if self.trajectory_drawer:
            if self.trajectory_drawer.is_animating:
                self.startButton.setIcon(QIcon("pict_trajectory/play.png"))
                self.startButton.setIconSize(QSize(35, 35))
                self.trajectory_drawer.pause_animation()
            else:
                self.startButton.setIcon(QIcon("pict_trajectory/pause.png"))
                self.startButton.setIconSize(QSize(35, 35))
                self.trajectory_drawer.resume_animation()

    def reset_animation(self) -> None:
        """
        Reset animation.
        """
        if self.trajectory_drawer:
            self.trajectory_drawer.reset_animation()

    def finish_animation(self) -> None:
        """
        Finish animation.
        """
        if self.trajectory_drawer:
            self.startButton.setIcon(QIcon("pict_trajectory/play.png"))
            self.startButton.setIconSize(QSize(35, 35))
            self.trajectory_drawer.finish_animation()

    def on_progress_slider_changed(self, value: int) -> None:
        """
        Change slider progress.
        """
        if self.trajectory_drawer:
            self.slider.blockSignals(True)
            progress = value / 100.0
            self.trajectory_drawer.set_progress(progress)
            self.slider.blockSignals(False)

    def update_animation_ui(self) -> None:
        """
        Update animation via mainwindow timer.
        """
        if self.trajectory_drawer:
            progress = self.trajectory_drawer.get_current_progress()
            cur_length = self.trajectory_drawer.get_current_length()

            self.slider.blockSignals(True)
            self.slider.setValue(int(progress * 100))
            self.slider.blockSignals(False)

            self.curDistanceLineEdit.setText(str(cur_length))

            if progress >= 1:
                self.startButton.setIcon(QIcon("pict_trajectory/play.png"))
                self.startButton.setIconSize(QSize(35, 35))

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

    def changeMap(self) -> None:
        """
        Slot for changing map.
        """
        if self.trajectory_drawer is not None and self.trajectory_drawer.is_animating:
            QMessageBox.information(self, "Траектория БПЛА",
                "Идет анимация траектории")
            return
        self.stackedWidget.setCurrentIndex(1)

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
                    len_of_start_point_line = 4
                    if len(params) == len_of_start_point_line:
                        start_point_params = params[1]
                        start_point_name = params[2]
                        start_point = Point.load(start_point_params)
                        self.start_point = PointDrawer(start_point.x, start_point.y, start_point_name)
                        self.start_point.is_start_point = True
                        self.geo_objects.append(self.start_point)
                        continue
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

    def saveMap(self) -> None:
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
                        obj_type = obj.type
                        obj_string = obj_type + "|" + obj_params + "|" + obj.name
                        file.write(obj_string + "\n")
                    if self.start_point is not None:
                        point_params = self.start_point.save()
                        point_name = self.start_point.name
                        obj_string = "Point|" + point_params + "|" + point_name + "|" + "Start"
                        file.write(obj_string + "\n")
                self.statusBar.showMessage("Карта сохранена")
        else:
            QMessageBox.information(self, "Траектория БПЛА",
                "Ha карте нет объектов для сохранения")

    def controlTrajectory(self) -> None:
        """
        Slot for showing trajectory control menu.
        """
        self.stackedWidget.setCurrentIndex(0)

    def calculateTrajectory(self) -> None:
        """
        Slot for calculation trajectory for animation.
        """
        control_points = []
        obstacles = []

        if self.start_point is None:
            QMessageBox.information(self, "Траектория БПЛА",
                "Ha карте нет стартовой точки")
            return

        control_points.append(self.start_point)

        for geo_object in self.geo_objects:
            if geo_object.type == "Point":
                control_points.append(geo_object)
            else:
                obstacles.append(geo_object)

        if not control_points:
            QMessageBox.information(self, "Траектория БПЛА",
                "Ha карте нет контрольных точек")
            return

        routes = route_calculation(control_points, obstacles)
        matrix = matrix_calculation(routes)

        if self.algorithm == Algorithm.LITTLE:
            solver = LittleAlgorithm()
            path, _ = solver.solve(matrix, 0)
        else:
            solver = BruteForceSolver()
            path, _ = solver.solve(matrix, 0)

        total_path_list = []
        for i in range(len(path) - 1):
            cur_path = routes[path[i]][path[i + 1]]
            total_path_list.extend(cur_path.route)

        total_path = Route(total_path_list)
        self.trajectory_drawer = TrajectoryDrawer(total_path, self.custom_plot)
        self.set_animation_buttons_state(enabled=True)
        QMessageBox.information(self, "Траектория БПЛА",
                "Оптимальный маршрут посчитан")

    def chooseAlgorithm(self, action: QAction) -> None:
        """
        Slot for choosing tsp algorithm.

        Args:
            action: selected algorithm menu button.

        """
        if action == self.algoLittle:
            self.algorithm = Algorithm.LITTLE
            self.statusBar.showMessage("Выбран алгоритм Литтла")
        else:
            self.algorithm = Algorithm.BRUTE_FORCE
            self.statusBar.showMessage("Выбран переборный алгоритм")

    def updateObjectList(self) -> None:
        """
        Update list of geometry objects.
        """
        self.objectList.clear()
        for obj in self.geo_objects:
            self.objectList.addItem(obj.name)

    def updatePointsPolygonList(self) -> None:
        """
        Update list of polygon points.
        """
        self.polygonPoints.clear()
        for i in range(len(self.points_polygon)):
            self.polygonPoints.addItem("Точка " + str(i + 1))

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
        self.set_animation_buttons_state(enabled=False)

    def deletePolygonPoint(self) -> None:
        """
        Delete selected geo object.
        """
        selected_objects = self.polygonPoints.selectedItems()

        if not selected_objects:
            QMessageBox.information(self, "Траектория БПЛА",
                "Выберите точку")
            return

        items_index = []

        for item in selected_objects:
            index = self.polygonPoints.row(item)
            items_index.append(index)

        items_index.sort(reverse=True)
        for i in items_index:
            self.points_polygon.pop(i)

        self.updatePointsPolygonList()

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
                info += param + ":" + f"  {value}" + "\n"

        self.infoLabel.setText(info)

    @staticmethod
    def clearLineEdit(line_edits: list[QLineEdit]) -> None:
        """
        Clear current lineEdits after adding geo object.

        Args:
            line_edits: lineEdits which will be cleared.

        """
        for line_edit in line_edits:
            line_edit.clear()

    def addPoint(self) -> None:
        """
        Add point to the list of current objects.
        """
        name = self.pointNameLineEdit.text()
        x_coord = self.XCoordLineEditPoint.text()
        y_coord = self.YCoordLineEditPoint.text()

        if not name:
            name = "Точка"

        try:
            point = PointDrawer(float(x_coord), float(y_coord), name)
        except ValueError as error:
            QMessageBox.information(self, "Траектория БПЛА", str(error))
            return

        if self.isStartRadioButton.isChecked():
            point.is_start_point = True
            if self.start_point is not None:
                for obj in self.geo_objects:
                    if obj.type == "Point" and obj.is_start_point:
                        obj.is_start_point = False
            self.start_point = point

        self.geo_objects.append(point)
        self.redraw()
        self.updateObjectList()

        MainWindow.clearLineEdit(
            [self.pointNameLineEdit, self.XCoordLineEditPoint, self.YCoordLineEditPoint]
        )

        self.objectList.setCurrentRow(len(self.geo_objects) - 1)

        QMessageBox.information(self, "Траектория БПЛА",
                "Точка добавлена")
        self.isStartRadioButton.setChecked(False)
        self.set_animation_buttons_state(enabled=False)

    def addCircle(self) -> None:
        """
        Add circle to the list of current objects.
        """
        name = self.circleNameLineEdit.text()
        x_coord = self.XCoordLineEditCircle.text()
        y_coord = self.YCoordLineEditCircle.text()
        radius = self.radiusLineEditCircle.text()

        if not name:
            name = "Окружность"

        try:
            center = Point(float(x_coord), float(y_coord))
            circle = CircleDrawer(center, float(radius), name)
        except ValueError as error:
            QMessageBox.information(self, "Траектория БПЛА", str(error))
            return

        self.geo_objects.append(circle)
        self.redraw()
        self.updateObjectList()

        MainWindow.clearLineEdit(
            [
                self.circleNameLineEdit,
                self.XCoordLineEditCircle,
                self.YCoordLineEditCircle,
                self.radiusLineEditCircle
            ]
        )

        self.objectList.setCurrentRow(len(self.geo_objects) - 1)

        QMessageBox.information(self, "Траектория БПЛА",
                "Окружность добавлена")
        self.set_animation_buttons_state(enabled=False)

    def addLine(self) -> None:
        """
        Add line to the list of current objects.
        """
        name = self.lineNameLineEdit.text()
        x_coord_beg = self.XCoordLineEditBegin.text()
        y_coord_beg = self.YCoordLineEditBegin.text()
        x_coord_end = self.XCoordLineEditEnd.text()
        y_coord_end = self.YCoordLineEditEnd.text()

        if not name:
            name = "Отрезок"

        try:
            point_begin = PointDrawer(float(x_coord_beg), float(y_coord_beg))
            point_end = PointDrawer(float(x_coord_end), float(y_coord_end))
        except ValueError as error:
            QMessageBox.information(self, "Траектория БПЛА", str(error))
            return

        line = LineDrawer(point_begin, point_end, name)
        self.geo_objects.append(line)
        self.redraw()
        self.updateObjectList()

        MainWindow.clearLineEdit(
            [
                self.lineNameLineEdit,
                self.XCoordLineEditBegin,
                self.YCoordLineEditBegin,
                self.XCoordLineEditEnd,
                self.YCoordLineEditEnd
            ]
        )

        self.objectList.setCurrentRow(len(self.geo_objects) - 1)

        QMessageBox.information(self, "Траектория БПЛА",
                "Отрезок добавлен")
        self.set_animation_buttons_state(enabled=False)

    def addPolygonPoint(self) -> None:
        """
        Add point to the current polygon.
        """
        x_coord = self.XCoordLineEditPolygon.text()
        y_coord = self.YCoordLineEditPolygon.text()

        try:
            polygon_point = Point(float(x_coord), float(y_coord))
        except ValueError as error:
            QMessageBox.information(self, "Траектория БПЛА", str(error))
            return

        self.points_polygon.append(polygon_point)
        self.updatePointsPolygonList()

        MainWindow.clearLineEdit(
            [
                self.XCoordLineEditPolygon,
                self.YCoordLineEditPolygon
            ]
        )

        QMessageBox.information(self, "Траектория БПЛА",
                "Точка многоугольника добавлена")

    def addPolygon(self) -> None:
        """
        Add polygon to the list of current objects.
        """
        min_points = 2
        points_count = len(self.points_polygon)
        if points_count <= min_points:
            QMessageBox.information(self, "Траектория БПЛА",
                "Недостаточно точек для добавления многоугольника")
            return

        name = self.polygonNameLineEdit.text()
        if not name:
            name = "Многоугольник"

        try:
            polygon = PolygonDrawer(self.points_polygon, name)
        except ValueError as error:
            QMessageBox.information(self, "Траектория БПЛА", str(error))
            return

        self.geo_objects.append(polygon)
        self.redraw()
        self.updateObjectList()

        self.objectList.setCurrentRow(len(self.geo_objects) - 1)

        self.points_polygon = []
        self.updatePointsPolygonList()
        MainWindow.clearLineEdit([self.polygonNameLineEdit])
        QMessageBox.information(self, "Траектория БПЛА",
                "Многоугольник добавлен")
        self.set_animation_buttons_state(enabled=False)

    def redraw(self) -> None:
        """
        Redraw current map.
        """
        self.custom_plot.clearItems()
        self.custom_plot.clearGraphs()
        self.custom_plot.clearPlottables()
        for obj in self.geo_objects:
            if obj.type == "Point" and obj.is_start_point:
                obj.draw(self.custom_plot, Qt.GlobalColor.yellow)
                continue
            obj.draw(self.custom_plot)
        self.custom_plot.replot()

    def get_start_point_index(self) -> int:
        """
        Get index of start point.

        Retruns:
            Index of start point.
            -1 if no start point.
        """
        for i in range(len(self.geo_objects)):
            if self.geo_objects[i].type == "Point" and self.geo_objects[i].is_start_point:
                return i
        return -1

    def editObject(self) -> None:
        """
        Edit selected object.
        """
        selected_objects = self.objectList.selectedItems()
        index = self.objectList.row(selected_objects[0])
        geo_object = self.geo_objects[index]
        edit_win = MainWindow.dialogs[geo_object.type](geo_object, self)
        start_point_index = self.get_start_point_index()

        if edit_win.exec() == QDialog.DialogCode.Accepted:
            if geo_object.type == "Point" and geo_object.is_start_point:
                if index != start_point_index:
                    self.geo_objects[start_point_index].is_start_point = False
                self.start_point = geo_object
            self.showObjectsParams()
            self.updateObjectList()
            self.redraw()
            QMessageBox.information(self, "Траектория БПЛА",
                    "Объект обновлён")
            self.set_animation_buttons_state(enabled=False)

    def editPolygonPoint(self) -> None:
        """
        Edit selected polygon point.
        """
        selected_objects = self.polygonPoints.selectedItems()
        index = self.polygonPoints.row(selected_objects[0])
        point = self.points_polygon[index]
        edit_point_win = PolygonPointEditDialogWindow(point, "Точка " + str(index + 1), self)

        if edit_point_win.exec() == QDialog.DialogCode.Accepted:
            edit_point_win.setChanges()
            QMessageBox.information(self, "Траектория БПЛА",
                    "Точка обновлена")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
