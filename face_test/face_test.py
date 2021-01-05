import cv2
from FaceDetector import FaceDetector
from exercises.StraightFace import StraightFace
stf = StraightFace()
fd = FaceDetector()
cap = cv2.VideoCapture(0)
width = int(cap.get(3))  # float
height = int(cap.get(4))  # float
cap.read()
ret, frame = cap.read()
face_array, image, face_location = fd.detect(frame)
landmarks = face_array["landmarks"]
for i in range(len(landmarks)):
    mark = landmarks[i]
    cv2.circle(frame, (int(mark[0]), int(mark[1])), 3, (255, 255, 255))
    cv2.putText(frame, str(i), (int(mark[0]-5), int(mark[1])-5), cv2.FONT_HERSHEY_PLAIN, 0.7, (127, 127, 127))
print(stf.load(landmarks))
cv2.imwrite("image.png", frame)

