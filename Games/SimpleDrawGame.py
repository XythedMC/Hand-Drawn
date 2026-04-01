import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import cv2
from API.handTrackerWrapper import HandTrackerWrapper
from API.CursorManager import CursorManager

# Hand landmark indices
INDEX_FINGER_TIP = 8



class SimpleDrawGame:
    def __init__(self):
        self.is_running = False

    def run(self, frame):
        self.is_running = True
        cursorManager = CursorManager(r'Games/assets/cursorRight.png', r'Games/assets/cursorLeft.png')
        tracker = HandTrackerWrapper()
        bg_image = cv2.resize(cv2.imread(r'Games/assets/mainMenuBG.png'), (tracker.cap.read()[1].shape[1],
                                                                            tracker.cap.read()[1].shape[0]))
        handPositionListRT = []
        handPositionListLF = []
        mode = 0
        hand_colors = {"Right": (0, 0, 255),
                       "Left": (255, 0, 0)}
        cv2.namedWindow("Canvas", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        while True:
            tracker.update_hands_list()
            for hand in tracker.hands_list:
                if hand.isIndexFingerUp():
                    color = hand_colors[hand.side]
                    if mode == 1:
                        cv2.circle(bg_image, (hand.getLandmarkX(INDEX_FINGER_TIP),
                                              hand.getLandmarkY(INDEX_FINGER_TIP)), 6, color, cv2.FILLED)
                    else:
                        if hand == tracker.hands_list.right:
                            if len(handPositionListRT) != 4:
                                handPositionListRT.append(hand.getLandmarkX(INDEX_FINGER_TIP))
                                handPositionListRT.append(hand.getLandmarkY(INDEX_FINGER_TIP))
                            else:
                                cv2.line(bg_image, (handPositionListRT[0], handPositionListRT[1]),
                                         (handPositionListRT[2], handPositionListRT[3]), color, 6, cv2.FILLED)
                                handPositionListRT.remove(handPositionListRT[0])
                                handPositionListRT.remove(handPositionListRT[0])
                        else:
                            if len(handPositionListLF) != 4:
                                handPositionListLF.append(hand.getLandmarkX(INDEX_FINGER_TIP))
                                handPositionListLF.append(hand.getLandmarkY(INDEX_FINGER_TIP))
                            else:
                                cv2.line(bg_image, (handPositionListLF[0], handPositionListLF[1]),
                                         (handPositionListLF[2], handPositionListLF[3]), color, 6, cv2.FILLED)
                                handPositionListLF.remove(handPositionListLF[0])
                                handPositionListLF.remove(handPositionListLF[0])
                elif hand.isHandOpen():
                    bg_image = cv2.resize(cv2.imread(r'Games/assets/mainMenuBG.png'),
                                          (tracker.cap.read()[1].shape[1], tracker.cap.read()[1].shape[0]))
                else:
                    if hand == tracker.hands_list.left:
                        handPositionListLF.clear()
                    else:
                        handPositionListRT.clear()
            bg_image_copy = bg_image.copy()
            if tracker.hands_list.has_left():
                x, y = tracker.hands_list.left.getLandmarkXY(INDEX_FINGER_TIP)
                cursorManager.displayCursor(bg_image_copy, x, y, "Left")
            if tracker.hands_list.has_right():
                x, y = tracker.hands_list.right.getLandmarkXY(INDEX_FINGER_TIP)
                cursorManager.displayCursor(bg_image_copy, x, y, "Right")
            cv2.imshow("Canvas", bg_image_copy)
            image = tracker.cap.read()[1]
            image = cv2.flip(image, 1)
            if tracker.hands_list.has_right():
                image = cv2.circle(image, tracker.hands_list.right.getLandmarkXY(INDEX_FINGER_TIP), 4,
                                   (0, 0, 255), cv2.LINE_AA)
            if tracker.hands_list.has_left():
                image = cv2.circle(image, tracker.hands_list.left.getLandmarkXY(INDEX_FINGER_TIP), 4,
                                   (255, 0, 0), cv2.LINE_AA)
            cv2.imshow("Video", image)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                break
        cv2.destroyAllWindows()
        self.is_running = False
