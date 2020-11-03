from Geometry2D import *
import cv2

class SymmetryEngine:

    def set_face_array(self, face_array):
        self.face_array = face_array
        self.landmarks = face_array["landmarks"]

    def create_symmetry_axis(self):
        landmarks = self.landmarks
        left_top = Point(landmarks[21][0], landmarks[21][1])
        right_top = Point(landmarks[22][0], landmarks[22][1])
        left_bottom = Point(landmarks[5][0], landmarks[5][1])
        right_bottom = Point(landmarks[11][0], landmarks[11][1])

        segment1 = Segment(left_top, right_top)
        segment2 = Segment(left_bottom, right_bottom)

        point1 = segment1.get_center_point()
        point2 = segment2.get_center_point()
        self.axis = Straight(point1, point2)

    def get_symmetry(self):
        landmarks = self.landmarks
        self.create_symmetry_axis()
        cross1, ratio1 = self.get_crossing_data(Point(landmarks[4][0], landmarks[4][1]),
                                                Point(landmarks[12][0], landmarks[12][1]))
        cross2, ratio2 = self.get_crossing_data(Point(landmarks[48][0], landmarks[48][1]),
                                                Point(landmarks[54][0], landmarks[54][1]))
        print("\nАнализ симметрии:")
        print(f"Отношение 1 пары точек: {ratio1},")
        print(f"Отношение 2 пары точек: {ratio2}\n")

    def get_crossing_data(self, point1: Point, point2: Point):
        axis = self.axis
        perpendicular = getPerpendicular(axis, point1)
        cross_point = perpendicular.getCrossing(axis)

        segment1 = Segment(point1, cross_point)
        segment2 = Segment(point2, cross_point)
        length1 = segment1.length
        length2 = segment2.length

        if length1 > length2:
            ratio = length2 / length1
        else:
            ratio = length1 / length2
        return cross_point, ratio
