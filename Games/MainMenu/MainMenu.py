import math
import time

import cv2
import numpy
from mediapipe.python.solutions.hands import HandLandmark as HandLM
from API.handTrackerWrapper import HandTrackerWrapper
from API.CursorManager import CursorManager


class MainMenu:
    def __init__(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        cap = cv2.VideoCapture(0)
        fps = 0.0
        tracker = HandTrackerWrapper()
        while True:
            time1 = time.time()
            ret, frame = cap.read()
            time2 = time.time()
            fps = 1 / (time2 - time1)
            time1 = time2
            print(str(numpy.round(fps, 1)) + " fps")
            #print(time.time() - time1)
            #tracker.update_hands_list()
            print(time.time())
            print(tracker.hands_list)

            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                break
        cv2.destroyAllWindows()
        self.is_running = False

if __name__ == '__main__':
    game = MainMenu()
    game.run()