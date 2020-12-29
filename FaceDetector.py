import cv2
import numpy
from Geometry2D import *


class FaceDetector:
    def __init__(self):
        self.detector = cv2.CascadeClassifier("cascades/frontal_face.xml")
        self.mouth_detector = cv2.CascadeClassifier("cascades/mouth.xml")

        self.landmark_detector = cv2.face.createFacemarkLBF()
        self.landmark_detector.loadModel("cascades/lbf_model.yaml")

    def fill_color(self, image, to_color, position):
        pos_y = position[0]
        pos_x = position[1]
        from_color = image[pos_y, pos_x]
        image[pos_y, pos_x] = to_color
        tasks = [position]
        print(from_color, to_color, position, tasks)
        while len(tasks) > 0:
            pos = tasks.pop(0)
            pos_y = pos[0]
            pos_x = pos[1]
            try:
                if image[pos_y - 1, pos_x] == from_color:
                    image[pos_y - 1, pos_x] = to_color
                    tasks.append((pos_y - 1, pos_x))
            except:
                pass
            try:
                if image[pos_y, pos_x + 1] == from_color:
                    image[pos_y, pos_x + 1] = to_color
                    tasks.append((pos_y, pos_x + 1))
            except:
                pass
            try:
                if image[pos_y + 1, pos_x] == from_color:
                    image[pos_y + 1, pos_x] = to_color
                    tasks.append((pos_y + 1, pos_x))
            except:
                pass
            try:
                if image[pos_y, pos_x - 1] == from_color:
                    image[pos_y, pos_x - 1] = to_color
                    tasks.append((pos_y, pos_x - 1))
            except:
                pass

    def has_same_pixel(self, image, position, direction):
        try:
            pos_y = position[0]
            pos_x = position[1]
            color = image[pos_y, pos_x]
            if direction == "top":
                pos_y -= 1
            elif direction == "bottom":
                pos_y += 1
            elif direction == "left":
                pos_x -= 1
            elif direction == "right":
                pos_x += 1
            new_color = image[pos_y, pos_x]
            return color == new_color
        except:
            return False

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
            lmn = 0
            for landmark in landmarks:
                for x, y in landmark[0]:
                    cv2.circle(image, (int(x), int(y)), 2, (255, 255, 255))
                    cv2.putText(image, str(lmn), (x, y),
                                cv2.FONT_HERSHEY_PLAIN, 0.8,
                                (63, 63, 63) if lmn % 2 == 0 else (0, 0, 0))
                    face_array["landmarks"].append([x, y])
                    lmn += 1
        if type(filename) == str:
            cv2.imwrite(filename, image)
            return face_array
        else:
            return face_array, image, face_final

    def detect_mouth(self, face_array, image):
        if face_array is None:
            return image
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

        top_left_point = Point(0, 0)
        top_right_point = Point(width, 0)
        bottom_left_point = Point(0, height)
        bottom_right_point = Point(width, half_height)
        for y in range(height):
            for x in range(width):
                pixel = mouth_img[y, x]
                if pixel < average_color - 40 or pixel > average_color - 10:  # -40 -10
                    mouth_img[y, x] = 255
                else:
                    mouth_img[y, x] = 191
        x_start = round(half_width)
        y_start = round(half_height)
        if half_width < half_height:
            iterations = x_start
        else:
            iterations = y_start
        final_pos = (0, 0)
        for i in range(iterations):
            try:
                if mouth_img[y_start - i, x_start] == 191:
                    final_pos = (y_start - i, x_start)
                    break
            except:
                pass
        print(final_pos)
        self.fill_color(mouth_img, 127, final_pos)
        copy_mouth = mouth_img.copy()
        mouth_top_point = None
        mouth_bottom_point = None
        mouth_left_point = None
        mouth_right_point = None
        for y in range(height):
            for x in range(width):
                bottom_y = height - 1 - y
                if not self.has_same_pixel(copy_mouth, (y, x), "top") and mouth_img[y, x] == 127:
                    mouth_img[y, x] = 63
                    if mouth_top_point is None:
                        mouth_top_point = (x, y)
                        cv2.circle(mouth_img, mouth_top_point, 3, 0)
                if not self.has_same_pixel(copy_mouth, (bottom_y, x), "bottom") and mouth_img[bottom_y, x] == 127:
                    mouth_img[bottom_y, x] = 63
                    if mouth_bottom_point is None:
                        mouth_bottom_point = (x, bottom_y)
                        cv2.circle(mouth_img, mouth_bottom_point, 3, 0)
        for x in range(width):
            for y in range(height):
                right_x = width - 1 - x
                if not self.has_same_pixel(copy_mouth, (y, x), "left") and mouth_img[y, x] == 127:
                    mouth_img[y, x] = 63
                    if mouth_left_point is None:
                        mouth_left_point = (x, y)
                        cv2.circle(mouth_img, mouth_left_point, 3, 0)
                if not self.has_same_pixel(copy_mouth, (y, right_x), "right") and mouth_img[y, right_x] == 127:
                    mouth_img[y, right_x] = 63
                    if mouth_right_point is None:
                        mouth_right_point = (right_x, y)
                        cv2.circle(mouth_img, mouth_right_point, 3, 0)
        return mouth_img, [Point(x_left, y_top), Point(x_right, y_bottom)]
