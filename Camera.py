from __future__ import print_function
import cv2


class Camera:
    def __init__(self, ranges=100):
        a = 1
        self.ranges = ranges

    def take_photo(self, path, out=True):
        cap = cv2.VideoCapture(0)
        for i in range(1, self.ranges + 1):
            cap.read()
            progress = int(i / self.ranges * 100)
            if out:
                if progress < 100:
                    ret = "\r"
                else:
                    ret = "\n"
                print(str(progress) + "% завершено", end=ret)
        ret, frame = cap.read()
        if path != "return":
            cv2.imwrite(path, frame)
            cap.release()
        else:
            return frame
