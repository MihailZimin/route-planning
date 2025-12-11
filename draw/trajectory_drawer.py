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
from draw.drone_drawer import DroneDrawer
from pathfinding.pathfinding import Route

import math

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
        self.trajectory_length = 0
        for curve in path.route:
            if isinstance(curve, Line):
                line = LineDrawer(curve.start, curve.end)
                self.trajectory_length += line.length()
                self.route_drawer.append(line)
            else:
                arc = ArcDrawer(curve.center, curve.p_start, curve.p_end)
                self.trajectory_length += arc.length()
                self.route_drawer.append(arc)

        self.progress = 0.0
        self.is_animating = False
        self.map_view = map_view
        self.current_length = 0.0
        self.trajectory = qcp.QCPCurve(self.map_view.xAxis, self.map_view.yAxis)
        pen = QPen(Qt.GlobalColor.blue)
        pen.setWidth(3)
        self.trajectory.setPen(pen)

        self.drone_marker = DroneDrawer(map_view, size=20.0)

        self.timer = QTimer()
        self.timer.timeout.connect(self._animation_step)
        self.duration = 5000

        self.prev_point = None
        self.current_angle = 0.0

        self._calculate_initial_angle()

    def _calculate_initial_angle(self) -> None:
        """
        Set a start angle of trajectory.
        """
        if len(self.route_drawer) > 0:
            initial_points = self._get_points_at_progress(0.001)
            if len(initial_points) >= 2:
                p1 = initial_points[0]
                p2 = initial_points[1]
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                
                if abs(dx) > 0.001 or abs(dy) > 0.001:
                    self.current_angle = math.atan2(dy, dx)
                    self.drone_marker.set_angle_rad(self.current_angle)
                else:
                    initial_points = self._get_points_at_progress(0.01)
                    if len(initial_points) >= 2:
                        p1 = initial_points[0]
                        p2 = initial_points[-1]
                        dx = p2.x - p1.x
                        dy = p2.y - p1.y
                        if abs(dx) > 0.001 or abs(dy) > 0.001:
                            self.current_angle = math.atan2(dy, dx)
                            self.drone_marker.set_angle_rad(self.current_angle)

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
        self.current_length = 0.0
        self.trajectory.data().clear()
        self.drone_marker.set_visible(False)

        initial_points = self._get_points_at_progress(0.0)
        if initial_points:
            start_point = initial_points[0]
            self.drone_marker.set_position(start_point.x, start_point.y)
            self.drone_marker.set_angle_rad(self.current_angle)

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
        self.current_length = 0
        self.drone_marker.set_visible(False)
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

    def finish_animation(self) -> None:
        """
        Finish animation of trajectory.
        """
        self.set_progress(1.0)

    def set_duration(self, duration_ms: int) -> None:
        """
        Set duration of animation.
        """
        self.duration = max(100, duration_ms)
        if self.is_animating:
            current_progress = self.progress
            self.reset_animation()
            self.progress = current_progress
            self.start_animation()

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

        if points:
            for point in points:
                self.trajectory.addData(point.x, point.y)

            current_point = points[-1]

            self.drone_marker.set_position(current_point.x, current_point.y)

            if len(points) >= 2:
                prev_point = points[-2]
                dx = current_point.x - prev_point.x
                dy = current_point.y - prev_point.y
                
                angle_rad = math.atan2(dy, dx)
                
                self.current_angle = angle_rad
                self.drone_marker.set_angle_rad(angle_rad)
            else:
                self.drone_marker.set_angle_rad(self.current_angle)

            if not self.drone_marker.is_visible():
                self.drone_marker.set_visible(True)
            
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

        if current_progress <= 0.0:
            if self.route_drawer:
                first_points = self.route_drawer[0].get_progress_points(0.0)
                if first_points:
                    return [first_points[0]]
            return []

        traveled_dist = current_progress * self.trajectory_length
        points = []
        counted_dist = 0
        self.current_length = 0

        for segment in self.route_drawer:
            segment_length = segment.length()

            if counted_dist + segment_length <= traveled_dist:
                segment_points = segment.get_progress_points(1.0)
                if segment_points:
                    points.extend(segment_points)
                counted_dist += segment_length
                self.current_length += segment_length
            else:
                remainder = traveled_dist - counted_dist
                segment_progress = remainder / segment_length

                if segment_progress > 0:
                    segment_points = segment.get_progress_points(segment_progress)
                    if segment_points:
                        points.extend(segment_points)

                    self.current_length += remainder
                break
        return points

    def get_current_progress(self) -> float:
        """
        Get current progress of animation.

        Returns:
            current progress of animation.

        """
        return self.progress

    def get_current_length(self) -> float:
        """
        Get current length of trajectory for statistic.

        Returns:
            Current length of trajectory.

        """
        return round(self.current_length)

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
