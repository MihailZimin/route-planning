"""Tests for core class Line."""


import pytest

from core.line import Line
from core.point import Point


@pytest.fixture
def sample_line() -> Line:
    """
    Fixture for line.
    """
    return Line(Point(1, 2), Point(2, 3))


class TestLine:
    """
    Tests for core class Line.
    """

    def test_initialization(self) -> None:
        """
        Test for creating line.
        """
        start = Point(1, 2)
        end = Point(2, 3)
        line = Line(start, end)
        assert line.start == start
        assert line.end == end

    def test_start_property(self, sample_line: Line) -> None:
        """
        Test getter and setter for start point.
        """
        start = Point(3, 4)
        sample_line.start = start
        assert sample_line.start == start

    def test_end_property(self, sample_line: Line) -> None:
        """
        Test getter and setter for end point.
        """
        end = Point(1, 2)
        sample_line.end = end
        assert sample_line.end == end

    def test_save_method(self, sample_line: Line) -> None:
        """
        Test save method.
        """
        str_saved = sample_line.save()

        assert str_saved == "[1, 2]; [2, 3]"

    def test_save_format_consistency(self, sample_line: Line) -> None:
        """
        Test save on independance of object.
        """
        line = Line(Point(1, 2), Point(2, 3))

        assert sample_line is not line
        assert sample_line.save() == line.save()

    def test_str_representation(self, sample_line: Line) -> None:
        """
        Test line format.
        """
        assert str(sample_line) == "(1, 2), (2, 3)"

    def test_load_method(self) -> None:
        """
        Test load method work with Line class.
        """
        string_data = "[1, 2]; [2, 3]"

        line = Line.load(string_data)
        assert line.start == Point(1, 2)
        assert line.end == Point(2, 3)

    def test_multiple_reassignments(self, sample_line: Line) -> None:
        """
        Test of multiple rewriting.
        """
        for i in range(10):
            sample_line.start.x = i * 1.5
            sample_line.start.y = i * 2.5
            sample_line.end.x = i * 3
            sample_line.end.y = i * 3
            assert sample_line.start.x == i * 1.5
            assert sample_line.start.y == i * 2.5
            assert sample_line.end.x == i * 3
            assert sample_line.end.y == i * 3

    def test_save_after_coordinate_change(self, sample_line: Line) -> None:
        """
        Another save test.
        """
        initial_save = sample_line.save()

        sample_line.start = Point(10, 10)
        sample_line.end = Point(4, 4)

        new_save = sample_line.save()
        assert initial_save != new_save
        assert new_save == "[10, 10]; [4, 4]"
