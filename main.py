import cv2
from Camera import Camera
from FaceDetector import FaceDetector
import os
import sys
from Geometry2D import *
import numpy
import time
import threading
import shutil


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
        "name": "smile",
        "text": "Smile!",
        "time": 5
    },
    {
        "name": "straw lips",
        "text": "Make your lips in a straw",
        "time": 5
    },
    {
        "name": "a letter",
        "text": "Say \"A\"",
        "time": 3
    }
]
exerciseNumber = 0
exerciseFrames = 0
allFrames = 0
lastTime = time.time() - 0.51
keep_going = True
while keep_going:
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    outFrame = frame.copy()
    outFrame = cv2.flip(outFrame, 1)
    exc = exercises[exerciseNumber]
    cv2.putText(outFrame, exc["text"], (5, 45), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0))
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
    cv2.imshow(window_name, outFrame)
    if exerciseNumber == 0 and exerciseFrames == 1:
        cv2.moveWindow(window_name, 0, 0)
cap.release()
exerciseNumber = 0
exerciseFrames = 0
for i in range(allFrames):
    exc = exercises[exerciseNumber]
    frame = cv2.imread(f"frames/frame{i}.png")
    face_array, image = fd.detect(frame)
    if face_array is None:
        continue
    mouth_img = fd.detect_mouth(face_array, frame)
    cv2.imwrite(f"mouth/mouth{i}.png", mouth_img)
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
    cv2.putText(image, "Exercise: " + exc["name"], (5, 75), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
    cv2.imwrite(f"frames/frame{i}.png", image)
    exerciseFrames += 1
    maxFrames = exc["time"] * fps
    if exerciseFrames >= maxFrames:
        if exerciseNumber + 1 < len(exercises):
            exerciseFrames = 0
            exerciseNumber += 1
sys.stdout.write(f"\rОбработка 100.0%: завершено\n")
print("Результаты сохранены в папку frames")
