"""
Class TrajectoryDrawer.

This module provides:
    TrajectoryDrawer class for drawing calculated trajectory.
"""

import QCustomPlot_PyQt6 as qcp
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPen

from core.line import Line
from core.point import Point
from draw.arc_drawer import ArcDrawer
from draw.line_drawer import LineDrawer
from pathfinding.pathfinding import Route


class TrajectoryDrawer:
    """
    Class for drawing trajectory with animation.
    """

    def __init__(self, path: Route, map_view: qcp.QCustomPlot) -> None:
        """
        Initialize trajectory drawer.

        Args:
            path: list of lines and arches which form a trajectory.
            map_view: widget where trajectory will be drawn.

        """
        self.route_drawer = []
        for curve in path.route:
            if isinstance(curve, Line):
                line = LineDrawer(curve.start, curve.end)
                self.route_drawer.append(line)
            else:
                arc = ArcDrawer(curve.center, curve.p_start, curve.p_end)
                self.route_drawer.append(arc)

        self.progress = 0.0
        self.is_animating = False
        self.map_view = map_view
        self.trajectory = qcp.QCPCurve(self.map_view.xAxis, self.map_view.yAxis)
        pen = QPen(Qt.GlobalColor.blue)
        pen.setWidth(3)
        self.trajectory.setPen(pen)

        self.timer = QTimer()
        self.timer.timeout.connect(self._animation_step)
        self.duration = 5000

    def start_animation(self) -> bool:
        """
        Start animation.

        Returns:
            True if it possible to start animation. Else returns False.

        """
        if self.is_animating:
            return False

        self.is_animating = True
        self.progress = 0.0
        self.trajectory.data().clear()
        self.timer.start(16)

        return True

    def pause_animation(self) -> None:
        """
        Pause animation.
        """
        self.is_animating = False
        self.timer.stop()

    def resume_animation(self) -> None:
        """
        Resume animation from current place.
        """
        if not self.is_animating:
            self.is_animating = True
            self.timer.start(16)

    def reset_animation(self) -> None:
        """
        Reset animation.
        """
        self.pause_animation()
        self.progress = 0.0
        self.trajectory.data().clear()
        self.map_view.replot()

    def set_progress(self, new_progress: float) -> None:
        """
        Set animation progress.

        Args:
            new_progress: animation progress which will be set

        """
        self.progress = new_progress
        self._update_trajectory()

    def _animation_step(self) -> None:
        """
        Increase animation progress.
        """
        if not self.is_animating:
            return

        time_step = 16
        progress_step = time_step / self.duration
        self.progress = self.progress + progress_step

        self._update_trajectory()

        if self.progress >= 1:
            self.pause_animation()

    def _update_trajectory(self) -> None:
        """
        Update trajectory at current progress.
        """
        self.trajectory.data().clear()

        points = self._get_points_at_progress(self.progress)
        for point in points:
            self.trajectory.addData(point.x, point.y)

        self.map_view.replot()

    def _get_points_at_progress(self, current_progress: float) -> list[Point]:
        """
        Get points of trajectory for current progress.

        Args:
            current_progress: current progress of animation.

        """
        lines_num = len(self.route_drawer)
        if lines_num == 0:
            return []

        progress_per_line = 1.0 / lines_num
        points = []
        animated_lines = int(current_progress / progress_per_line)
        for i in range(animated_lines):
            line_points = self.route_drawer[i].get_progress_points(1.0)
            points.extend(line_points)

        if animated_lines < lines_num:
            line_progress = (current_progress % progress_per_line) / progress_per_line
            line_points = self.route_drawer[animated_lines].get_progress_points(line_progress)
            points.extend(line_points)

        return points

    def get_current_progress(self) -> float:
        """
        Get current progress of animation.

        Returns:
            current progress of animation.

        """
        return self.progress

    def draw(self, map_view: qcp.QCustomPlot, color:Qt.GlobalColor=Qt.GlobalColor.red) -> None:
        """
        Draw full trajectory without animation.

        Args:
            map_view: widget where trajectory will be drawn.
            color: color of trajectory.

        Default color: red.

        """
        for curve in self.route_drawer:
            curve.draw(map_view, color)
