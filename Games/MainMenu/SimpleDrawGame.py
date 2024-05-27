import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import cv2
from mediapipe.python.solutions.hands import HandLandmark as HandLM
from API.handTrackerWrapper import HandTrackerWrapper
from API.CursorManager import CursorManager
from API.UiManager import UiManager


class SimpleDrawGame:
    def __init__(self):
        self.is_running = False
        self.BackButton = None

    def run(self, tracker: HandTrackerWrapper, bg_image, bg_path: str, handPositionListRT: list,
            handPositionListLF: list, uiManager: UiManager,
            cursorManager : CursorManager, FirstRun=True):
        self.is_running = True
        if FirstRun:
            bg_image = cv2.resize(cv2.imread(bg_path), (tracker.cap.read()[1].shape[1],
                                                        tracker.cap.read()[1].shape[0]))
            handPositionListRT = []
            handPositionListLF = []
        mode = 0
        hand_colors = {"Right": (0, 0, 255),
                       "Left": (255, 0, 0)}
        x = bg_image.shape[1]
        y = bg_image.shape[0]
        self.BackButton = uiManager.Button(bg_image, int(x - x / 7), int(0), int(x), int(y / 6), [0, 0, 0])
        self.BackButton.CreateImageButton(
            cv2.imread(r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\assets\back_button.jpg'))
        if self.BackButton.isCursorHover(cursorManager) is False:
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
                                         (handPositionListRT[2], handPositionListRT[3]), color, 6, cv2.FILLED)
                                handPositionListRT.remove(handPositionListRT[0])
                                handPositionListRT.remove(handPositionListRT[0])
                        else:
                            if len(handPositionListLF) != 4:
                                handPositionListLF.append(hand.getLandmarkX(HandLM.INDEX_FINGER_TIP))
                                handPositionListLF.append(hand.getLandmarkY(HandLM.INDEX_FINGER_TIP))
                            else:
                                cv2.line(bg_image, (handPositionListLF[0], handPositionListLF[1]),
                                         (handPositionListLF[2], handPositionListLF[3]), color, 6, cv2.FILLED)
                                handPositionListLF.remove(handPositionListLF[0])
                                handPositionListLF.remove(handPositionListLF[0])
                elif hand.isHandOpen():
                    bg_image = cv2.resize(cv2.imread(bg_path),
                                          (tracker.cap.read()[1].shape[1], tracker.cap.read()[1].shape[0]))
                    self.BackButton = uiManager.Button(bg_image, int(x - x / 7), int(0), int(x), int(y / 6),
                                                       [0, 0, 0])
                    #self.BackButton = uiManager.Button(bg_image, int(x / 3), int(y / 3), int(x - (x / 3)), int(y / 2),
                    #                                   [0, 255, 251])
                    self.BackButton.CreateImageButton(
                        cv2.imread(r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\assets\back_button.jpg'))
                else:
                    if hand == tracker.hands_list.left:
                        handPositionListLF.clear()
                    else:
                        handPositionListRT.clear()
        return bg_image
