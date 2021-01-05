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
from exercises.Smile import Smile
from exercises.StraightFace import StraightFace
from exercises.RaiseEyebrows import RaiseEyebrows
from exercises.FrownEyebrows import FrownEyebrows
tubelips = TubeLips()
smile = Smile()
straightface = StraightFace()
raiseeyebrows = RaiseEyebrows()
frowneyebrows = FrownEyebrows()



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


def exercise_check(image, exercise):
    cv2.imwrite("face.png", image)
    face_array, image, face_location = fd.detect(image)
    if face_array is None:
        return False
    x, y, w, h = face_location

    # square landmarks
    landmarks = []
    for landmark in face_array["landmarks"]:
        landmarks.append([landmark[0] - x, landmark[1] - y])

    grayscale_img = cv2.cvtColor(frame[y:y + h, x:x + h], cv2.COLOR_BGR2GRAY)
    cv2.imwrite("face.png", grayscale_img)
    correction = straightface.load(landmarks)
    if correction != True:
        return correction
    if exercise == "tube_lips":
        return tubelips.load(landmarks)
    elif exercise == "smile":
        return smile.load(landmarks)
    elif exercise == "raise_eyebrows":
        return raiseeyebrows.load(landmarks)
    elif exercise == "frown_eyebrows":
        return frowneyebrows.load(landmarks)
    else:
        return False


def exercise_output(image, exercise):
    print("\r", "Data:", exercise_check(image, exercise), end="")


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
        "name": "smile",
        "text": "Улыбнитесь",
        "time": 20
    },
    {
        "name": "wait",
        "text": "Перерыв",
        "time": 3
    },
    {
        "name": "tube_lips",
        "text": "Сделайте губы трубочкой",
        "time": 20
    },
    {
        "name": "wait",
        "text": "Перерыв",
        "time": 3
    },
    {
        "name": "raise_eyebrows",
        "text": "Поднимите брови вверх",
        "time": 20
    },
    {
        "name": "wait",
        "text": "Перерыв",
        "time": 3
    },
    {
        "name": "frown_eyebrows",
        "text": "Нахмурьтесь",
        "time": 20
    }
]
keep_going = True
exerciseID = 0
end_time = exercises[0]["time"] + time.time() + 1
while keep_going:
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    exercise = exercises[exerciseID]
    exercise_result = exercise_check(frame, exercise["name"])
    rem_time = end_time - time.time()
    if rem_time < 0:
        rem_time = 0
    if not exercise_result in [True, False]:
        print(f"\r{exercise_result} ({round(rem_time) if rem_time <= exercise['time'] else exercise['time']} с.)",
              end="")
    elif exercise_result:
        print(f"\r{exercise['text']}: OK", end="")
        if exerciseID < len(exercises) - 1:
            exerciseID += 1
            end_time = exercises[exerciseID]["time"] + time.time() + 1
        else:
            keep_going = False
    elif rem_time > 0:
        print(f"\r{exercise['text']} ({round(rem_time) if rem_time <= exercise['time'] else exercise['time']} с.)", end="")
    else:
        if exerciseID < len(exercises) - 1:
            exerciseID += 1
            end_time = exercises[exerciseID]["time"] + time.time() + 1
        else:
            keep_going = False


cap.release()
print("\nИспытание завершено")
