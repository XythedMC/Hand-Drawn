RT = "Right"
LF = "Left"


class HandsList:
    def __init__(self):
        self.right = None
        self.left = None

    def __str__(self):
        result = ""
        if self.has_right():
            result += str(self.right)
        else:
            result += "Right: not found. "
        if self.has_left():
            result += " " + str(self.left)
        else:
            result += "Left: not found. "
        return result

    def __iter__(self):
        if self.has_right():
            yield self.right
        if self.has_left():
            yield self.left

    def add_hand(self, hand):
        if hand.side == RT:
            self.right = hand
        else:
            self.left = hand

    def count(self):
        return int(self.right is not None) + int(self.left is not None)

    def clear(self):
        self.left = None
        self.right = None

    def has_right(self):
        return self.right is not None

    def has_left(self):
        return self.left is not None
