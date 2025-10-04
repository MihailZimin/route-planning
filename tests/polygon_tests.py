"""Tests for core class Polygon."""

import json

import pytest

from core.point import Point
from core.polygon import Polygon


@pytest.fixture
def sample_polygon() -> Polygon:
    """
    Fixture for Polygon.
    """
    return Polygon([Point(i, 10 * i) for i in range(10)])

@pytest.fixture
def sample_points() -> list[Point]:
    """
    Fixture for point list.
    """
    return [Point(i, 5 * i) for i in range(10)]


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
        json_str = sample_polygon.save()

        data = json.loads(json_str)
        assert data == [
            "[0, 0]", "[1, 10]", "[2, 20]", "[3, 30]", "[4, 40]",
            "[5, 50]", "[6, 60]", "[7, 70]", "[8, 80]", "[9, 90]"
        ]

    def test_save_format_consistency(self, sample_polygon: Polygon) -> None:
        """
        Test save independance of object.
        """
        polygon = Polygon([Point(i, 10 * i) for i in range(10)])

        assert sample_polygon is not polygon
        assert sample_polygon.save() == polygon.save()

    def test_str_representation(self, sample_polygon: Polygon) -> None:
        """
        Test polygon format.
        """
        assert str(sample_polygon) == (
            "['(0, 0)', '(1, 10)', '(2, 20)', '(3, 30)', '(4, 40)', "
            "'(5, 50)', '(6, 60)', '(7, 70)', '(8, 80)', '(9, 90)']"
        )

    def test_mupltiple_reassignments(self, sample_polygon: Polygon) -> None:
        """
        Test of multiple rewriting.
        """
        for i in range(10):
            sample_polygon.points = [Point(j, j * i) for j in range(i+5)]
            assert sample_polygon.points == [Point(j, j * i) for j in range(i+5)]

    def test_save_after_coordinate_change(
            self, sample_polygon: Polygon, sample_points: Point) -> None:
        """
        Another save test.
        """
        initial_save = sample_polygon.save()

        sample_polygon.points = sample_points

        new_save = sample_polygon.save()
        assert initial_save != new_save
