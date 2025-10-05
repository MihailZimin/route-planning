"""Tests for core class Circle."""
import pytest

from core.circle import Circle
from core.point import Point


@pytest.fixture
def sample_circle() -> Circle:
    """
    Fixture for Circle.
    """
    return Circle(Point(2, 5), 5.5)


class TestCircle:
    """
    Tests for core class Circle.
    """

    def test_initialization(self) -> None:
        """
        Test for creating Circle.
        """
        circle = Circle(Point(3, 4), 5.6)
        assert str(circle) == "(3, 4); radius=5.6"

    def test_radius_property(self, sample_circle: Circle) -> None:
        """
        Test getter and setter for radius of circle.
        """
        sample_circle.radius = 10
        assert sample_circle.radius == 10

    def test_center_property(self, sample_circle: Circle) -> None:
        """
        Test getter and setter for center of circle.
        """
        sample_circle.center = Point(13, 14)
        assert sample_circle.center == Point(13, 14)

    def test_save_method(self, sample_circle: Circle) -> None:
        """
        Test save method.
        """
        str_saved = sample_circle.save()

        assert str_saved == "[2, 5]; 5.5"

    def test_save_format_consistency(self, sample_circle: Circle) -> None:
        """
        Test save independance of object.
        """
        circle = Circle(Point(2, 5), 5.5)

        assert sample_circle is not circle
        assert sample_circle.save() == circle.save()

    def test_str_representation(self, sample_circle: Circle) -> None:
        """
        Test circle format.
        """
        assert str(sample_circle) == "(2, 5); radius=5.5"

    def test_multiple_reassignements(self, sample_circle: Circle) -> None:
        """
        Test of mupltiple rewriting.
        """
        for i in range(10):
            sample_circle.radius = i
            sample_circle.center = Point(4 * i, 6 * i)
            assert sample_circle.center == Point(4 * i, 6 * i)
            assert sample_circle.radius == i

    def test_save_after_coordinate_change(self, sample_circle: Circle) -> None:
        """
        Another save test.
        """
        initial_save = sample_circle.save()

        sample_circle.center = Point(2, 2)

        new_save = sample_circle.save()
        assert initial_save != new_save

    def test_load_method(self) -> None:
        """
        Test load method work with circle class.
        """
        string_data = "[1, 2]; 5.6"

        circle = Circle.load(string_data)
        assert circle.center == Point(1, 2)
        assert circle.radius == 5.6
