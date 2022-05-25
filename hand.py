import traceback
import sys
from unoplayer import UnoPlayer
from card import Card


# import unodqn


def get_class(kls):  # credits to hasen from stackoverflow
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def eq_index(lst, c):
    # print("DEBUG - LIST, C:", [str(i) for i in lst], c)
    for i, j in enumerate(lst):
        if j == c:
            return i
    raise ValueError("Selected card not found!")


# class Hand:
#     def __init__(self, uno_player_class_name, player_name):
#         try:
#             self.player = get_class(uno_player_class_name)
#             self.player = self.player()
#         except:
#             print("Problem with", uno_player_class_name)
#             traceback.print_exc()
#             sys.exit(1)
#         self.player_name = player_name
#         self.cards = []
#
#     def add_card(self, c):
#         self.cards.append(c)
#
#     def size(self):
#         return len(self.cards)
#
#     def play(self, game):
#         played_card = self.player.play(self.cards, game.get_up_card(), game.called_color, game.get_game_state())
#         if played_card == -1:
#             return None
#         else:
#             to_play = self.cards[played_card]
#             del self.cards[played_card]
#             return to_play
#
#     def call_color(self, game):
#         return self.player.call_color(self.cards)
#
#     def is_empty(self):
#         return len(self.cards) == 0
#
#     def __str__(self):
#         return ",".join([str(i) for i in self.cards])
#
#     def count_cards(self):
#         total = 0
#         for i in range(len(self.cards)):
#             total += self.cards[i].forfeit_cost()
#         return total
#
#     def get_player_name(self):
#         return self.player_name


class Hand:
    num_to_color = {1: UnoPlayer.Color.YELLOW, 2: UnoPlayer.Color.BLUE, 3: UnoPlayer.Color.GREEN,
                    0: UnoPlayer.Color.RED}

    def __init__(self, uno_player_class_name, player_name, dqn=False):
        self.dqn = dqn
        try:
            if dqn:
                self.player = None
            else:
                self.player = get_class(uno_player_class_name)
                self.player = self.player()
        except:
            print("Problem with", uno_player_class_name)
            traceback.print_exc()
            sys.exit(1)
        self.player_name = player_name
        self.cards = []
        self.next_card = None
        self.next_color = None

    def add_card(self, c):
        self.cards.append(c)

    def size(self):
        return len(self.cards)

    def set_next_card(self, action):
        self.next_card = int(action)
        action = int(action)
        # print("DEBUG - NEXT CARD: ", self.next_card)
        if self.next_card < 40:
            self.next_card = eq_index(self.cards,
                                      Card(self.num_to_color[action % 4], UnoPlayer.Rank.NUMBER, action // 4))
        elif self.next_card < 44:
            self.next_card = eq_index(self.cards, Card(self.num_to_color[action % 4], UnoPlayer.Rank.SKIP, -1))
        elif self.next_card < 48:
            self.next_card = eq_index(self.cards, Card(self.num_to_color[action % 4], UnoPlayer.Rank.REVERSE, -1))
        elif self.next_card < 52:
            self.next_card = eq_index(self.cards, Card(self.num_to_color[action % 4], UnoPlayer.Rank.DRAW_TWO, -1))
        elif self.next_card < 56:
            self.next_card = eq_index(self.cards, Card(UnoPlayer.Color.NONE, UnoPlayer.Rank.WILD, -1))
            self.next_color = self.num_to_color[action % 4]
        elif self.next_card < 60:
            self.next_card = eq_index(self.cards, Card(UnoPlayer.Color.NONE, UnoPlayer.Rank.WILD_D4, -1))
            self.next_color = self.num_to_color[action % 4]

    def play(self, game, action):
        if self.dqn:
            if -1 < action < 60:
                self.set_next_card(action)
            else:
                self.next_card = -1
            played_card = self.next_card
        else:
            played_card = self.player.play(self.cards, game.get_up_card(), game.called_color, game.get_game_state())
        if played_card == -1 or action == 60:
            return None
        else:
            to_play = self.cards[played_card]
            del self.cards[played_card]
            return to_play

    def call_color(self, game):
        if self.dqn:
            return self.next_color
        return self.player.call_color(self.cards)

    def is_empty(self):
        return len(self.cards) == 0

    def __str__(self):
        return ",".join([str(i) for i in self.cards])

    def count_cards(self):
        total = 0
        for i in range(len(self.cards)):
            total += self.cards[i].forfeit_cost()
        return total

    def get_player_name(self):
        return self.player_name
