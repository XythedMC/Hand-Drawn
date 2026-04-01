from mediapipe.tasks.python.vision import HandLandmarker

# Hand landmark indices
INDEX_FINGER_TIP = 8
INDEX_FINGER_PIP = 6
INDEX_FINGER_DIP = 7
MIDDLE_FINGER_TIP = 12
MIDDLE_FINGER_MCP = 9
MIDDLE_FINGER_PIP = 10
RING_FINGER_TIP = 16
RING_FINGER_MCP = 13
RING_FINGER_PIP = 14
PINKY_TIP = 20
PINKY_MCP = 17
PINKY_PIP = 18


class SimpleHand:
    def __init__(self, id, side, score, lmlist):
        self.id = id
        self.side = side
        self.score = score
        self.lmlist = lmlist
        self.cx, self.cy = self.getLandmarkXY(INDEX_FINGER_TIP)

    # Override for print purpose
    def __str__(self):
        return f"{self.side}:index position {self.cx}, {self.cy}"

    def get_xy(self):
        return self.getLandmarkXY(INDEX_FINGER_TIP)

    def getLandmarkXY(self, targetLm):
        x = self.lmlist[targetLm][1]
        y = self.lmlist[targetLm][2]
        return x, y

    def getLandmarkX(self, targetLm):
        x = self.lmlist[targetLm][1]
        return x

    def getLandmarkY(self, targetLm):
        y = self.lmlist[targetLm][2]
        return y

    def isIndexFingerUp(self):
        if self.getLandmarkY(INDEX_FINGER_TIP) < self.getLandmarkY(
                INDEX_FINGER_PIP) and self.getLandmarkY(MIDDLE_FINGER_TIP) > self.getLandmarkY(
            MIDDLE_FINGER_MCP) and self.getLandmarkY(RING_FINGER_TIP) > self.getLandmarkY(
            RING_FINGER_MCP) and self.getLandmarkY(PINKY_TIP) > self.getLandmarkY(
            PINKY_MCP) and self.getLandmarkY(INDEX_FINGER_TIP) < self.getLandmarkY(
            INDEX_FINGER_DIP):
            return True

    def isHandOpen(self):
        if self.getLandmarkY(INDEX_FINGER_TIP) < self.getLandmarkY(
                INDEX_FINGER_PIP) and self.getLandmarkY(MIDDLE_FINGER_TIP) < self.getLandmarkY(
            MIDDLE_FINGER_PIP) and self.getLandmarkY(RING_FINGER_TIP) < self.getLandmarkY(
            RING_FINGER_PIP) and self.getLandmarkY(PINKY_TIP) < self.getLandmarkY(
            PINKY_PIP) and self.getLandmarkY(INDEX_FINGER_TIP) < self.getLandmarkY(
            INDEX_FINGER_DIP):
            return True

    def isHandClick(self):
        if self.getLandmarkY(INDEX_FINGER_TIP) > self.getLandmarkY(
                INDEX_FINGER_PIP) and self.getLandmarkY(MIDDLE_FINGER_TIP) < self.getLandmarkY(
            MIDDLE_FINGER_PIP) and self.getLandmarkY(RING_FINGER_TIP) < self.getLandmarkY(
            RING_FINGER_PIP) and self.getLandmarkY(PINKY_TIP) < self.getLandmarkY(
            PINKY_PIP) and self.getLandmarkY(INDEX_FINGER_TIP) > self.getLandmarkY(
            INDEX_FINGER_DIP):
            return True