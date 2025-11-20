"""
Class TrajectoryDrawer.

This module provides:
    TrajectoryDrawer class for drawing calculated trajectory.
"""

import QCustomPlot_PyQt6 as qcp

from core.line import Line
from draw.arc_drawer import ArcDrawer
from draw.line_drawer import LineDrawer
from pathfinding.pathfinding import Route


class TrajectoryDrawer:
    """
    Class for drawing trajectory.
    """

    def __init__(self, path: Route) -> None:
        """
        Initialize trajectory drawer.

        Args:
            path: list of lines and arches which form a trajectory.

        """
        self.route_drawer = []
        for curve in path.route:
            if isinstance(curve, Line):
                line = LineDrawer(curve.start, curve.end)
                self.route_drawer.append(line)
            else:
                arc = ArcDrawer(curve.center, curve.p_start, curve.p_end)
                self.route_drawer.append(arc)

    def draw(self, map_view: qcp.QCustomPlot) -> None:
        """
        Draw trajectory.

        Args:
            map_view: widget where trajectory will be drawn.

        """
        for curve in self.route_drawer:
            curve.draw(map_view) 
