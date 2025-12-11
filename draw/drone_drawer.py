"""Module for drawing drone"""

from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt
import QCustomPlot_PyQt6 as qcp
import math

class DroneDrawer:
    """
    Class for drawing drone.
    """

    def __init__(self, plot: qcp.QCustomPlot, size: float = 10.0) -> None:
        """
        Initialize drone drawer.
        """
        self.plot = plot
        self.size = size

        self.triangle_curve = qcp.QCPCurve(plot.xAxis, plot.yAxis)

        pen = QPen(QColor(0, 0, 255))
        pen.setWidth(2)
        self.triangle_curve.setPen(pen)
        
        brush = QBrush(Qt.GlobalColor.white)
        self.triangle_curve.setBrush(brush)
        self.triangle_curve.setVisible(False)

        self.x = 0
        self.y = 0
        self.angle = 0
        
    def set_position(self, x: float, y: float) -> None:
        """
        Set position of drone.
        """
        self.x = x
        self.y = y
        self._update_triangle()
        
    def set_angle_deg(self, angle_degrees: float) -> None:
        """
        Set angle in degrees.
        """
        self.angle = math.radians(angle_degrees)
        self._update_triangle()
        
    def set_angle_rad(self, angle_radians: float) -> None:
        """
        Set angle in rad
        """
        self.angle = angle_radians
        self._update_triangle()
        
    def _update_triangle(self) -> None:
        """
        Update vertices of the triangle.
        """
        if not self.triangle_curve.visible():
            self.triangle_curve.setVisible(True)
            
        base_vertices = [
            (self.size, 0),
            (-self.size/2, self.size/3),
            (-self.size/2, -self.size/3),
            (self.size, 0)
        ]

        self.triangle_curve.data().clear()

        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        
        for vx, vy in base_vertices:
            rx = vx * cos_a - vy * sin_a
            ry = vx * sin_a + vy * cos_a

            final_x = self.x + rx
            final_y = self.y + ry

            self.triangle_curve.addData(final_x, final_y)
            
    def set_visible(self, visible: bool) -> None:
        """
        Set drone visible.
        """
        self.triangle_curve.setVisible(visible)

    def is_visible(self) -> bool:
        """
        Check if drone is visible or not.
        """
        return self.triangle_curve.visible()
