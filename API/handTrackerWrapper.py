import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode

from API.HandsList import HandsList
from API.SimpleHand import SimpleHand


class HandTrackerWrapper:
    def __init__(self, flip_image=True, camera_ch=0, mode=False, max_hands=2, detection_con=0.5, model_complexity=1, track_con=0.5):
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path='API/hand_landmarker.task'),
            running_mode=VisionRunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_con,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=track_con
        )
        self.__landmarker = HandLandmarker.create_from_options(options)
        self.hands_list = HandsList()
        self.__flip_image = flip_image
        self.found_hands = False
        self.cap = cv2.VideoCapture(camera_ch)
        self.timestamp = 0

    def update_hands_list(self):

        success, image = self.cap.read()

        if self.__flip_image:
            image = cv2.flip(image, 1)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        results = self.__landmarker.detect_for_video(mp_image, self.timestamp)
        self.timestamp += 1

        count = 0
        if results.hand_landmarks:
            for hand_idx, hand in enumerate(results.hand_landmarks):
                handedness = results.handedness[hand_idx]
                side = handedness[0].category_name
                score = handedness[0].score
                lm_list = []
                for lm_id, lm in enumerate(hand):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([lm_id, cx, cy])
                detected_hand = SimpleHand(count, side, score, lm_list)
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
