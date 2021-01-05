from Geometry2D import *


class RaiseEyebrows:
    def load(self, points):
        point17 = Point(points[17][0], points[17][1])
        point18 = Point(points[18][0], points[18][1])
        point19 = Point(points[19][0], points[19][1])
        point20 = Point(points[20][0], points[20][1])
        point21 = Point(points[21][0], points[21][1])
        left_triangle = Triangle(point17, point19, point21)

        point22 = Point(points[22][0], points[22][1])
        point23 = Point(points[23][0], points[23][1])
        point24 = Point(points[24][0], points[24][1])
        point25 = Point(points[25][0], points[25][1])
        point26 = Point(points[26][0], points[26][1])
        right_triangle = Triangle(point22, point24, point26)

        point0 = Point(points[0][0], points[0][1])
        point16 = Point(points[16][0], points[16][1])
        self.segment = Segment(point0, point16)

        left_angle = left_triangle.beta_angle * 57.2958
        right_angle = right_triangle.beta_angle * 57.2958

        condition1 = left_angle < 128 and right_angle < 128
        condition2 = abs(left_angle - right_angle) < 4

        div1 = self.compare_len(point17, point26)
        div2 = self.compare_len(point18, point25)
        div3 = self.compare_len(point19, point24)
        div4 = self.compare_len(point20, point23)
        div5 = self.compare_len(point21, point22)
        div = (div1 + div2 + div3 + div4 + div5) / 5
        condition3 = div >= 0.85

        return condition1 and condition3

    def compare_len(self, point1, point2):
        segment = self.segment
        perpendicular1 = getPerpendicular(segment, point1)
        point12 = perpendicular1.getCrossing(segment)
        segment1 = Segment(point1, point12)

        perpendicular2 = getPerpendicular(segment, point2)
        point22 = perpendicular2.getCrossing(segment)
        segment2 = Segment(point2, point22)

        return segment1.length / segment2.length if segment1.length < segment2.length else segment2.length / segment1.length
