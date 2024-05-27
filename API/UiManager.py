import cv2
import numpy as np


def overlay_image(background, overlay, x_offset, y_offset):
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


class UiManager:
    class Button:
        def __init__(self, frame, xPos1, yPos1, xPos2, yPos2, color, text=None):
            self.frame = frame
            self.xPos1 = xPos1
            self.yPos1 = yPos1
            self.xPos2 = xPos2
            self.yPos2 = yPos2
            self.color = color
            self.text = text

        def CreateButton(self):
            image = cv2.rectangle(self.frame, (self.xPos1, self.yPos1), (self.xPos2, self.yPos2), self.color, -1)
            print(self.xPos2)
            print(image.shape[1])
            if self.text is not None:
                textsize = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                cv2.putText(self.frame, self.text, ((int(self.xPos2 - textsize[0]) / 2), int(self.yPos2 / 2)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        def CreateImageButton(self, image):
            if image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
            image = cv2.resize(image, (self.xPos2 - self.xPos1, self.yPos2 - self.yPos1))
            overlay_image(self.frame, image, self.xPos1, self.yPos1)
            if self.text is not None:
                textsize = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                cv2.putText(self.frame, self.text, ((int(self.xPos2 - textsize[0]) / 2), int(self.yPos2 / 2)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        def isClicked(self, cursorManager):
            if cursorManager.cursorClick:
                if self.xPos2 > cursorManager.cursorClick[0] > self.xPos1 and self.yPos2 > cursorManager.cursorClick[
                    1] > self.yPos1:
                    return True
            return False

        def isCursorHover(self, cursorManager):
            if ((self.xPos2 > cursorManager.cursorRTpos[0] > self.xPos1 and self.yPos2 > cursorManager.cursorRTpos[1] > self.yPos1)
                    or (self.xPos2 > cursorManager.cursorLFpos[0] > self.xPos1 and self.yPos2 >
                        cursorManager.cursorLFpos[1] > self.yPos1)):
                return True
            return False
