from Geometry2D import *
class StraightFace:
    def __init__(self):
        self.error_codes = [
            "Поверните лицо немного влево",
            "Поверните лицо немного вправо",
            "Немного наклоните голову к левому плечу",
            "Немного наклоните голову к правому плечу"
        ]

    def load(self, points):
        point27 = Point(points[27][0], points[27][1])  # верхний край носа
        point30 = Point(points[30][0], points[30][1])  # нижний край носа
        point30_left = Point(points[30][0] - 1, points[30][1] - 0.00000001)  # точка, чуть левее нижнего края носа
        point39 = Point(points[39][0], points[39][1])  # край левого глаза (со стороны наблюдателя)
        point42 = Point(points[42][0], points[42][1])  # край правого глаза (со стороны наблюдателя)
        left_segment = Segment(point39, point27)  # отрезок от края левого глаза до носа
        right_segment = Segment(point42, point27)  # отрезок от края правого глаза до носа
        if left_segment.length > right_segment.length:
            if right_segment.length / left_segment.length < 0.7:  # если для нас правый короче левого
                return self.error_codes[1]  # результат зеркальный
        else:
            if left_segment.length / right_segment.length < 0.7:  # если для нас левый короче правого
                return self.error_codes[0]  # результат зеркальный
        nose_triangle = Triangle(point27, point30, point30_left)
        angle = nose_triangle.beta_angle
        angle_ratio = angle / 1.577 if angle < 1.577 else 1.577 / angle
        return angle_ratio > 0.9
