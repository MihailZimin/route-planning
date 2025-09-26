from abc import ABC, abstractmethod


class ABCGeo(ABC):
    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def load(self) -> None:
        pass


class Point(ABCGeo):
    def __init__(self, x: float, y: float) -> None:
        self._xCoord = x
        self._yCoord = y

    def save(self) -> None:
        pass

    def load(self) -> None:
        pass

    @property
    def xCoord(self) -> float:
        return self._xCoord
    
    @xCoord.setter
    def xCoord(self, x: float) -> None:
        # check of possible value
        self._xCoord = x

    @property
    def yCoord(self) -> float:
        return self._yCoord
    
    @yCoord.setter
    def yCoord(self, y: float) -> None:
        # check of possible value
        self._yCoord = y

    def __str__(self) -> str:
        return f"{self._xCoord}, {self._yCoord}"


class Line(ABCGeo):
    def __init__(self, start: Point, end: Point) -> None:
        self._start = start
        self._end = end

    def save(self) -> None:
        pass

    def load(self) -> None:
        pass

    @property
    def start(self) -> Point:
        return self._start
    
    @property.setter
    def start(self, start: Point) -> None:
        self._start = start

    @property
    def end(self) -> Point:
        return self._end
    
    @property.setter
    def end(self, end: Point) -> None:
        self._end = end


class Polygon(ABCGeo):
    def __init__(self, points: list[Point]) -> None:
        self._points = points

    def save(self) -> None:
        pass

    def load(self) -> None:
        pass

    @property
    def points(self) -> list[Point]:
        return self._points
    
    @property.setter
    def points(self, points: list[Point]) -> None:
        self._points = points


class Circle(ABCGeo):
    def __init__(self, radius: float, center: Point) -> None:
        self._radius = radius
        self._center = center

    @property
    def radius(self) -> float:
        return self._radius
    
    @property.setter
    def radius(self, radius: float) -> None:
        self._radius = radius

    @property
    def center(self) -> Point:
        return self._center
    
    @property.setter
    def center(self, center: Point) -> None:
        self._center = center


class Arc(ABCGeo):
    def __init__(self, radius: float, center: Point, angle: float) -> None:
        self._radius = radius
        self._center = center
        self._angle = angle

    @property
    def radius(self) -> float:
        return self._radius
    
    @property.setter
    def radius(self, radius: float) -> None:
        self._radius = radius

    @property
    def center(self) -> Point:
        return self._center
    
    @property.setter
    def center(self, center: Point) -> None:
        self._center = center

    @property
    def angle(self) -> float:
        return self._angle
    
    @property.setter
    def angle(self, angle: float) -> None:
        self._angle = angle