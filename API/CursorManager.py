import cv2
import numpy as np
from mediapipe.python.solutions.hands import HandLandmark as HandLM
from API.UiManager import UiManager, overlay_image


class CursorManager():
    def __init__(self, cursorRightPath: str, cursorLeftPath: str, cursorLFdimentions=(30, 30),
                 cursorRTdimentions=(30, 30)):
        self.uiManager = UiManager()
        self.cursorRT = cv2.resize(cv2.imread(cursorRightPath, cv2.IMREAD_UNCHANGED), cursorRTdimentions)
        self.cursorClick = []
        self.cursorLF = cv2.resize(cv2.imread(cursorLeftPath, cv2.IMREAD_UNCHANGED), cursorLFdimentions)
        self.cursorLFpos = [0, 0]
        self.cursorRTpos = [0, 0]

    def displayCursor(self, background, xStartPosition, yStartPosition, cursorName: str):
        if cursorName == "Right":
            self.cursorRTpos = [xStartPosition, yStartPosition]
            return overlay_image(background, self.cursorRT, xStartPosition, yStartPosition)
        self.cursorLFpos = [xStartPosition, yStartPosition]
        return overlay_image(background, self.cursorLF, xStartPosition, yStartPosition)

    def click(self, hand):
        self.cursorClick.clear()
        self.cursorClick.append(hand.getLandmarkX(HandLM.INDEX_FINGER_TIP))
        self.cursorClick.append(hand.getLandmarkY(HandLM.INDEX_FINGER_TIP))

    def overlay_image_with_bound_box(self, background, overlay, x_offset, y_offset):
        bg_h, bg_w, bg_channels = background.shape
        fg_h, fg_w, fg_channels = overlay.shape

        assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
        assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

        # center by default
        if x_offset is None:
            x_offset = (bg_w - fg_w) // 2
        if y_offset is None:
            y_offset = (bg_h - fg_h) // 2

        w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
        h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

        if w < 1 or h < 1:
            return

        # clip foreground and background images to the overlapping regions
        bg_x = max(0, x_offset)
        bg_y = max(0, y_offset)
        fg_x = max(0, x_offset * -1)
        fg_y = max(0, y_offset * -1)
        foreground = overlay[fg_y:fg_y + h, fg_x:fg_x + w]
        background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

        # separate alpha and color channels from the foreground image
        foreground_colors = foreground[:, :, :3]
        alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

        # construct an alpha_mask that matches the image shape
        alpha_mask = alpha_channel[:, :, np.newaxis]
        # combine the background with the overlay image weighted by alpha
        composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

        # overwrite the section of the background image that has been updated
        background[bg_y:bg_y + h, bg_x:bg_x + w] = composite
        return background
