import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import cv2
from mediapipe.python.solutions.hands import HandLandmark as HandLM
from API.handTrackerWrapper import HandTrackerWrapper
from API.CursorManager import CursorManager
from API.UiManager import UiManager
#from Games.SimpleDrawGame.SimpleDrawGame import SimpleDrawGame
#from Games.SimpleMazeGame.SimpleMazeGame import SimpleMazeGame
from Games.MainMenu.SimpleDrawGame import SimpleDrawGame
import time

class MainMenu:
    def __init__(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        cursorManager = CursorManager(r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\MainMenu\cursorRight.png', r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\MainMenu\cursorLeft.png')
        tracker = HandTrackerWrapper()
        uiManager = UiManager()
        bg_image = cv2.resize(cv2.imread(r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\MainMenu\img.png'), (tracker.cap.read()[1].shape[1], tracker.cap.read()[1].shape[0]))
        handPositionListRT = []
        handPositionListLF = []
        mode = 0
        hand_colors = {"Right": (0, 0, 255),
                       "Left": (255, 0, 0)}
        game_open = 0
        x = bg_image.shape[1]
        y = bg_image.shape[0]
        SimpleDrawGameButton = uiManager.Button(bg_image, int(x / 8), int(y / 2), int(x / 2), int(y - (y / 8)), [0, 255, 251])
        SimpleDrawGameButton.CreateButton()
        SimpleDrawGameButton.CreateImageButton(cv2.imread(r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\MainMenu\clock.png', cv2.IMREAD_UNCHANGED))
        BackButton = uiManager.Button(bg_image, int(x - (x / 10)), int(0), int(x), int(y / 7), [0, 0, 251])
        #BackButton.CreateButton()
        while True:
            tracker.update_hands_list()
            for hand in tracker.hands_list:
                if hand.isHandClick():
                    cursorManager.click(hand)
                    print("click")
            if game_open == 1:
                draw_game = SimpleDrawGame()
                bg_image = draw_game.run(tracker, bg_image.copy(), r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\SimpleDrawGame\img.png', handPositionListRT, handPositionListLF)
            elif game_open == 2:
                draw_game = SimpleDrawGame()
                bg_image = draw_game.run(tracker, bg_image.copy(),
                                         r'C:\Users\User\PycharmProjects\handTrackingGiftedProject\Games\SimpleDrawGame\img.png',
                                         handPositionListRT, handPositionListLF, FirstRun=False)
            if SimpleDrawGameButton.isClicked(cursorManager):
                if game_open == 1 or game_open == 2:
                    game_open = 2
                else:
                    game_open = 1
            bg_image_copy = bg_image.copy()
            if tracker.hands_list.has_left():
                x, y = tracker.hands_list.left.getLandmarkXY(HandLM.INDEX_FINGER_TIP)
                cursorManager.displayCursor(bg_image_copy, x, y, "Left")
            if tracker.hands_list.has_right():
                x, y = tracker.hands_list.right.getLandmarkXY(HandLM.INDEX_FINGER_TIP)
                cursorManager.displayCursor(bg_image_copy, x, y, "Right")
            cv2.namedWindow("MainMenu", cv2.WINDOW_GUI_NORMAL)
            cv2.resizeWindow('MainMenu', bg_image_copy.shape[1], bg_image_copy.shape[0])
            cv2.imshow("MainMenu", bg_image_copy)
            cv2.setWindowProperty('MainMenu', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            image = tracker.cap.read()[1]
            image = cv2.flip(image, 1)
            if tracker.hands_list.has_right():
                image = cv2.circle(image, tracker.hands_list.right.getLandmarkXY(HandLM.INDEX_FINGER_TIP), 4,
                                   (0, 0, 255), cv2.LINE_AA)
            if tracker.hands_list.has_left():
                image = cv2.circle(image, tracker.hands_list.left.getLandmarkXY(HandLM.INDEX_FINGER_TIP), 4,
                                   (255, 0, 0), cv2.LINE_AA)
            cv2.imshow("Video", image)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                break
        cv2.destroyAllWindows()
        self.is_running = False

if __name__ == '__main__':
    mainmenu = MainMenu()
    mainmenu.run()