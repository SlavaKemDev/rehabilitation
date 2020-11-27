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

    def get_mouth_symmetry(self, mouth_img, points):
        self.create_symmetry_axis()

        left_top_point = points[0]
        right_bottom_point = points[1]

        y_line_1 = left_top_point.y
        x_line_1 = self.axis.getX(y_line_1)

        y_line_2 = right_bottom_point.y
        x_line_2 = self.axis.getX(y_line_2)

        if x_line_1 is None or x_line_2 is None:  # если ось симмтерии не проходит через область рта
            return 0

        height, width = mouth_img.shape[:2]
        y_line_1 -= left_top_point.y
        x_line_1 -= left_top_point.x

        y_line_2 -= left_top_point.y
        x_line_2 -= left_top_point.x

        left_top_point = Point(x_line_1, y_line_1)
        right_bottom_point = Point(x_line_2, y_line_2)

        axis = Straight(left_top_point, right_bottom_point)

        delta_y = y_line_2 - y_line_1

        output_list = []

        max_fault = math.ceil(width * 0.2)

        for y in range(delta_y):
            x = round(axis.getX(y))
            if width - x > x:
                ranges = width - x
            else:
                ranges = x

            left_length = None
            right_length = None
            for i in range(1, ranges + 1):
                x1 = x - i
                x2 = x + i
                # сравнение слева
                if 0 <= x1 < width:  # только если x не пересекает границу слева
                    if mouth_img[y, x1] == 63:  # если это пиксель обводки
                        left_length = i  # длина до пикселя

                # сравнение справа
                if 0 <= x2 < width:  # только если x не пересекает границу справа
                    if mouth_img[y, x2] == 63:  # если это пиксель обводки
                        right_length = i  # длина до пикселя

            if left_length is None and right_length is None:  # если нет точки ни слева, ни справа
                continue  # то, скорее всего тут ничего и недолжно быть, идём дальше
            elif left_length is None or right_length is None:  # если нет точки либо слева, либо справа
                output_list.append(False)  # то непорядок, сравнение не пройдено
            else:  # если обе точки на месте
                output_list.append(abs(left_length - right_length) <= max_fault)
        return output_list.count(True) / len(output_list) > 0.4
