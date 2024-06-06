import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import time
import cv2
from mediapipe.python.solutions.hands import HandLandmark as HandLM
from API.handTrackerWrapper import HandTrackerWrapper
from API.CursorManager import CursorManager
from API.DrawManager import DrawManager


class SimpleDrawGame:
    def __init__(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        cursorManager = CursorManager(
            r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\SimpleDrawGame\cursorRight.png',
            r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\SimpleDrawGame\cursorLeft.png')
        tracker = HandTrackerWrapper()
        bg_image = cv2.resize(
            cv2.imread(r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\SimpleDrawGame\img.png'),
            (tracker.cap.read()[1].shape[1],
             tracker.cap.read()[1].shape[0]))
        hand_colors = {"Right": (0, 0, 255),
                       "Left": (255, 0, 0)}
        drawManager = DrawManager(6, hand_colors, 6, cv2.FILLED, "Dot")
        handPositionListRT = []
        handPositionListLF = []

        while True:
            tracker.update_hands_list()
            for hand in tracker.hands_list:
                if hand.isIndexFingerUp():
                    bg_image = drawManager.Draw(hand.getLandmarkX(HandLM.INDEX_FINGER_TIP),
                                                hand.getLandmarkY(HandLM.INDEX_FINGER_TIP), tracker, hand,
                                                bg_image)
                elif hand.isHandOpen():
                    bg_image = drawManager.ClearCanvas(tracker, hand, bg_image)
                else:
                    if hand == tracker.hands_list.left:
                        handPositionListLF.clear()
                    else:
                        handPositionListRT.clear()
            bg_image_copy = bg_image.copy()
            if tracker.hands_list.has_left():
                x, y = tracker.hands_list.left.getLandmarkXY(HandLM.INDEX_FINGER_TIP)
                cursorManager.displayCursor(bg_image_copy, x, y, "Left")
            if tracker.hands_list.has_right():
                x, y = tracker.hands_list.right.getLandmarkXY(HandLM.INDEX_FINGER_TIP)
                cursorManager.displayCursor(bg_image_copy, x, y, "Right")
            cv2.namedWindow("Canvas", cv2.WINDOW_GUI_NORMAL)
            cv2.imshow("Canvas", bg_image_copy)
            cv2.setWindowProperty("Canvas", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                break
        cv2.destroyAllWindows()
        self.is_running = False


if __name__ == '__main__':
    draw = SimpleDrawGame()
    draw.run()
