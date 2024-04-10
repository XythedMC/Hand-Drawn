import cv2
import mediapipe as mp

from API.HandsList import HandsList
from API.SimpleHand import SimpleHand


class HandTrackerWrapper:
    def __init__(self, flip_image=True, camera_ch=0, mode=False, max_hands=2, detection_con=0.5, model_complexity=1, track_con=0.5):
        self.__mp_hands = mp.solutions.hands.Hands(mode, max_hands, model_complexity,
                                                   detection_con, track_con)
        self.hands_list = HandsList()
        self.__flip_image = flip_image
        self.found_hands = False
        self.cap = cv2.VideoCapture(camera_ch)

    def update_hands_list(self):

        success, image = self.cap.read()

        if self.__flip_image:
            image = cv2.flip(image, 1)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.__mp_hands.process(image_rgb)

        count = 0
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if results.multi_handedness:
                    hand = results.multi_hand_landmarks[count]
                    hand_classification = results.multi_handedness[count]
                    side = hand_classification.classification[0].label
                    score = hand_classification.classification[0].score
                    lm_list = []
                    for lm_id, lm in enumerate(hand.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lm_list.append([lm_id, cx, cy])
                    # Create simple hand object
                    detected_hand = SimpleHand(count, side, score, lm_list)
                    # Add this hand found to the list
                    self.hands_list.add_hand(detected_hand)
                    count += 1
        self.found_hands = count > 0

    def get_hands_image(self):
        success, image = self.cap.read()

        if self.__flip_image:
            image = cv2.flip(image, 1)
        count = 0
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.__mp_hands.process(image_rgb)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                count += 1
                mp.solutions.drawing_utils.draw_landmarks(image, handLms, mp.solutions.hands.HAND_CONNECTIONS)
        self.found_hands = count > 0
        return image
