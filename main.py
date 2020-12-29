import cv2
from Camera import Camera
from FaceDetector import FaceDetector
import os
import sys
from Geometry2D import *
import threading
import shutil
import time
from SymmetryEngine import SymmetryEngine


from exercises.TubeLips import TubeLips
tubelips = TubeLips()
from exercises.Smile import Smile
smile = Smile()


def play_sound(file):
    a = 1


try:
    shutil.rmtree("frames")
except:
    a = 1
try:
    os.mkdir("frames")
except:
    a = 1
try:
    shutil.rmtree("mouth")
except:
    a = 1
try:
    os.mkdir("mouth")
except:
    a = 1

window_name = "Rehabilitation testing"
fd = FaceDetector()
se = SymmetryEngine()
cam = Camera(10)
imageCount = 60
tasks = ("smile")
taskProgress = 0
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
width = int(cap.get(3))  # float
height = int(cap.get(4))  # float
fps = 2  # int(cap.get(5) / 1.5)
# print(width, height, fps)
frames = fps * 5
exercises = [
    {
        "name": "test",
        "text": "Test Exercise",
        "time": 5
    }
]
exerciseNumber = 0
exerciseFrames = 0
allFrames = 0
lastTime = time.time() - 0.51
keep_going = True
prev_sign = ""
while keep_going:
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    outFrame = frame.copy()
    outFrame = cv2.flip(outFrame, 1)
    exc = exercises[exerciseNumber]
    cv2.putText(outFrame, exc["text"], (5, 45), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0))
    if exc["text"] != prev_sign:
        print(exc["text"])
        prev_sign = exc["text"]
    if time.time() >= lastTime + 1 / fps:
        # out.write(frame)
        cv2.imwrite(f"frames/frame{allFrames}.png", frame)
        allFrames += 1
        exerciseFrames += 1
        maxFrames = exc["time"] * fps
        lastTime = time.time()
        if exerciseFrames >= maxFrames:
            threading.Thread(target=play_sound, args=('sounds/success.mp3',), daemon=True).start()
            if exerciseNumber + 1 < len(exercises):
                exerciseFrames = 0
                exerciseNumber += 1
            else:
                keep_going = False
    #white_rect = numpy.ones(outFrame.shape, dtype=numpy.uint8) * 255
    #outFrame = cv2.addWeighted(outFrame, 0.9, white_rect, 0.9, 1.0)
    '''cv2.imshow(window_name, outFrame)
    if exerciseNumber == 0 and exerciseFrames == 1:
        cv2.moveWindow(window_name, 0, 0)'''
print("OK")
cap.release()
exerciseNumber = 0
exerciseFrames = 0
mouth_data = []
for i in range(allFrames):
    exc = exercises[exerciseNumber]
    frame = cv2.imread(f"frames/frame{i}.png")
    face_array, image, face_location = fd.detect(frame)
    if face_array is None:
        mouth_data.append(False)
        continue
    x, y, w, h = face_location

    # square landmarks
    landmarks = []
    for landmark in face_array["landmarks"]:
        landmarks.append([landmark[0] - x, landmark[1] - y])
    print(landmarks)

    grayscale_img = cv2.cvtColor(frame[y:y+h, x:x+h], cv2.COLOR_BGR2GRAY)
    se.set_face_array(face_array)
    se.get_symmetry()
    mouth, points = fd.detect_mouth(face_array, frame)
    cv2.imwrite(f"mouth/mouth{i}.png", mouth)
    mouth_symmetry = se.get_mouth_symmetry(mouth, points)
    mouth_data.append(mouth_symmetry)
    print("Рот: ", mouth_symmetry)
    print("Трубочка: ", tubelips.load(landmarks))
    print("Улыбка: ", smile.load(landmarks, grayscale_img))
    cv2.imwrite("face.png", grayscale_img)
    left_border = Point(
        face_array["landmarks"][48][0],
        face_array["landmarks"][48][1]
    )
    right_border = Point(
        face_array["landmarks"][54][0],
        face_array["landmarks"][54][1]
    )
    top_border = Point(
        face_array["landmarks"][51][0],
        face_array["landmarks"][51][1]
    )
    bottom_border = Point(
        face_array["landmarks"][57][0],
        face_array["landmarks"][57][1]
    )
    triangle = Triangle(left_border, bottom_border, right_border)
    segment = Segment(left_border, right_border)
    perp = getPerpendicular(segment, top_border)
    cross_point = segment.getCrossing(perp)
    length = ((cross_point.x - top_border.x) ** 2 + (cross_point.y - top_border.y) ** 2) ** 0.5
    sys.stdout.write(f"\rОбработка {round(i / allFrames * 10000) / 100}%")
    cv2.putText(image, "Smile: " + str(length), (5, 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
    cv2.putText(image, "Alpha: " + str(triangle.alpha_angle / math.pi * 180), (5, 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (0, 0, 0))
    cv2.putText(image, "Beta: " + str(triangle.beta_angle / math.pi * 180), (5, 45), cv2.FONT_HERSHEY_PLAIN, 1,
                (0, 0, 0))
    cv2.putText(image, "Gamma: " + str(triangle.gamma_angle / math.pi * 180), (5, 60), cv2.FONT_HERSHEY_PLAIN, 1,
                (0, 0, 0))
    cv2.putText(image, "Mouth: " + "yes" if mouth_symmetry else "error" + "%", (5, 75), cv2.FONT_HERSHEY_PLAIN, 1,
                (0, 0, 0))
    cv2.putText(image, "Exercise: " + exc["name"], (5, 90), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
    cv2.imwrite(f"frames/frame{i}.png", image)
    exerciseFrames += 1
    maxFrames = exc["time"] * fps
    if exerciseFrames >= maxFrames:
        if exerciseNumber + 1 < len(exercises):
            exerciseFrames = 0
            exerciseNumber += 1
sys.stdout.write(f"\rОбработка 100.0%: завершено\n")
mouth_result = mouth_data.count(True) / len(mouth_data)
print(f"Рот: {round(mouth_result * 10000) / 100} %")
print("Результаты сохранены в папку frames")


if mouth_result <= 0.2:
    print("Вам необходиимо выполнить профилактические упражнения")
elif mouth_result <= 0.4:
    print("Вам настоятельно рекомендуется выполнить профилактические упражнения")
elif mouth_result <= 0.6:
    print("Вам рекомендуется выполнить профилактические упражнения")
elif mouth_result <= 0.8:
    print("Вам было бы неплохо выполнить профилактические упражнения")
else:
    print("На вашем лице не обраружно искажений")
