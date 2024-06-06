from typing import Sequence
from mediapipe.python.solutions.hands import HandLandmark as HandLM
import cv2
from API.CursorManager import CursorManager
from API.SimpleHand import SimpleHand
from API.handTrackerWrapper import HandTrackerWrapper
import numpy as np

class DrawManager():
    def __init__(self, radius, color : dict, thickness, lineType, drawMethod : str):
        self.radius = radius
        self.color = color
        self.thickness = thickness
        self.lineType = lineType
        self.PositionListRT = []
        self.PositionListLF = []
        self.LinePositionListRT = []
        self.LinePositionListLF = []
        self.drawMethod = drawMethod
        if self.drawMethod != "Line" and self.drawMethod != "Dot":
            raise ValueError("drawMethod must be Line or Dot!")

    def Draw(self, x, y, tracker, hand, image):
        if self.drawMethod == "Dot":
            return self.DrawByDots(x, y, tracker, hand, image)
        elif self.drawMethod == "Line":
            return self.DrawByLines(image, x, y, tracker, hand)

    def DrawByDots(self, x, y, tracker, hand, frame):
        if hand == tracker.hands_list.right:
            cv2.circle(frame, (x, y), self.radius, self.color["Right"], self.lineType)
        else:
            cv2.circle(frame, (x, y), self.radius, self.color["Left"], self.lineType)
        return frame

    def DrawByLines(self, bg_image, x, y, tracker : HandTrackerWrapper, hand : SimpleHand):
        if hand == tracker.hands_list.right:
            if len(self.LinePositionListRT) != 4:
                self.LinePositionListRT.append(x)
                self.LinePositionListRT.append(y)
            else:
                cv2.line(bg_image, (self.LinePositionListRT[0], self.LinePositionListRT[1]), (self.LinePositionListRT[2], self.LinePositionListRT[3]), self.color["Right"], self.thickness, self.lineType)
                self.PositionListRT.append(self.LinePositionListRT)
                self.LinePositionListRT.remove(self.LinePositionListRT[0])
                self.LinePositionListRT.remove(self.LinePositionListRT[0])
        else:
            if len(self.LinePositionListLF) != 4:
                self.LinePositionListLF.append(x)
                self.LinePositionListLF.append(y)
            else:
                cv2.line(bg_image, (self.LinePositionListLF[0], self.LinePositionListLF[1]),
                         (self.LinePositionListLF[2], self.LinePositionListLF[3]), self.color["Left"], self.thickness,
                         self.lineType)
                self.PositionListLF.append(self.LinePositionListLF)
                self.LinePositionListLF.remove(self.LinePositionListLF[0])
                self.LinePositionListLF.remove(self.LinePositionListLF[0])
        return bg_image

    def ClearCanvas(self, tracker : HandTrackerWrapper, hand, frame):
        if hand == tracker.hands_list.right:
            frame[np.all(frame == self.color["Right"], axis=-1)] = (255, 255, 255)
            if self.drawMethod == "Line":
                self.LinePositionListRT.clear()
            self.PositionListRT.clear()
        else:
            frame[np.all(frame == self.color["Left"], axis=-1)] = (255, 255, 255)
            if self.drawMethod == "Line":
                self.LinePositionListLF.clear()
            self.PositionListLF.clear()
        return frame

