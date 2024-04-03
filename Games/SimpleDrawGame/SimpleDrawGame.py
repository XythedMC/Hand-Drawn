import math
import time

import cv2
import numpy
from mediapipe.python.solutions.hands import HandLandmark as HandLM
from API.handTrackerWrapper import HandTrackerWrapper
from API.CursorManager import CursorManager


class SimpleDrawGame:
    def __init__(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        cursorManager = CursorManager(r'Games/SimpleDrawGame/cursorRight.png', r'Games/SimpleDrawGame/cursorLeft.png')
        tracker = HandTrackerWrapper()
        bg_image = cv2.resize(cv2.imread(r'Games/SimpleDrawGame/img.png'), (tracker.cap.read()[1].shape[1], tracker.cap.read()[1].shape[0]))
        handPositionListRT = []
        handPositionListLF = []
        mode = 0
        fps = 0.0
        hand_colors = {"Right": (255, 0, 0),
                       "Left": (0, 0, 255)}
        while True:
            time1 = time.time()
            tracker.update_hands_list()
            for hand in tracker.hands_list:
                if hand.isIndexFingerUp():
                    color = hand_colors[hand.side]
                    if mode == 1:
                        cv2.circle(bg_image, (hand.getLandmarkX(HandLM.INDEX_FINGER_TIP),
                                              hand.getLandmarkY(HandLM.INDEX_FINGER_TIP)), 6, color, cv2.FILLED)
                    else:
                        if hand == tracker.hands_list.right:
                            if len(handPositionListRT) != 4:
                                handPositionListRT.append(hand.getLandmarkX(HandLM.INDEX_FINGER_TIP))
                                handPositionListRT.append(hand.getLandmarkY(HandLM.INDEX_FINGER_TIP))
                            else:
                                cv2.line(bg_image, (handPositionListRT[0], handPositionListRT[1]),
                                         (handPositionListRT[2], handPositionListRT[3]), color, 10, cv2.FILLED)
                                handPositionListRT.remove(handPositionListRT[0])
                                handPositionListRT.remove(handPositionListRT[0])
                        else:
                            if len(handPositionListLF) != 4:
                                handPositionListLF.append(hand.getLandmarkX(HandLM.INDEX_FINGER_TIP))
                                handPositionListLF.append(hand.getLandmarkY(HandLM.INDEX_FINGER_TIP))
                            else:
                                cv2.line(bg_image, (handPositionListLF[0], handPositionListLF[1]),
                                         (handPositionListLF[2], handPositionListLF[3]), color, 10, cv2.FILLED)
                                handPositionListLF.remove(handPositionListLF[0])
                                handPositionListLF.remove(handPositionListLF[0])
                else:
                    handPositionListLF.clear()
                    handPositionListRT.clear()
            if tracker.hands_list.has_left():
                x, y = tracker.hands_list.left.getLandmarkXY(HandLM.INDEX_FINGER_TIP)
                cursorManager.displayCursor(bg_image.copy(), x, y, "Left")
            if tracker.hands_list.has_right():
                x, y = tracker.hands_list.right.getLandmarkXY(HandLM.INDEX_FINGER_TIP)
                cursorManager.displayCursor(bg_image.copy(), x, y, "Right")
            time2 = time.time()
            fps = 1 / (time2-time1)
            time1 = time2
            print(str(numpy.round(fps, 1)) + " fps")
            bg_image_copy = bg_image.copy()
            cv2.namedWindow("Canvas", cv2.WINDOW_NORMAL)
            cv2.imshow("Canvas", bg_image_copy)

            image = tracker.get_hands_image()
            cv2.imshow("Video", image)

            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                break
        cv2.destroyAllWindows()
        self.is_running = False

