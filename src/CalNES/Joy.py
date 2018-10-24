from enum import Enum

class Button(Enum):
    A = 0
    B = 1
    SELECT = 2
    START = 3
    UP = 4
    DOWN = 5
    LEFT = 6
    RIGHT = 7

class Joy:
    def __init__(self):
        self.state = [0x40] * 8

    def button_down(self, button):
        print("{} pressed!".format(button))
        self.state[button.value] = 0x41

    def button_up(self, button):
        print("{} released!".format(button))
        self.state[button.value] = 0x40
