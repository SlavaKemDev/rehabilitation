import cv2
import numpy
from Geometry2D import *


class FaceDetector:
    def __init__(self):
        self.detector = cv2.CascadeClassifier("cascades/frontal_face.xml")
        self.mouth_detector = cv2.CascadeClassifier("cascades/mouth.xml")

        self.landmark_detector = cv2.face.createFacemarkLBF()
        self.landmark_detector.loadModel("cascades/lbf_model.yaml")

    def detect(self, filename):
        if type(filename) == str:
            image = cv2.imread(filename)
        else:
            image = filename.copy()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # scan

        faces = self.detector.detectMultiScale(image_gray)

        max_face_size = 0
        for face in faces:
            face_size = face[2] * face[3]
            if face_size > max_face_size:
                face_final = face
                max_face_size = face_size
        if max_face_size == 0:
            return None, None
        else:
            cv2.rectangle(image, (face_final[0], face_final[1]),
                          (face_final[0] + face_final[2], face_final[1] + face_final[3]), (255, 255, 255), 2)
            _, landmarks = self.landmark_detector.fit(image_gray, numpy.array([face_final]))
            face_array = {
                "rectangle": face_final.tolist(),
                "landmarks": []
            }
            for landmark in landmarks:
                for x, y in landmark[0]:
                    cv2.circle(image, (int(x), int(y)), 2, (255, 255, 255))
                    face_array["landmarks"].append([x, y])
        if type(filename) == str:
            cv2.imwrite(filename, image)
            return face_array
        else:
            return face_array, image

    def detect_mouth(self, face_array, image):
        left_edge = Point(face_array["landmarks"][48][0], face_array["landmarks"][48][1])
        right_edge = Point(face_array["landmarks"][54][0], face_array["landmarks"][54][1])
        top_edge = Point(face_array["landmarks"][51][0], face_array["landmarks"][51][1])
        bottom_edge = Point(face_array["landmarks"][57][0], face_array["landmarks"][57][1])
        y_top = int(top_edge.y - abs(bottom_edge.y - top_edge.y))
        y_bottom = int(bottom_edge.y + abs(bottom_edge.y - top_edge.y))
        x_left = int(left_edge.x - abs(right_edge.x - left_edge.x) * 0.4)
        x_right = int(right_edge.x + abs(right_edge.x - left_edge.x) * 0.4)
        mouth_img = cv2.cvtColor(image[y_top:y_bottom, x_left:x_right], cv2.COLOR_BGR2GRAY)
        height, width = mouth_img.shape
        pixels_count = float(width * height)
        average_color = float(0)
        for y in range(height):
            for x in range(width):
                average_color += float(mouth_img[y, x]) / pixels_count

        half_width = width / 2
        half_height = height / 2
        top_point = Point(half_width, 0)
        bottom_point = Point(half_width, height)
        left_point = Point(0, half_height)
        right_point = Point(width, half_height)
        segment1 = Segment(top_point, right_point)
        segment2 = Segment(top_point, left_point)
        segment3 = Segment(left_point, bottom_point)
        segment4 = Segment(right_point, bottom_point)
        for y in range(height):
            for x in range(width):
                point = Point(x, y)
                if x > half_width:
                    if y > half_height:
                        # 4th quater
                    else:
                        # 1st quater
                        second_point = Point(x, y - 1)
                        ray = Ray(point, second_point)
                else:
                    if y > half_height:
                        # 3rd quater
                    else:
                        # 2nd quater
        for y in range(height):
            for x in range(width):
                pixel = mouth_img[y, x]
                if pixel < average_color - 40 or pixel > average_color - 10:
                    mouth_img[y, x] = 255
                else:
                    mouth_img[y, x] = 0
        return mouth_img
