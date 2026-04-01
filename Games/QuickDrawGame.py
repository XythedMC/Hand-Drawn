import random
import cv2
from API.handTrackerWrapper import HandTrackerWrapper
from API.CursorManager import CursorManager
from API.QuickDrawPredictor import QuickDrawPredictor
import time
from tensorflow import keras
import matplotlib.pyplot as plt

# Hand landmark indices
INDEX_FINGER_TIP = 8
import numpy as np

class QuickDrawGame:
    def __init__(self):
        self.is_running = False

    def run(self):
        guess_list = []
        self.is_running = True
        start_time = time.time()
        model = keras.saving.load_model('Games/QuickDrawGame/sketch_recognition_mobilenet.keras', compile=False)
        cursorManager = CursorManager(r'Games/QuickDrawGame/cursorRight.png', r'Games/SimpleDrawGame/cursorLeft.png')
        predictor = QuickDrawPredictor(model=model)
        tracker = HandTrackerWrapper()
        bg_image = cv2.resize(cv2.imread(r'Games/QuickDrawGame/mainMenuBG.png').copy(), (tracker.cap.read()[1].shape[1], tracker.cap.read()[1].shape[0]))
        mode = 0
        word = random.choice(predictor.label_list).replace('_', ' ')
        guess_txt = "I see"
        handPositionListRT = []
        handPositionListLF = []
        game_state = 1
        hand_colors = {"Right": (0, 0, 0),
                       "Left": (0, 0, 0)}

        cv2.namedWindow("Canvas", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        if game_state == 1:
            while game_state == 1:
                if guess_txt == "I see":
                    cv2.putText(bg_image.copy(), guess_txt,(int(bg_image.copy().shape[0] / 2), bg_image.copy().shape[1] - 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                tracker.update_hands_list()
                cv2.putText(bg_image, word, (int(bg_image.shape[0] / 2), 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0,0), 2, cv2.LINE_AA)
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
                                             (handPositionListRT[2], handPositionListRT[3]), color, 10, cv2.FILLED)
                                    handPositionListRT.remove(handPositionListRT[0])
                                    handPositionListRT.remove(handPositionListRT[0])
                            else:
                                if len(handPositionListLF) != 4:
                                    handPositionListLF.append(hand.getLandmarkX(INDEX_FINGER_TIP))
                                    handPositionListLF.append(hand.getLandmarkY(INDEX_FINGER_TIP))
                                else:
                                    cv2.line(bg_image, (handPositionListLF[0], handPositionListLF[1]),
                                             (handPositionListLF[2], handPositionListLF[3]), color, 10, cv2.FILLED)
                                    handPositionListLF.remove(handPositionListLF[0])
                                    handPositionListLF.remove(handPositionListLF[0])
                    else:
                        handPositionListLF.clear()
                        handPositionListRT.clear()
                    if hand.isHandOpen():
                        bg_image = cv2.resize(cv2.imread(r'Games/QuickDrawGame/mainMenuBG.png').copy(), (920, 768))
                bg_image_copy = bg_image.copy()
                if tracker.hands_list.has_left():
                    x, y = tracker.hands_list.left.getLandmarkXY(INDEX_FINGER_TIP)
                    cursorManager.displayCursor(bg_image_copy, x, y, "Left")
                if tracker.hands_list.has_right():
                    x, y = tracker.hands_list.right.getLandmarkXY(INDEX_FINGER_TIP)
                    cursorManager.displayCursor(bg_image_copy, x, y, "Right")
                if (time.time() - start_time) >= 2:
                    cv2.imshow("image", bg_image)
                    prediction, guesses = predictor.process(predictor.predict(bg_image.copy()), guess_list)
                    guess_list = guesses
                    prediction = prediction.replace('_', ' ')
                    print(prediction)
                    print(guess_list)
                    print(bg_image_copy.shape)
                    if len(guess_txt.split(' ')[1:]) > 4:
                        guess_txt = "I see"
                    else:
                        guess_txt = guess_txt + ' ' + prediction + ','
                    print(int(bg_image_copy.shape[0] / 2), bg_image_copy.shape[1] - 100)
                    #textsize = cv2.getTextSize(guess_txt, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                    #textX = int(bg_image_copy[0] - (textsize[0] / 2))
                    #cv2.putText(bg_image_copy, guess_txt,(textX, bg_image_copy[1] - 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    if prediction is word:
                        game_state = 0
                        print("True")
                        start_time = time.time()
                cv2.imshow("Canvas", bg_image_copy)

                image = tracker.get_hands_image()
                cv2.imshow("Video", image)

                if (cv2.waitKey(1) & 0xFF) == ord('m'):
                    plt.show()
                if (cv2.waitKey(1) & 0xFF) == ord('q'):
                    break

                if game_state == 0:
                    cv2.rectangle(bg_image_copy, (0, 0), (bg_image_copy.shape[1], bg_image_copy.shape[0]),
                                  (12, 216, 235))
                    cv2.putText(bg_image_copy, f"OH I KNOW, ITS {prediction.upper()}",
                                (int(bg_image_copy.shape[0] / 2), int(bg_image_copy.shape[1] / 2)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.destroyAllWindows()
        self.is_running = False
