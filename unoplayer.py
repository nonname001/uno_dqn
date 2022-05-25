from enum import Enum


class UnoPlayer:
    class Color(Enum):
        RED = 0
        YELLOW = 1
        GREEN = 2
        BLUE = 3
        NONE = 4

    class Rank(Enum):
        NUMBER = 0
        SKIP = 1
        REVERSE = 2
        DRAW_TWO = 3
        WILD = 4
        WILD_D4 = 5

    def play(self, hand, up_card, called_color, state):
        pass

    def call_color(self, hand):
        pass
