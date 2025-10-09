"""Tests for core class Point."""
import json

import pytest

from core.point import Point


class TestPoint:
    """
    Tests for core class Point.
    """

    def test_initialization(self) -> None:
        """
        Test for creating point with positive coords.
        """
        point = Point(3.5, 4.2)
        assert point.x == 3.5
        assert point.y == 4.2

    def test_initialization_with_negative_coords(self) -> None:
        """
        Test for creating point with negative coords.
        """
        point = Point(-1.5, -2.5)
        assert point.x == -1.5
        assert point.y == -2.5

    def test_initialization_with_zero(self) -> None:
        """
        Test for creating point in (0, 0).
        """
        point = Point(0, 0)
        assert point.x == 0
        assert point.y == 0

    def test_x_property(self) -> None:
        """
        Test getter and setter for x coordinate.
        """
        point = Point(1, 2)
        point.x = 10.5
        assert point.x == 10.5

    def test_y_property(self) -> None:
        """
        Test getter and setter for y coordinate.
        """
        point = Point(1, 2)
        point.y = 20.5
        assert point.y == 20.5

    def test_coordinates_change_independently(self) -> None:
        """
        Specific test for coordinate.
        """
        point = Point(1, 2)
        point.x = 100
        assert point.y == 2

        point.y = 200
        assert point.x == 100


    def test_save_method(self) -> None:
        """
        Test save method with positive coords.
        """
        point = Point(3.14, 2.71)
        json_str = point.save()

        data = json.loads(json_str)
        assert data == [3.14, 2.71]

    def test_save_with_negative_coords(self) -> None:
        """
        Test save method with negative coords.
        """
        point = Point(-5.5, -10.2)
        json_str = point.save()
        data = json.loads(json_str)
        assert data == [-5.5, -10.2]

    def test_save_format_consistency(self) -> None:
        """
        Test save on independance of object.
        """
        point1 = Point(1, 2)
        point2 = Point(1, 2)
        assert point1.save() == point2.save()

    def test_str_representation(self) -> None:
        """
        Test string format with positive coords.
        """
        point = Point(1.5, 2.5)
        assert str(point) == "(1.5, 2.5)"

    def test_str_with_negative_coords(self) -> None:
        """
        Test string format with negative coords.
        """
        point = Point(-1.5, -2.5)
        assert str(point) == "(-1.5, -2.5)"

    def test_str_with_zero_coords(self) -> None:
        """
        Test string format with (0, 0) coords.
        """
        point = Point(0, 0)
        assert str(point) == "(0, 0)"

    # Parametrized tests
    @pytest.mark.parametrize(("x", "y", "expected_str"), [
        (1, 2, "(1, 2)"),
        (1.5, 2.5, "(1.5, 2.5)"),
        (-1, -2, "(-1, -2)"),
        (0, 0, "(0, 0)"),
        (1000000, 2000000, "(1000000, 2000000)"),
    ])
    def test_str_parametrized(self, x: float, y: float, expected_str: str) -> None:
        """
        Parametrized test of str format.
        """
        point = Point(x, y)
        assert str(point) == expected_str

    @pytest.mark.parametrize(("x", "y", "expected_json"), [
        (1, 2, [1, 2]),
        (1.5, 2.5, [1.5, 2.5]),
        (-1, -2, [-1, -2]),
        (0, 0, [0, 0]),
    ])
    def test_load_parametrized(self, x: float, y: float, expected_json: str) -> None:
        """
        Parametrized test to load.
        """
        point = Point(x, y)
        json_data = json.loads(point.save())
        assert json_data == expected_json

    # Should it work?
    def test_very_large_coordinates(self) -> None:
        """
        Test with big coords.
        """
        point = Point(1e10, 2e10)
        assert point.x == 1e10
        assert point.y == 2e10

        json_data = json.loads(point.save())
        assert json_data == [1e10, 2e10]

    def test_very_small_coordinates(self) -> None:
        """
        Test with low coords.
        """
        point = Point(1e-10, 2e-10)
        assert point.x == 1e-10
        assert point.y == 2e-10

    def test_float_precision(self) -> None:
        """
        Test for precision.
        """
        point = Point(1.123456789, 2.987654321)

        json_str = point.save()
        loaded_data = json.loads(json_str)
        assert loaded_data[0] == 1.123456789
        assert loaded_data[1] == 2.987654321

    def test_load_method(self) -> None:
        """
        Test load method work with Point class.
        """
        json_data = json.dumps([2, 3])

        point = Point.load(json_data)
        assert point.x == 2
        assert point.y == 3
        assert str(point) == "(2, 3)"


class TestPointEdgeCases:
    """
    Some specific tests for Point.
    """

    def test_multiple_reassignments(self) -> None:
        """
        Test of multiple rewriting.
        """
        point = Point(1, 2)

        for i in range(10):
            point.x = i * 1.5
            point.y = i * 2.5
            assert point.x == i * 1.5
            assert point.y == i * 2.5

    def test_save_after_coordinate_change(self) -> None:
        """
        Another save test.
        """
        point = Point(1, 2)
        initial_save = point.save()

        point.x = 10
        point.y = 20

        new_save = point.save()
        assert initial_save != new_save
        assert json.loads(new_save) == [10, 20]


@pytest.fixture
def sample_point() -> Point:
    """
    Fixture for a point.
    """
    return Point(5, 10)

@pytest.fixture
def origin_point() -> Point:
    """
    Fixture for a point.
    """
    return Point(0, 0)


def test_with_fixtures(sample_point: Point, origin_point: Point) -> None:
    """
    Test using fixtures.
    """
    assert sample_point.x == 5
    assert sample_point.y == 10
    assert origin_point.x == 0
    assert origin_point.y == 0


def test_distance_calculation() -> None:
    """
    Test of distance calculation.
    """
    p1 = Point(0, 3)
    p2 = Point(4, 0)
    assert p1.distance_to(p2) == 5
