"""Tests for core class Polygon."""

import pytest

from core.point import Point
from core.polygon import Polygon


@pytest.fixture
def sample_polygon() -> Polygon:
    """
    Fixture for Polygon.
    """
    return Polygon([Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])


@pytest.fixture
def sample_points() -> list[Point]:
    """
    Fixture for point list.
    """
    return [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1), Point(0, 0)]


class TestPolygon:
    """
    Tests for core class Polygon.
    """

    def test_initialization(self, sample_points: list[Point]) -> None:
        """
        Test for creating Polygon.
        """
        polygon = Polygon(sample_points)
        for ind, point in enumerate(sample_points):
            assert str(polygon.points[ind]) == str(point)

    def test_points_property(self, sample_polygon: Polygon, sample_points: list[Point]) -> None:
        """
        Test getter and setter for polygon list of points.
        """
        sample_polygon.points = sample_points
        assert sample_polygon.points == sample_points

    def test_save_method(self, sample_polygon: Polygon) -> None:
        """
        Test save method.
        """
        str_saved = sample_polygon.save()

        assert str_saved == ("[0, 0]; [1, 0]; [1, 1]; [0, 1]; [0, 0]")

    def test_save_format_consistency(self, sample_polygon: Polygon) -> None:
        """
        Test save independance of object.
        """
        polygon = Polygon(sample_polygon.points)

        assert sample_polygon is not polygon
        assert sample_polygon.save() == polygon.save()

    def test_str_representation(self, sample_polygon: Polygon) -> None:
        """
        Test polygon format.
        """
        assert str(sample_polygon) == ("[(0, 0) (1, 0) (1, 1) (0, 1) (0, 0)]")

    def test_reassignment_of_points(self, sample_polygon: Polygon) -> None:
        """
        Test of rewriting.
        """
        new_points = [Point(0, 0), Point(1, 1), Point(0, 1)]
        sample_polygon.points = new_points
        assert sample_polygon.points == [*new_points, Point(0, 0)]

    def test_change_point_list(self, sample_polygon: Polygon, sample_points: list[Point]) -> None:
        """
        Test about independency of data in list data of polygon.
        """
        sample_polygon.points = sample_points
        sample_points[0] = Point(7, 13)
        assert sample_polygon.points[0] != Point(7, 13)
        assert sample_polygon.points != sample_points

    def test_load_method(self) -> None:
        """
        Test load method work with Polygon class.
        """
        string_data = "[1, 2]; [2, 3]; [3, 4]; [4, 5]; [1, 2]"

        poly = Polygon.load(string_data)
        assert poly.points[0] == Point(1, 2)
        assert poly.points[1] == Point(2, 3)
        assert poly.points[2] == Point(3, 4)
        assert poly.points[3] == Point(4, 5)

    def test_check_on_convex_method(self) -> None:
        """
        Test check on convex method.
        """
        convex_list_of_points = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1), Point(0, 0)]
        not_convex_list_of_points = [
            Point(0, 0),
            Point(1, 0),
            Point(1, 1),
            Point(0.5, 0.5),
            Point(0, 1),
            Point(0, 0),
        ]
        assert Polygon.check_on_convex(convex_list_of_points)
        assert not Polygon.check_on_convex(not_convex_list_of_points)

    def test_getitem_attribute(self, sample_polygon: Polygon, sample_points: list[Point]) -> None:
        """
        Test getitem method.
        """
        for i in range(len(sample_polygon.points) - 1):
            point = sample_polygon[i]
            assert point == sample_points[i]

    def test_setitem_attribute(self, sample_polygon: Polygon) -> None:
        """
        Test setitem method.
        """
        sample_polygon[1] = Point(2, 0)
        assert sample_polygon[1] == Point(2, 0)
