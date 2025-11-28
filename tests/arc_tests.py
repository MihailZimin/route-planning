"""Tests for core class Arc."""
import math

import pytest

from core.arc import Arc
from core.basic_validation_functions import BasicValidationFunctions
from core.point import Point

BasicValidationFunctions.X_MIN_COORDS = -100
BasicValidationFunctions.Y_MIN_COORDS = -100

@pytest.fixture
def sample_arc() -> Arc:
    """
    Fixture for Arc.
    """
    return Arc(Point(0, 0), Point(1, 0), Point(0, 1))

@pytest.fixture(params=[
    (Point(-1.0, 0)),
    (Point(math.cos(math.pi / 3), math.sin(math.pi / 3))),
    (Point(math.cos(-math.pi / 3), math.sin(-math.pi / 3))),
    (Point(math.cos(-2 * math.pi / 3), math.sin(-2 * math.pi / 3))),
    (Point(math.cos(-math.pi), math.sin(-math.pi))),
    (Point(math.cos(-4 * math.pi / 3), math.sin(-4 * math.pi / 3))),
])
def sample_point(request: pytest.FixtureRequest) -> Point:
    """
    Fixture for set of start points.
    """
    return request.param

class TestArc:
    """
    Tests for core class Arc.
    """

    def test_initialization(self) -> None:
        """
        Test for creating Arc.
        """
        center = Point(0, 0)
        p_start = Point(1, 0)
        p_end = Point(0, 1)

        arc = Arc(center, p_start, p_end, precision=1e-5)
        assert arc.center == center
        assert arc.p_start == p_start
        assert arc.p_end == p_end
        assert math.isclose(arc.radius, 1.0, abs_tol=arc.precision)

    def test_angle_start_property(self, sample_arc: Arc) -> None:
        """
        Test angle_start getter.
        """
        assert math.isclose(sample_arc.angle_start, 0, abs_tol=1e-5)

    @pytest.mark.parametrize(("new_start", "expected_angle"), [
        (Point(-1.0, 0), math.pi),
        (Point(math.cos(math.pi / 3), math.sin(math.pi / 3)), math.pi / 3),
        (Point(math.cos(-math.pi / 3), math.sin(-math.pi / 3)), -math.pi / 3),
        (Point(math.cos(-2 * math.pi / 3), math.sin(-2 * math.pi / 3)), -2 * math.pi / 3),
        (Point(math.cos(-math.pi), math.sin(-math.pi)), -math.pi),
        (Point(math.cos(-4 * math.pi / 3), math.sin(-4 * math.pi / 3)), 2 * math.pi / 3),
    ])
    def test_p_start_property(self, sample_arc: Arc, new_start: Point, expected_angle: float) -> None:
        """
        Test p_start getter and setter.

        Also test start angle adjustment.
        """
        sample_arc.p_start = new_start
        assert sample_arc.p_start == new_start
        assert math.isclose(sample_arc.angle_start, expected_angle, abs_tol=1e-5)

    def test_angle_end_property(self, sample_arc: Arc) -> None:
        """
        Test angle_end getter.
        """
        assert math.isclose(sample_arc.angle_end, math.pi / 2, abs_tol=1e-5)

    @pytest.mark.parametrize(("new_end", "expected_angle"), [
        (Point(-1.0, 0), math.pi),
        (Point(math.cos(math.pi / 3), math.sin(math.pi / 3)), math.pi / 3),
        (Point(math.cos(-math.pi / 3), math.sin(-math.pi / 3)), -math.pi / 3),
        (Point(math.cos(-2 * math.pi / 3), math.sin(-2 * math.pi / 3)), -2 * math.pi / 3),
        (Point(math.cos(-math.pi), math.sin(-math.pi)), -math.pi),
        (Point(math.cos(-4 * math.pi / 3), math.sin(-4 * math.pi / 3)), 2 * math.pi / 3),
    ])
    def test_p_end_property(self, sample_arc: Arc, new_end: Point, expected_angle: float) -> None:
        """
        Test p_end getter and setter.

        Also test end angle adjustment.
        """
        sample_arc.p_end = new_end
        assert sample_arc.p_end == new_end
        assert math.isclose(sample_arc.angle_end, expected_angle, abs_tol=1e-5)

    @pytest.mark.parametrize(("new_radius"), [
        (2), (3), (4), (5), (6), (7),
    ])
    def test_radius_property(self, new_radius: float, sample_point: Point) -> None:
        """
        Test radius getter and setter.

        Also test start and end point's adjustment.
        """
        start_point = Point(sample_point.x, sample_point.y)
        end_point = Point(sample_point.x, sample_point.y)
        arc = Arc(Point(0, 0), start_point, end_point)
        arc.radius = new_radius
        assert arc.radius == new_radius
        assert math.isclose(arc.p_start.distance_to(arc.center), new_radius, abs_tol=1e-5)
        assert math.isclose(arc.p_end.distance_to(arc.center), new_radius, abs_tol=1e-5)

    @pytest.mark.parametrize(("new_center"), [
        Point(2, 3),
        Point(3, 4),
        Point(-4, -5),
        Point(-5, 5),
        Point(6, -6),
        Point(0, 7),
    ])
    def test_center_property(self, new_center: Point, sample_point: Point) -> None:
        """
        Test center getter and setter.

        Also test start and end point's adjustment.
        """
        start_point = Point(sample_point.x, sample_point.y)
        end_point = Point(sample_point.x, sample_point.y)
        arc = Arc(Point(0, 0), start_point, end_point)
        arc.center = new_center
        assert arc.center == new_center
        assert math.isclose(arc.p_start.distance_to(arc.center), arc.radius, abs_tol=1e-5)
        assert math.isclose(arc.p_end.distance_to(arc.center), arc.radius, abs_tol=1e-5)

    def test_precision_property(self, sample_arc: Arc) -> None:
        """
        Test precision getter and setter.
        """
        sample_arc.precision = 1e-6
        assert sample_arc.precision == 1e-6

    def test_save_method(self, sample_arc: Arc) -> None:
        """
        Test save method.
        """
        str_saved = sample_arc.save()

        assert str_saved == (
            """{
    "center": [0, 0],
    "radius": 1.0,
    "angle_start": 0.0,
    "angle_end": 1.5707963267948966,
    "precision": 1e-05
}"""
        )

    def test_load_method(self) -> None:
        """
        Test load method.
        """
        string_data = """{
            "center": [0, 0],
            "radius": 1.0,
            "angle_start": 0.0,
            "angle_end": 1.5707963267948966,
            "precision": 1e-05
        }"""

        arc = Arc.load(string_data)

        assert math.isclose(arc.center.distance_to(Point(0, 0)), 0, abs_tol=1e-5)
        assert math.isclose(arc.p_start.distance_to(Point(1, 0)), 0, abs_tol=1e-5)
        assert math.isclose(arc.p_end.distance_to(Point(0, 1)), 0, abs_tol=1e-5)
        assert arc.precision == 1e-5
        assert arc.angle_start == 0
        assert math.isclose(arc.angle_end, math.pi / 2, abs_tol=1e-5)

    def test_creation_with_invalid_points(self) -> None:
        """
        Test exception in constructor.
        """
        center = Point(0, 0)
        p_start = Point(1, 0)
        p_end = Point(0, 2)

        with pytest.raises(ValueError, match="Invalid input points"):
            Arc(center, p_start, p_end)

    def test_change_start_point_on_invalid(self, sample_arc: Arc) -> None:
        """
        Test exception in p_start setter.
        """
        with pytest.raises(ValueError, match="Invalid input points"):
            sample_arc.p_start = Point(2, 3)

    def test_change_end_point_on_invalid(self, sample_arc: Arc) -> None:
        """
        Test exception in p_end setter.
        """
        with pytest.raises(ValueError, match="Invalid input points"):
            sample_arc.p_end = Point(2, 3)
