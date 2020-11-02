import numpy
import math

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class LinearFunction:
    def __init__(self, k: float, b: float):
        self.k = k
        self.b = b
        self.min = float("-inf")
        self.max = float("inf")

    def getCrossing(self, function) -> Point:
        k1 = self.k
        b1 = self.b
        k2 = function.k
        b2 = function.b
        M1 = numpy.array([
            [float(-k1), 1.0],
            [float(-k2), 1.0]
        ])
        v1 = numpy.array([
            [b1],
            [b2]
        ])
        solution = numpy.linalg.solve(M1, v1).tolist()
        x = solution[0][0]
        y = solution[1][0]
        if x < self.min or x < function.min or x > self.max or x > function.max:
            return None
        else:
            return Point(x, y)


class Straight(LinearFunction):
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        deltaX = point1.x - point2.x
        deltaY = point1.y - point2.y
        k = deltaX / deltaY
        b = point1.y - k * point1.x

        M1 = numpy.array([
            [point1.x, 1.0],
            [point2.x, 1.0]
        ])
        v1 = numpy.array([
            [point1.y],
            [point2.y]
        ])
        solution = numpy.linalg.solve(M1, v1).tolist()
        k = solution[0][0]
        b = solution[1][0]

        super().__init__(k, b)


class Segment(Straight):
    def __init__(self, point1: Point, point2: Point):
        super().__init__(point1, point2)
        self.length = ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5
        if point1.x < point2.x:
            self.min = point1.x
            self.max = point2.x
        else:
            self.min = point2.x
            self.max = point1.x

    def get_center_point(self) -> Point:
        x1 = self.point1.x
        y1 = self.point1.y
        x2 = self.point2.x
        y2 = self.point2.y
        delta_x = x1 - x2
        delta_y = y1 - y2
        point = Point(x1 - (delta_x / 2), y1 - (delta_y / 2))
        return point


class Ray(Straight):
    def __init__(self, point1, point2):
        # точка 1 - всегда конец луча, а через точку 2 он продолжается
        super().__init__(point1, point2)
        if point1.x < point2.x:
            self.min = point1.x
        else:
            self.max = point1.x


class Triangle:
    def __init__(self, point1: Point, point2: Point, point3: Point):
        #sides
        self.a_segment = Segment(point1, point2)
        self.b_segment = Segment(point2, point3)
        self.c_segment = Segment(point3, point1)

        a = self.a_segment.length
        b = self.b_segment.length
        c = self.c_segment.length
        #angles
        self.alpha_angle = math.acos(
            (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
        )
        self.beta_angle = math.acos(
            (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        )
        self.gamma_angle = math.acos(
            (b ** 2 + c ** 2 - a ** 2) / (2 * c * b)
        )


class Geometry2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = []
        self.segments = []

    def createPoint(self, x, y) -> Point:
        point = Point(x, y)
        return point

    def createSegment(self, point1: Point, point2: Point) -> Segment:
        segment = Segment(point1, point2)
        return segment


def getPerpendicular(function: LinearFunction, point: Point):
    k1 = function.k
    k2 = -1 / k1
    x = point.x
    y = point.y
    b2 = y - k2 * x
    function2 = LinearFunction(k2, b2)
    return function2
