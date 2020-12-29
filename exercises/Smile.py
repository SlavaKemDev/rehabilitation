from Geometry2D import *
import cv2


class Smile:
    def __init__(self):
        self.smile = cv2.CascadeClassifier("cascades/smile.xml")

    def load(self, points, image):
        top_point = Point(points[51][0], points[51][1])
        bottom_point = Point(points[57][0], points[57][1])
        left_point = Point(points[48][0], points[48][1])
        right_point = Point(points[54][0], points[54][1])

        top_up_ray = Ray(top_point, Point(points[51][0]-0.0000000001, points[51][1] - 1))
        left_right_segment = Segment(left_point, right_point)

        left_top = Segment(left_point, top_point)
        right_top = Segment(right_point, top_point)
        top_value = left_top.length / right_top.length if left_top.length < right_top.length else right_top.length / left_top.length

        left_bottom = Segment(left_point, bottom_point)
        right_bottom = Segment(right_point, bottom_point)
        bottom_value = left_bottom.length / right_bottom.length if left_bottom.length < right_bottom.length else right_bottom.length / left_bottom.length

        is_smile = left_right_segment.getCrossing(top_up_ray) is not None

        return top_value >= 0.85 and bottom_value >= 0.85 and is_smile

