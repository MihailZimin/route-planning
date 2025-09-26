import pytest
from core.geometry_objects import Point


@pytest.fixture
def simple_point_str() -> str:
    return "{x: 1, y: 2}"


@pytest.fixture
def simple_point() -> Point:
    return Point(1, 2)


def test_serialize(simple_point, simple_point_str) -> None:
    p = simple_point
    assert p.save() == simple_point_str


def test_deserialize(simple_point, simple_point_str) -> None:
    assert Point.load(simple_point_str) == simple_point_str


def test_setter_x() -> None: ...
def test_setter_y() -> None: ...
def test_getter_x() -> None: ...
def test_getter_y() -> None: ...
