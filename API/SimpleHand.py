from mediapipe.python.solutions.hands import HandLandmark as HandLM


class SimpleHand:
    def __init__(self, id, side, score, lmlist):
        self.id = id
        self.side = side
        self.score = score
        self.lmlist = lmlist
        self.cx, self.cy = self.getLandmarkXY(HandLM.INDEX_FINGER_TIP)

    # Override for print purpose
    def __str__(self):
        return f"{self.side}:index position {self.cx}, {self.cy}"

    def get_xy(self):
        return self.getLandmarkXY(HandLM.INDEX_FINGER_TIP)

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
        if self.getLandmarkY(HandLM.INDEX_FINGER_TIP) < self.getLandmarkY(
                HandLM.INDEX_FINGER_PIP) and self.getLandmarkY(HandLM.MIDDLE_FINGER_TIP) > self.getLandmarkY(
            HandLM.MIDDLE_FINGER_MCP) and self.getLandmarkY(HandLM.RING_FINGER_TIP) > self.getLandmarkY(
            HandLM.RING_FINGER_MCP) and self.getLandmarkY(HandLM.PINKY_TIP) > self.getLandmarkY(
            HandLM.PINKY_MCP) and self.getLandmarkY(HandLM.INDEX_FINGER_TIP) < self.getLandmarkY(
            HandLM.INDEX_FINGER_DIP):
            return True

    def isHandOpen(self):
        if self.getLandmarkY(HandLM.INDEX_FINGER_TIP) < self.getLandmarkY(
                HandLM.INDEX_FINGER_PIP) and self.getLandmarkY(HandLM.MIDDLE_FINGER_TIP) < self.getLandmarkY(
            HandLM.MIDDLE_FINGER_PIP) and self.getLandmarkY(HandLM.RING_FINGER_TIP) < self.getLandmarkY(
            HandLM.RING_FINGER_PIP) and self.getLandmarkY(HandLM.PINKY_TIP) < self.getLandmarkY(
            HandLM.PINKY_PIP) and self.getLandmarkY(HandLM.INDEX_FINGER_TIP) < self.getLandmarkY(
            HandLM.INDEX_FINGER_DIP):
            return True

    def isHandClick(self):
        if self.getLandmarkY(HandLM.INDEX_FINGER_TIP) > self.getLandmarkY(
                HandLM.INDEX_FINGER_PIP) and self.getLandmarkY(HandLM.MIDDLE_FINGER_TIP) < self.getLandmarkY(
            HandLM.MIDDLE_FINGER_PIP) and self.getLandmarkY(HandLM.RING_FINGER_TIP) < self.getLandmarkY(
            HandLM.RING_FINGER_PIP) and self.getLandmarkY(HandLM.PINKY_TIP) < self.getLandmarkY(
            HandLM.PINKY_PIP) and self.getLandmarkY(HandLM.INDEX_FINGER_TIP) > self.getLandmarkY(
            HandLM.INDEX_FINGER_DIP):
            return True